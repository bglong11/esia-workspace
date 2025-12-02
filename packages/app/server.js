import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { executePipeline, getPipelineStatus, getAllPipelineExecutions } from './pipelineExecutor.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

// Set UTF-8 charset for all JSON responses
app.use(express.json());
app.set('json spaces', 2);

// Middleware to set charset on all responses
app.use((req, res, next) => {
  const originalJson = res.json;
  res.json = function(data) {
    res.charset = 'utf-8';
    res.set('Content-Type', 'application/json; charset=utf-8');
    return originalJson.call(this, data);
  };
  next();
});

// Create data/pdf directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'data', 'pdf');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    // Generate filename with timestamp to avoid conflicts
    const timestamp = Date.now();
    const originalName = file.originalname;
    cb(null, `${timestamp}-${originalName}`);
  }
});

const fileFilter = (req, file, cb) => {
  // Only accept PDF files
  if (file.mimetype === 'application/pdf' || file.originalname.endsWith('.pdf')) {
    cb(null, true);
  } else {
    cb(new Error('Only PDF files are allowed'), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB limit
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Upload endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }

  try {
    // Start pipeline execution asynchronously WITHOUT awaiting
    // This allows the response to return immediately while pipeline runs in background
    const uploadedFilePath = req.file.path;

    // Generate execution ID that will be shared between server response and pipeline executor
    const executionId = `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    // Start pipeline in background (don't await) - pass executionId so it's consistent
    executePipeline(req.file.filename, uploadedFilePath, executionId).catch(error => {
      console.error(`[Pipeline] Background execution error for ${executionId}:`, error);
    });

    res.json({
      message: `File "${req.file.originalname}" uploaded successfully.`,
      filename: req.file.filename,
      size: req.file.size,
      path: `/data/pdf/${req.file.filename}`,
      pipeline: {
        executionId: executionId,
        status: 'running',
        sanitizedName: req.file.originalname.replace(/\.[^/.]+$/, '').toLowerCase().replace(/[^a-z0-9_-]/g, '_').replace(/_+/g, '_').replace(/^_+|_+$/g, ''),
      }
    });
  } catch (error) {
    res.status(500).json({
      message: 'Upload failed',
      filename: req.file.filename,
      error: error.message
    });
  }
});

// Error handling middleware for multer
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'FILE_TOO_LARGE') {
      return res.status(400).json({ message: 'File size exceeds 10MB limit' });
    }
    return res.status(400).json({ message: err.message });
  } else if (err) {
    return res.status(400).json({ message: err.message });
  }
  next();
});

// Pipeline status endpoint
app.get('/api/pipeline/:executionId', (req, res) => {
  const execution = getPipelineStatus(req.params.executionId);
  if (!execution) {
    return res.status(404).json({ message: 'Execution not found' });
  }
  res.json(execution);
});

// Pipeline history endpoint
app.get('/api/pipeline', (req, res) => {
  const executions = getAllPipelineExecutions();
  res.json({ executions });
});

// Download results endpoint - creates a zip file with all pipeline outputs
app.get('/api/download/:executionId', async (req, res) => {
  const execution = getPipelineStatus(req.params.executionId);
  if (!execution) {
    return res.status(404).json({ message: 'Execution not found' });
  }

  if (execution.status !== 'completed') {
    return res.status(400).json({ message: 'Pipeline not yet completed' });
  }

  try {
    // Dynamically import archiver
    const archiver = (await import('archiver')).default;

    // Set up response headers for zip download
    const zipFilename = `${execution.sanitizedName}_results.zip`;
    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', `attachment; filename="${zipFilename}"`);

    // Create archiver instance
    const archive = archiver('zip', {
      zlib: { level: 9 } // Maximum compression
    });

    // Handle archiver errors
    archive.on('error', (err) => {
      console.error('[Download] Archiver error:', err);
      res.status(500).json({ message: 'Error creating zip file', error: err.message });
    });

    // Pipe archive to response
    archive.pipe(res);

    // Define output directory (from pipeline config)
    const outputDir = path.resolve(__dirname, '../pipeline/data/outputs');

    // Add all output files for this execution
    // The pipeline uses pdfFilename (with timestamp) as the base for output files
    // Extract the base name: remove extension from pdfFilename
    const pdfBase = execution.pdfFilename.replace(/\.[^/.]+$/, '');

    // List of expected output files
    const outputFiles = [
      `${pdfBase}_chunks.jsonl`,
      `${pdfBase}_meta.json`,
      `${pdfBase}_facts.json`,
      `${pdfBase}_review.html`,
      `${pdfBase}_review.xlsx`,
    ];

    // Add each file if it exists
    for (const filename of outputFiles) {
      const filePath = path.join(outputDir, filename);
      if (fs.existsSync(filePath)) {
        archive.file(filePath, { name: filename });
        console.log(`[Download] Added to zip: ${filename}`);
      } else {
        console.warn(`[Download] File not found: ${filePath}`);
      }
    }

    // Finalize the archive
    await archive.finalize();
    console.log(`[Download] Zip file sent: ${zipFilename}`);
  } catch (error) {
    console.error('[Download] Error:', error);
    if (!res.headersSent) {
      res.status(500).json({ message: 'Error generating download', error: error.message });
    }
  }
});

// Serve static files from data/pdf (optional - to access uploaded files)
app.use('/data/pdf', express.static(uploadsDir));

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Uploads directory: ${uploadsDir}`);
  console.log(`API endpoints:`);
  console.log(`  POST /api/upload - Upload and process a PDF`);
  console.log(`  GET /api/pipeline/:executionId - Get pipeline execution status`);
  console.log(`  GET /api/pipeline - Get all pipeline executions`);
});
