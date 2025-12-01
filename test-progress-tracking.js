import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const PDF_PATH = 'M:\\GitHub\\esia-workspace\\packages\\app\\data\\pdf\\1764581680665-ESIA Report Final Elang AMNT_as submitted V.07.pdf';
const API_URL = 'http://localhost:5001';

async function testProgressTracking() {
  try {
    console.log('Starting progress tracking test...\n');

    // 1. Upload file using curl
    console.log('1. Uploading PDF...');
    const uploadCmd = `curl -s -X POST -F "file=@${PDF_PATH}" ${API_URL}/api/upload`;
    const uploadOutput = execSync(uploadCmd, { encoding: 'utf-8' });
    const uploadData = JSON.parse(uploadOutput);
    const executionId = uploadData.pipeline.executionId;
    console.log(`   Upload successful! Execution ID: ${executionId}\n`);

    // 2. Poll for status updates
    console.log('2. Monitoring pipeline progress...\n');
    let previousStatus = null;
    let progressUpdates = [];
    let pollCount = 0;
    const maxPolls = 150; // 5 minutes at 2-second intervals

    const pollInterval = setInterval(() => {
      try {
        pollCount++;
        const statusCmd = `curl -s ${API_URL}/api/pipeline/${executionId}`;
        const statusOutput = execSync(statusCmd, { encoding: 'utf-8' });
        const status = JSON.parse(statusOutput);

        if (!status || !status.steps) {
          return;
        }

        const step = status.steps[0];
        const currentStatus = `${status.status} | Step: ${step.status}`;

        if (currentStatus !== previousStatus || (step.progress && step.progress.currentPage)) {
          previousStatus = currentStatus;

          console.log(`\n[${new Date().toLocaleTimeString()}]`);
          console.log(`  Pipeline: ${status.status}`);
          console.log(`  Step: ${step.name} (${step.status})`);

          if (step.progress) {
            const progress = `Page ${step.progress.currentPage} of ${step.progress.totalPages}`;
            console.log(`  Progress: ${progress}`);
            progressUpdates.push(progress);
          } else if (step.status === 'running') {
            console.log(`  Progress: Waiting for progress update...`);
          }
        }

        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(pollInterval);
          console.log(`\n✓ Pipeline ${status.status}!`);
          console.log(`\nProgress updates received: ${progressUpdates.length}`);
          if (progressUpdates.length > 0) {
            console.log(`Latest: ${progressUpdates[progressUpdates.length - 1]}`);
          }
          process.exit(0);
        }

        if (pollCount >= maxPolls) {
          clearInterval(pollInterval);
          console.log('\n✗ Test timeout - pipeline did not complete within 5 minutes');
          process.exit(1);
        }
      } catch (error) {
        console.error('Polling error:', error.message);
      }
    }, 2000);
  } catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
  }
}

testProgressTracking();
