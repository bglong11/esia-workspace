#!/usr/bin/env node

/**
 * Test script to verify CUDA environment variables are passed to Python subprocess
 */

const { spawn } = require('child_process');
const path = require('path');

const pythonExe = path.resolve('packages/pipeline/venv312/Scripts/python.exe');

// Test Python script that prints environment variables
const testScript = `
import os
import sys

print("CUDA_VISIBLE_DEVICES:", os.environ.get('CUDA_VISIBLE_DEVICES', 'NOT SET'))
print("TORCH_DEVICE:", os.environ.get('TORCH_DEVICE', 'NOT SET'))
print("PYTHONIOENCODING:", os.environ.get('PYTHONIOENCODING', 'NOT SET'))

# Try importing torch to see if CUDA is disabled
try:
    import torch
    print("PyTorch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("WARNING: CUDA is still available despite CUDA_VISIBLE_DEVICES being empty!")
    else:
        print("✓ CUDA is correctly disabled")
except Exception as e:
    print("Error importing PyTorch:", e)
`;

console.log('Testing CUDA environment variable passing...\n');

const child = spawn(pythonExe, ['-c', testScript], {
  env: {
    ...process.env,
    PYTHONIOENCODING: 'utf-8',
    PYTHONUNBUFFERED: '1',
    CUDA_VISIBLE_DEVICES: '',
    TORCH_DEVICE: 'cpu',
  },
});

let output = '';

child.stdout.on('data', (data) => {
  output += data.toString();
  process.stdout.write(data);
});

child.stderr.on('data', (data) => {
  process.stderr.write(data);
});

child.on('close', (code) => {
  console.log('\n\nTest completed with exit code:', code);

  if (output.includes('CUDA_VISIBLE_DEVICES: ') && output.includes('TORCH_DEVICE: cpu')) {
    console.log('✓ Environment variables are being passed correctly!');
  } else {
    console.log('✗ Environment variables may not be passed correctly');
  }
});
