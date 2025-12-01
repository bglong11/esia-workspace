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
  workingDir: 'M:/GitHub/esia-pipeline',

  // ESIA Pipeline folder location
  pipelineFolder: 'M:/GitHub/esia-pipeline',

  // Main pipeline script - the ESIA pipeline uses run-esia-pipeline.py
  // This single script orchestrates the entire 3-step pipeline:
  // 1. Chunk PDF into semantic chunks with page tracking
  // 2. Extract domain-specific facts using archetype-based extraction
  // 3. Analyze extracted facts for consistency and compliance
  steps: [
    {
      id: 'full_pipeline',
      name: 'ESIA Full Pipeline',
      description: 'Run complete ESIA pipeline: chunking, extraction, and analysis',
      script: 'M:/GitHub/esia-pipeline/run-esia-pipeline.py',
      // Pass the PDF file path to the pipeline script
      // The script expects the PDF to be in data/pdf/ directory
      args: ['{PDF_FILE}'],
      timeout: 1800000, // 30 minutes - full pipeline takes time
    },
  ],

  // Output directory for processed files
  // All pipeline outputs are saved to a single local folder for simplified file management
  outputDir: './data/output',

  // Metadata directory for pipeline execution records
  metadataDir: './data/output/metadata',

  // Python executable (customize if needed)
  pythonExecutable: 'python',
  // pythonExecutable: 'python3',  // Use this on Linux/Mac
};

/**
 * Gets the script arguments for a pipeline step
 * Replaces placeholders with actual values
 */
export function getStepArgs(step, pdfFilename, sanitizedName) {
  const rootName = sanitizedName.replace(/\.[^/.]+$/, ''); // Remove extension

  return step.args.map(arg =>
    arg
      .replace('{PDF_FILE}', pdfFilename)
      .replace('{SANITIZED_NAME}', sanitizedName)
      .replace('{ROOT_NAME}', rootName)
  );
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
