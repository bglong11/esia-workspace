/**
 * ESIA Pipeline Configuration
 * Integrates with ESIA pipeline scripts from M:\GitHub\esia-pipeline
 *
 * The pipeline will process uploaded PDFs through a series of steps,
 * passing the sanitized filename to each step for further processing.
 */

import path from 'path';

export const pipelineConfig = {
  // Name of the pipeline
  name: 'ESIA Processing Pipeline',

  // Base working directory for script execution
  // This is where the scripts will run from
  workingDir: '../pipeline/esia-fact-extractor-pipeline',

  // ESIA Pipeline folder location
  pipelineFolder: '../pipeline',

  // Main pipeline orchestrator
  // This runs the complete 4-step ESIA pipeline:
  // 1. Chunk PDF into semantic chunks with page tracking
  // 2. Extract domain-specific facts using archetype-based mapping
  // 3. Analyze extracted facts for consistency and compliance
  // 4. Generate comprehensive ESIA review factsheet (automatic after Step 3)
  steps: [
    {
      id: 'step1_chunking',
      name: 'Step 1: Document Chunking',
      description: 'Converting PDF to semantic chunks with page tracking using Docling...',
      script: '../run-esia-pipeline.py',
      args: ['{PDF_FILE}', '--steps', '1'],
      timeout: 600000, // 10 minutes for chunking
    },
    {
      id: 'step2_extraction',
      name: 'Step 2: Fact Extraction',
      description: 'Extracting domain-specific facts using archetype-based mapping...',
      script: '../run-esia-pipeline.py',
      args: ['{PDF_FILE}', '--steps', '2'],
      timeout: 14400000, // 4 hours for extraction (large documents with LLM calls)
    },
    {
      id: 'step3_analysis',
      name: 'Step 3: Fact Analysis & Factsheet Generation',
      description: 'Analyzing facts for consistency, compliance, and generating comprehensive reports...',
      script: '../run-esia-pipeline.py',
      args: ['{PDF_FILE}', '--steps', '3'],
      timeout: 600000, // 10 minutes for analysis + factsheet generation
    },
  ],

  // Output directory for processed files
  // All pipeline outputs are saved to a single local folder for simplified file management
  outputDir: './data/output',

  // Metadata directory for pipeline execution records
  metadataDir: './data/output/metadata',

  // Python executable (customize if needed)
  // Using Python 3.12 from venv312
  pythonExecutable: path.resolve('../pipeline/venv312/Scripts/python.exe'),
  // pythonExecutable: 'python3',  // Use this on Linux/Mac
};

/**
 * Gets the script arguments for a pipeline step
 * Replaces placeholders with actual values
 */
export function getStepArgs(step, pdfFilename, sanitizedName, outputDir) {
  const rootName = sanitizedName.replace(/\.[^/.]+$/, ''); // Remove extension
  // PDF root = filename without extension (keeps timestamp prefix)
  // Extract just the filename (basename) from the full path if necessary
  const baseName = path.basename(pdfFilename);
  const pdfRoot = baseName.replace(/\.[^/.]+$/, '');

  return step.args.map(arg => {
    let processedArg = arg
      .replace('{PDF_FILE}', pdfFilename)
      .replace('{SANITIZED_NAME}', sanitizedName)
      .replace('{ROOT_NAME}', rootName)
      .replace('{PDF_ROOT}', pdfRoot);

    // Convert relative paths to absolute (those starting with ../)
    if (processedArg.startsWith('../')) {
      processedArg = path.resolve(path.join(pipelineConfig.workingDir, processedArg));
    }

    return processedArg;
  });
}

/**
 * Resolves the script path (supports relative and absolute paths)
 * @param scriptPath - Path to the script (relative or absolute)
 * @param workingDir - Base working directory
 * @returns Full resolved path to the script
 */
export function resolveScriptPath(scriptPath, workingDir) {
  // If absolute path, return as-is
  if (path.isAbsolute(scriptPath)) {
    return scriptPath;
  }

  // Relative path: resolve from working directory
  return path.resolve(workingDir, scriptPath);
}

/**
 * Sanitizes PDF filename to create root name for pipeline
 */
export function sanitizeFilename(filename) {
  // Remove timestamp prefix if present (format: timestamp-originalname)
  const cleanName = filename.replace(/^\d+-/, '');

  // Remove extension
  const rootName = cleanName.replace(/\.[^/.]+$/, '');

  // Sanitize: lowercase, replace spaces/special chars with underscores
  return rootName
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, '');
}
