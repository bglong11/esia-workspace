"use client"; // This component uses client-side hooks like useState, useCallback, useRef

import React, { useState, useCallback, useRef, useEffect, ChangeEvent, DragEvent } from 'react';
import { uploadFile, getPipelineStatus } from '../services/apiService';
import { UploadStatus } from '../types';

interface FileUploadProps {
  onUploadComplete?: (message: string) => void;
  onUploadError?: (error: string) => void;
}

const MAX_FILE_SIZE_MB = 50;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024; // 50MB in bytes

interface PipelineStep {
  stepId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  name?: string;
  description?: string;
  output?: string;
  error?: string;
  progress?: { currentPage: number; totalPages: number };
}

interface PipelineStatus {
  id: string; // Backend returns 'id', not 'executionId'
  executionId?: string; // Keep for backward compatibility
  status: 'running' | 'completed' | 'failed';
  sanitizedName: string;
  steps: PipelineStep[];
  error?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete, onUploadError }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>(UploadStatus.IDLE);
  const [message, setMessage] = useState<string>('');
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [isDragActive, setIsDragActive] = useState<boolean>(false);
  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cancelUploadRef = useRef<(() => void) | null>(null);
  const pipelineCheckRef = useRef<NodeJS.Timeout | null>(null);

  const resetState = useCallback(() => {
    setSelectedFile(null);
    setMessage('');
    setUploadStatus(UploadStatus.IDLE);
    setUploadProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (cancelUploadRef.current) {
      cancelUploadRef.current(); // Ensure any ongoing upload is cancelled
      cancelUploadRef.current = null;
    }
  }, []);

  const processFile = useCallback((file: File | null) => {
    resetState(); // Reset state on new file selection or clear
    if (!file) {
      return false;
    }

    if (file.type !== 'application/pdf') {
      setUploadStatus(UploadStatus.ERROR);
      setMessage('Please select a PDF file.');
      return false;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      setUploadStatus(UploadStatus.ERROR);
      setMessage(`File size exceeds the limit of ${MAX_FILE_SIZE_MB}MB.`);
      return false;
    }

    setSelectedFile(file);
    setMessage(''); // Clear any previous error message
    return true;
  }, [resetState]);

  const handleFileChange = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      processFile(event.target.files[0]);
    } else {
      processFile(null); // Clear selected file if no file is chosen
    }
  }, [processFile]);

  const handleDragOver = useCallback((event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);
  }, []);

  const handleDrop = useCallback((event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      processFile(file);
    } else {
      processFile(null); // Clear selected file if no file is dropped
    }
  }, [processFile]);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setMessage('Please select a file first.');
      setUploadStatus(UploadStatus.ERROR);
      setUploadProgress(0);
      return;
    }

    setUploadStatus(UploadStatus.PENDING);
    setMessage('Uploading...');
    setUploadProgress(0);

    const { promise, cancel } = uploadFile(selectedFile, (progress) => {
      setUploadProgress(progress);
    });
    cancelUploadRef.current = cancel; // Store the cancel function

    try {
      const response = await promise;
      setUploadProgress(100);

      // If pipeline is available, start monitoring it
      if (response.pipeline) {
        setMessage('✓ PDF Successfully Uploaded');
        setUploadStatus(UploadStatus.PENDING); // Keep as PENDING while pipeline runs

        // Start polling for pipeline status immediately
        // Don't set initial hardcoded step structure - let the API provide the real structure
        console.log(`[FileUpload] Upload successful, execution ID:`, response.pipeline.executionId);
        monitorPipelineStatus(response.pipeline.executionId);
      } else {
        console.warn(`[FileUpload] Upload response missing pipeline info:`, response);
        setMessage(response.message);
        setUploadStatus(UploadStatus.SUCCESS);
        onUploadComplete?.(response.message);
      }
    } catch (error: any) {
      const errorMessage = error.message || 'An unknown error occurred during upload.';
      setMessage(errorMessage);
      setUploadStatus(UploadStatus.ERROR);
      onUploadError?.(errorMessage);
      setUploadProgress(0);
    } finally {
      cancelUploadRef.current = null;
      if (uploadStatus !== UploadStatus.ERROR) {
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }
    }
  }, [selectedFile, onUploadComplete, onUploadError, uploadStatus]);

  const handleCancelUpload = useCallback(() => {
    if (cancelUploadRef.current) {
      cancelUploadRef.current(); // Call the stored cancel function
    }
    resetState(); // Reset component state
    setMessage('Upload cancelled.');
    setUploadStatus(UploadStatus.IDLE); // Set status back to idle
  }, [resetState]);

  const monitorPipelineStatus = useCallback((executionId: string) => {
    setUploadStatus(UploadStatus.PENDING);

    // Clear any existing timeout
    if (pipelineCheckRef.current) {
      clearTimeout(pipelineCheckRef.current);
    }

    const checkPipelineStatus = async () => {
      try {
        const status = await getPipelineStatus(executionId);
        console.log(`[FileUpload] Pipeline status poll:`, status);
        setPipelineStatus(status);

        if (status.status === 'completed') {
          setMessage(`✓ Pipeline completed! Output: ${status.sanitizedName}`);
          setUploadStatus(UploadStatus.SUCCESS);
          onUploadComplete?.(`Pipeline completed. Root name: ${status.sanitizedName}`);
        } else if (status.status === 'failed') {
          const errorMsg = status.error || 'Unknown error';
          console.error(`[FileUpload] Pipeline failed with error:`, errorMsg);
          setMessage(`✗ Pipeline failed: ${errorMsg}`);
          setUploadStatus(UploadStatus.ERROR);
          onUploadError?.(`Pipeline failed: ${errorMsg}`);
        } else {
          // Still running, check again in 1 second
          console.log(`[FileUpload] Pipeline still running (status: ${status.status}), checking again in 1s`);
          pipelineCheckRef.current = setTimeout(checkPipelineStatus, 1000);
        }
      } catch (error: any) {
        console.error('Failed to check pipeline status:', error);
        // Continue checking even if fetch fails
        pipelineCheckRef.current = setTimeout(checkPipelineStatus, 2000);
      }
    };

    checkPipelineStatus();
  }, [onUploadComplete, onUploadError]);

  // Cleanup pipeline checker on unmount
  useEffect(() => {
    return () => {
      if (pipelineCheckRef.current) {
        clearTimeout(pipelineCheckRef.current);
      }
    };
  }, []);

  const getStatusClasses = (status: UploadStatus): string => {
    switch (status) {
      case UploadStatus.PENDING:
        return 'text-blue-600';
      case UploadStatus.SUCCESS:
        return 'text-green-600';
      case UploadStatus.ERROR:
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-xl w-full max-w-md sm:max-w-lg md:max-w-xl">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Upload PDF Document</h2>

      <div className="w-full mb-6">
        <label
          htmlFor="pdf-upload"
          className={`flex flex-col items-center justify-center w-full h-32 border-2 ${
            isDragActive ? 'border-blue-600 bg-blue-100' : 'border-blue-400 bg-blue-50'
          } border-dashed rounded-lg cursor-pointer hover:bg-blue-100 transition-colors duration-200`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          aria-label="Drag and drop PDF file or click to upload"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <svg
              className="w-8 h-8 mb-3 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M7 16a4 4 0 0 1-.88-7.903A5 0 0 1 15.9 6L16 6a5 5 0 0 1 1 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              ></path>
            </svg>
            <p className="mb-2 text-sm text-blue-700">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-blue-500">PDF files only (Max {MAX_FILE_SIZE_MB}MB)</p>
          </div>
          <input
            id="pdf-upload"
            type="file"
            className="hidden"
            accept=".pdf"
            onChange={handleFileChange}
            ref={fileInputRef}
          />
        </label>
      </div>

      {selectedFile && (
        <div className="w-full bg-gray-50 p-3 rounded-md flex items-center justify-between mb-6 border border-gray-200">
          <span className="text-sm text-gray-700 truncate">{selectedFile.name}</span>
          <button
            onClick={resetState} // Use resetState to clear file and input
            className="ml-4 p-1 text-red-500 hover:text-red-700 transition-colors duration-200"
            aria-label="Remove selected file"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>
      )}

      {/* Upload Progress Bar - Show while uploading or file uploaded */}
      {uploadStatus === UploadStatus.PENDING && uploadProgress < 100 && (
        <div className="w-full mb-6">
          {/* Progress label and percentage */}
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Uploading...
            </span>
            <span className="text-sm font-bold text-blue-600">{uploadProgress}%</span>
          </div>

          {/* Progress bar */}
          <div
            className="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-sm"
            role="progressbar"
            aria-valuenow={uploadProgress}
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="Upload progress"
          >
            <div
              className="h-3 rounded-full transition-all duration-300 ease-out bg-gradient-to-r from-blue-500 to-blue-600"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>

          {/* File size info */}
          <p className="text-xs text-gray-500 mt-2 text-center">
            {selectedFile ? (selectedFile.size / (1024 * 1024)).toFixed(2) : '0'} MB file
          </p>
        </div>
      )}

      {/* Upload Complete Progress Bar - Show brief completion state */}
      {uploadStatus === UploadStatus.PENDING && uploadProgress === 100 && !pipelineStatus && (
        <div className="w-full mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Upload Complete</span>
            <span className="text-sm font-bold text-green-600">100%</span>
          </div>

          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-sm">
            <div className="h-3 rounded-full bg-gradient-to-r from-green-500 to-green-600 w-full"></div>
          </div>

          <p className="text-xs text-gray-500 mt-2 text-center">
            Starting pipeline processing...
          </p>
        </div>
      )}

      {/* Upload Button - Only show if not uploading or not waiting for pipeline */}
      {!pipelineStatus && (
        <div className="flex w-full gap-4">
          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploadStatus === UploadStatus.PENDING}
            className={`flex-1 px-6 py-3 text-lg font-medium rounded-lg transition-colors duration-300 ${
              !selectedFile || uploadStatus === UploadStatus.PENDING
                ? 'bg-blue-300 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md'
            }`}
          >
            {uploadStatus === UploadStatus.PENDING && uploadProgress < 100 ? (
              <span className="flex items-center justify-center">
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 0 0 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Uploading...
              </span>
            ) : (
              'Upload File'
            )}
          </button>

          {uploadStatus === UploadStatus.PENDING && uploadProgress < 100 && (
            <button
              onClick={handleCancelUpload}
              className="flex-1 px-6 py-3 text-lg font-medium rounded-lg bg-red-500 hover:bg-red-600 text-white shadow-md transition-colors duration-300"
            >
              Cancel Upload
            </button>
          )}
        </div>
      )}

      {message && (
        <div className="w-full mt-4 p-3 rounded-md border">
          <p className={`text-sm font-medium ${getStatusClasses(uploadStatus)}`}>
            {message}
          </p>
          {uploadStatus === UploadStatus.PENDING && pipelineStatus && pipelineStatus.status === 'running' && (
            <p className="text-xs text-blue-600 mt-2 flex items-center gap-2">
              <svg
                className="w-4 h-4 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 0 0 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {/* Show current running step name */}
              {pipelineStatus.steps.find(s => s.status === 'running')?.name || 'Processing...'}
            </p>
          )}
        </div>
      )}

      {/* Pipeline Steps Progress */}
      {pipelineStatus && pipelineStatus.steps.length > 0 && (
        <div className="w-full mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-semibold text-gray-800 mb-4">Pipeline Processing</h3>

          <div className="space-y-3">
            {pipelineStatus.steps.map((step, idx) => (
              <div key={step.stepId} className="flex items-start gap-3">
                {/* Step number and status icon */}
                <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-medium text-sm">
                  {step.status === 'completed' ? (
                    <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                      <svg
                        className="w-5 h-5 text-green-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                  ) : step.status === 'running' ? (
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                      <svg
                        className="w-5 h-5 text-blue-600 animate-spin"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <circle className="opacity-25" cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                    </div>
                  ) : step.status === 'failed' ? (
                    <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center">
                      <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
                      {idx + 1}
                    </div>
                  )}
                </div>

                {/* Step info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium text-gray-800">
                      {step.name || `Step ${idx + 1}`}
                    </h4>
                    <span className="text-xs font-medium">
                      {step.status === 'completed' && (
                        <span className="text-green-600">Complete</span>
                      )}
                      {step.status === 'running' && (
                        <span className="text-blue-600">Running</span>
                      )}
                      {step.status === 'failed' && (
                        <span className="text-red-600">Failed</span>
                      )}
                      {step.status === 'pending' && (
                        <span className="text-gray-500">Pending</span>
                      )}
                    </span>
                  </div>
                  {step.description && (
                    <p className="text-xs text-gray-600 mt-1 whitespace-pre-line">{step.description}</p>
                  )}
                  {step.status === 'running' && step.progress && (
                    <p className="text-xs text-blue-600 mt-1 font-medium">
                      Processing page {step.progress.currentPage} of {step.progress.totalPages}
                    </p>
                  )}
                  {step.status === 'running' && !step.progress && (
                    <p className="text-xs text-blue-600 mt-1 font-medium animate-pulse">
                      Processing... Please wait
                    </p>
                  )}
                  {step.status === 'running' && (
                    <div className="mt-2 w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-400 to-blue-600 animate-pulse rounded-full"></div>
                    </div>
                  )}
                  {step.error && (
                    <p className="text-xs text-red-600 mt-1 font-medium">{step.error}</p>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Overall progress indicator */}
          {pipelineStatus.status === 'running' && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-gray-700">Overall Progress</span>
                <span className="text-xs font-bold text-blue-600">
                  {Math.round(
                    (pipelineStatus.steps.filter((s) => s.status === 'completed').length /
                      pipelineStatus.steps.length) *
                      100
                  )}
                  %
                </span>
              </div>
              <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500"
                  style={{
                    width: `${
                      (pipelineStatus.steps.filter((s) => s.status === 'completed').length /
                        pipelineStatus.steps.length) *
                      100
                    }%`,
                  }}
                ></div>
              </div>
            </div>
          )}

          {/* Download Results Button - Only show when pipeline is complete */}
          {pipelineStatus.status === 'completed' && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <button
                type="button"
                onClick={() => {
                  const executionId = pipelineStatus.id || pipelineStatus.executionId;
                  window.location.href = `/api/download/${executionId}`;
                }}
                className="w-full px-6 py-3 text-lg font-medium rounded-lg bg-green-600 hover:bg-green-700 text-white shadow-md transition-colors duration-300 flex items-center justify-center gap-2"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  ></path>
                </svg>
                Download Results
              </button>
              <p className="text-xs text-gray-500 mt-2 text-center">
                Download chunks, facts, analysis report, and Excel summary
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FileUpload;