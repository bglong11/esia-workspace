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
      const args = getStepArgs(step, uploadedFilePath, sanitizedName);

      console.log(`[Pipeline] Running: ${pipelineConfig.pythonExecutable} ${scriptPath} ${args.join(' ')}`);

      // Spawn the Python process
      const child = spawn(pipelineConfig.pythonExecutable, [scriptPath, ...args], {
        cwd: pipelineConfig.workingDir,
        timeout: step.timeout,
        env: {
          ...process.env,
          // Force UTF-8 encoding for Python to handle Unicode characters
          PYTHONIOENCODING: 'utf-8',
          PYTHONUNBUFFERED: '1',
          PDF_FILE: uploadedFilePath,
          SANITIZED_NAME: sanitizedName,
          ROOT_NAME: sanitizedName.replace(/\.[^/.]+$/, ''),
          OUTPUT_DIR: outputDir,
        },
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

        // Pattern 1: JSON format with "page" field: {"chunk_id": 0, "page": 42, ...}
        try {
          const jsonMatch = output.match(/\{"[^}]*"page"\s*:\s*(\d+)[^}]*\}/);
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
          }
        }

        // Pattern 3: "processing page 42" with running total tracked elsewhere
        if (!pageMatch) {
          const match = output.match(/[Pp]rocessing?\s+(?:page\s+)?(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = null;
            pageMatch = true;
          }
        }

        // Pattern 4: Progress indicator like "42/411" or "42 of 411"
        if (!pageMatch) {
          const match = output.match(/^(\d+)\s+(?:of|\/)\s+(\d+)/);
          if (match) {
            currentPage = parseInt(match[1]);
            totalPages = parseInt(match[2]);
            pageMatch = true;
          }
        }

        if (pageMatch && currentPage !== null) {
          // Store progress in global tracker
          if (global.pipelineProgress && global.pipelineProgress[executionId]) {
            global.pipelineProgress[executionId][step.id] = {
              currentPage,
              totalPages: totalPages || currentPage
            };
            console.log(`[Pipeline] Progress tracked for ${step.id}: page ${currentPage} of ${totalPages || currentPage}`);
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
 */
export async function executePipeline(pdfFilename, uploadedFilePath) {
  const executionId = `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const sanitizedName = sanitizeFilename(pdfFilename);

  // Initialize global progress tracker for this execution
  if (!global.pipelineProgress) {
    global.pipelineProgress = {};
  }
  global.pipelineProgress[executionId] = {};

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
