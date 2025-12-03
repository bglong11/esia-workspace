/**
 * Pipeline Executor - Executes ESIA pipeline steps
 */

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { pipelineConfig, sanitizeFilename, getStepArgs, resolveScriptPath } from './pipeline.config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// In-memory store for pipeline execution status
const executionStatus = new Map();

/**
 * Executes a pipeline step by running the Python script
 */
function executeStep(step, pdfFilename, sanitizedName, uploadedFilePath, executionId, outputDir) {
  return new Promise((resolve, reject) => {
    console.log(`[Pipeline] Executing step: ${step.name}`);
    console.log(`  Script: ${step.script}`);
    console.log(`  Input PDF: ${pdfFilename}`);
    console.log(`  Sanitized name: ${sanitizedName}`);

    try {
      // Resolve the script path (supports relative and absolute paths)
      const scriptPath = resolveScriptPath(step.script, pipelineConfig.workingDir);

      // Check if script exists
      if (!fs.existsSync(scriptPath)) {
        console.warn(`[Pipeline] Warning: Script not found at ${scriptPath}`);
        console.log(`[Pipeline] Falling back to mock execution for demo purposes`);

        // Mock execution if script doesn't exist
        setTimeout(() => {
          resolve({
            stepId: step.id,
            status: 'completed',
            timestamp: new Date(),
            output: {
              message: `${step.name} completed (mock - script not found)`,
              sanitizedName: sanitizedName,
            },
          });
        }, 500);
        return;
      }

      // Prepare arguments
      const args = getStepArgs(step, uploadedFilePath, sanitizedName, outputDir);

      // Quote arguments that contain spaces for shell execution
      const quotedArgs = args.map(arg => {
        // If arg contains spaces and is not already quoted, wrap in double quotes
        if (arg.includes(' ') && !arg.startsWith('"')) {
          return `"${arg}"`;
        }
        return arg;
      });

      console.log(`[Pipeline] Running: ${pipelineConfig.pythonExecutable} ${scriptPath} ${quotedArgs.join(' ')}`);

      // Build environment variables
      const envVars = {
        ...process.env,
        // Force UTF-8 encoding for Python to handle Unicode characters
        PYTHONIOENCODING: 'utf-8',
        PYTHONUNBUFFERED: '1',
        PDF_FILE: uploadedFilePath,
        SANITIZED_NAME: sanitizedName,
        ROOT_NAME: sanitizedName.replace(/\.[^/.]+$/, ''),
        OUTPUT_DIR: outputDir,
      };

      // Only force CPU mode if CUDA is disabled in config
      // When useCuda is true, don't set these vars - let the --use-cuda flag control GPU usage
      if (!pipelineConfig.useCuda) {
        envVars.CUDA_VISIBLE_DEVICES = '';
        envVars.TORCH_DEVICE = 'cpu';
      }

      // Spawn the Python process WITHOUT shell to avoid argument parsing issues
      // Shell mode causes problems with spaces in arguments
      const child = spawn(pipelineConfig.pythonExecutable, ['-u', scriptPath, ...args], {
        cwd: path.dirname(scriptPath), // Use script directory as working directory
        timeout: step.timeout,
        shell: false, // Don't use shell to avoid argument splitting issues
        env: envVars,
      });

      let stdout = '';
      let stderr = '';
      let finished = false;

      // Update execution status with real-time progress
      const progressUpdateInterval = setInterval(() => {
        if (!finished && global.pipelineProgress && global.pipelineProgress[executionId]) {
          const currentProgress = global.pipelineProgress[executionId][step.id];
          if (currentProgress) {
            // This would be updated in the parent executePipeline if we pass execution object
            // For now, the progress is stored and fetched on status requests
          }
        }
      }, 500); // Update progress every 500ms

      // Handle timeout
      const timeoutHandle = setTimeout(() => {
        if (!finished) {
          finished = true;
          child.kill();
          reject(new Error(`Step timeout after ${step.timeout}ms`));
        }
      }, step.timeout);

      child.stdout.on('data', (data) => {
        const output = data.toString();
        stdout += output;
        console.log(`[Pipeline] ${step.id}: ${output}`.trim());

        // Extract page progress from output - try multiple patterns
        let pageMatch = null;
        let currentPage = null;
        let totalPages = null;

        // Pattern 1: JSON format with "page" field (more flexible) - matches "page": X anywhere in JSON
        try {
          const jsonMatch = output.match(/"page"\s*:\s*(\d+)/);
          if (jsonMatch) {
            currentPage = parseInt(jsonMatch[1]);
            // For JSON chunks, we'll track the highest page number seen so far as the total
            if (global.pipelineProgress && global.pipelineProgress[executionId] && global.pipelineProgress[executionId][step.id]) {
              const existing = global.pipelineProgress[executionId][step.id];
              totalPages = Math.max(existing.totalPages || currentPage, currentPage);
            } else {
              totalPages = currentPage;
            }
            pageMatch = true;
            console.log(`[Pipeline] Pattern 1 matched: "page": ${currentPage} (total tracked: ${totalPages})`);
          }
        } catch (e) {
          // Silently ignore JSON parsing errors
        }

        // Pattern 2: "page 42 of 411" or "Page 42/411"
        if (!pageMatch) {
          const match = output.match(/[Pp]age[s]?\s+(\d+)\s+(?:of|\/)\s+(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = parseInt(match[2]);
            pageMatch = true;
            console.log(`[Pipeline] Pattern 2 matched: page ${currentPage} of ${totalPages}`);
          }
        }

        // Pattern 3: "processing page 42" with running total tracked elsewhere
        if (!pageMatch) {
          const match = output.match(/[Pp]rocessing?\s+(?:page\s+)?(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = null;
            pageMatch = true;
            console.log(`[Pipeline] Pattern 3 matched: processing page ${currentPage}`);
          }
        }

        // Pattern 4: Progress indicator like "42/411" or "42 of 411"
        if (!pageMatch) {
          const match = output.match(/^(\d+)\s+(?:of|\/)\s+(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = parseInt(match[2]);
            pageMatch = true;
            console.log(`[Pipeline] Pattern 4 matched: ${currentPage} of ${totalPages}`);
          }
        }

        // Pattern 5: Explicit progress format: "[PROGRESS] Page X of Y"
        if (!pageMatch) {
          const match = output.match(/\[PROGRESS\]\s+Page\s+(\d+)\s+of\s+(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = parseInt(match[2]);
            pageMatch = true;
            console.log(`[Pipeline] Pattern 5 matched (explicit): Page ${currentPage} of ${totalPages}`);
          }
        }

        if (pageMatch && currentPage !== null) {
          // Store progress in global tracker
          if (global.pipelineProgress && global.pipelineProgress[executionId]) {
            global.pipelineProgress[executionId][step.id] = {
              currentPage,
              totalPages: totalPages || currentPage
            };
            console.log(`[Pipeline] ✓ Progress tracked for ${step.id}: page ${currentPage} of ${totalPages || currentPage}`);
          } else {
            console.log(`[Pipeline] ⚠ Warning: pipelineProgress not initialized for ${executionId}/${step.id}`);
          }
        }
      });

      child.stderr.on('data', (data) => {
        const output = data.toString();
        stderr += output;
        console.log(`[Pipeline] ${step.id} ERROR: ${output}`);
      });

      child.on('close', (code) => {
        clearTimeout(timeoutHandle);
        clearInterval(progressUpdateInterval);
        if (finished) return; // Already handled by timeout

        finished = true;

        if (code === 0) {
          console.log(`[Pipeline] Step ${step.id} completed successfully`);
          resolve({
            stepId: step.id,
            status: 'completed',
            timestamp: new Date(),
            output: stdout || `${step.name} completed successfully`,
          });
        } else {
          console.error(`[Pipeline] Step ${step.id} failed with code ${code}`);
          reject(new Error(`Step failed with exit code ${code}: ${stderr}`));
        }
      });

      child.on('error', (err) => {
        clearTimeout(timeoutHandle);
        clearInterval(progressUpdateInterval);
        if (!finished) {
          finished = true;
          console.error(`[Pipeline] Step ${step.id} error:`, err);
          reject(err);
        }
      });
    } catch (error) {
      console.error(`[Pipeline] Error executing step:`, error);
      reject(error);
    }
  });
}

/**
 * Executes the entire pipeline for an uploaded PDF
 * @param {string} pdfFilename - The filename of the uploaded PDF
 * @param {string} uploadedFilePath - The full path to the uploaded PDF file
 * @param {string} executionId - Optional execution ID (if not provided, one will be generated)
 */
export async function executePipeline(pdfFilename, uploadedFilePath, executionId = null) {
  if (!executionId) {
    executionId = `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  const sanitizedName = sanitizeFilename(pdfFilename);

  // Initialize global progress tracker for this execution
  if (!global.pipelineProgress) {
    global.pipelineProgress = {};
    console.log(`[Pipeline] Initialized global.pipelineProgress`);
  }
  global.pipelineProgress[executionId] = {};
  console.log(`[Pipeline] Initialized progress tracking for execution: ${executionId}`);

  // Initialize execution status
  const execution = {
    id: executionId,
    pdfFilename,
    sanitizedName,
    uploadedFilePath,
    status: 'running',
    startTime: new Date(),
    endTime: null,
    steps: [],
    error: null,
  };

  executionStatus.set(executionId, execution);

  try {
    // Create output directory if it doesn't exist
    const outputDir = path.resolve(__dirname, pipelineConfig.outputDir);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
      console.log(`[Pipeline] Created output directory: ${outputDir}`);
    }

    console.log(`[Pipeline] Starting pipeline execution: ${executionId}`);
    console.log(`[Pipeline] Processing PDF: ${pdfFilename}`);
    console.log(`[Pipeline] Sanitized root name: ${sanitizedName}`);
    console.log(`[Pipeline] Output directory: ${outputDir}`);

    // Execute each step in sequence
    for (const stepConfig of pipelineConfig.steps) {
      try {
        // Mark step as running
        const stepData = {
          stepId: stepConfig.id,
          status: 'running',
          name: stepConfig.name,
          description: stepConfig.description,
          progress: null, // Will be updated as step runs
        };
        execution.steps.push(stepData);
        executionStatus.set(executionId, execution);

        // Execute the step with real-time progress updates
        const stepIndex = execution.steps.findIndex((s) => s.stepId === stepConfig.id);

        // Set up periodic progress sync from global tracker
        const progressInterval = setInterval(() => {
          const currentProgress = global.pipelineProgress[executionId]?.[stepConfig.id];
          if (stepIndex !== -1 && currentProgress) {
            execution.steps[stepIndex].progress = currentProgress;
            executionStatus.set(executionId, execution);
          }
        }, 500); // Update progress every 500ms

        let stepResult;
        try {
          stepResult = await executeStep(stepConfig, pdfFilename, sanitizedName, uploadedFilePath, executionId, outputDir);
          clearInterval(progressInterval);

          // Sync final progress from global tracker before marking complete
          const finalProgress = global.pipelineProgress[executionId]?.[stepConfig.id];
          if (stepIndex !== -1 && finalProgress) {
            execution.steps[stepIndex].progress = finalProgress;
          }
        } catch (error) {
          clearInterval(progressInterval);
          throw error;
        }

        // Mark step as completed
        if (stepIndex !== -1) {
          execution.steps[stepIndex] = {
            ...execution.steps[stepIndex],
            status: 'completed',
            output: stepResult.output,
          };
        }

        executionStatus.set(executionId, execution);
      } catch (error) {
        // Mark step as failed
        const stepIndex = execution.steps.findIndex((s) => s.stepId === stepConfig.id);
        if (stepIndex !== -1) {
          execution.steps[stepIndex] = {
            ...execution.steps[stepIndex],
            status: 'failed',
            error: error.message,
          };
        }
        throw error;
      }
    }

    // Pipeline completed successfully
    execution.status = 'completed';
    execution.endTime = new Date();

    console.log(`[Pipeline] Pipeline execution completed: ${executionId}`);
    console.log(`[Pipeline] Output root name: ${sanitizedName}`);

    return execution;
  } catch (error) {
    execution.status = 'failed';
    execution.endTime = new Date();
    execution.error = error.message;

    console.error(`[Pipeline] Pipeline execution failed: ${executionId}`, error);

    return execution;
  }
}

/**
 * Gets the status of a pipeline execution
 */
export function getPipelineStatus(executionId) {
  return executionStatus.get(executionId) || null;
}

/**
 * Gets all pipeline executions
 */
export function getAllPipelineExecutions() {
  return Array.from(executionStatus.values()).sort((a, b) =>
    new Date(b.startTime) - new Date(a.startTime)
  );
}

/**
 * Clears old execution records (older than 1 hour)
 */
export function cleanupOldExecutions() {
  const oneHourAgo = Date.now() - 60 * 60 * 1000;
  for (const [id, execution] of executionStatus.entries()) {
    if (new Date(execution.endTime).getTime() < oneHourAgo) {
      executionStatus.delete(id);
    }
  }
}
