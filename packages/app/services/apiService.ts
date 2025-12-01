export interface UploadResponse {
  message: string;
  filename: string;
  size: number;
  path: string;
  pipeline?: {
    executionId: string;
    status: string;
    sanitizedName: string;
  };
}

/**
 * Uploads a file to the backend API.
 * @param file The File object to upload.
 * @param onProgress Callback to report upload progress (0-100).
 * @returns An object containing a Promise that resolves with the response or rejects with an error, and a cancel function.
 */
export const uploadFile = (file: File, onProgress?: (progress: number) => void): { promise: Promise<UploadResponse>; cancel: () => void } => {
  const controller = new AbortController();

  const promise = new Promise<UploadResponse>((resolve, reject) => {
    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100);
        onProgress?.(percentComplete);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText) as UploadResponse;
          resolve(response);
        } catch {
          resolve({
            message: `File "${file.name}" uploaded successfully.`,
            filename: file.name,
            size: file.size,
            path: `/data/pdfs/${file.name}`,
          });
        }
      } else {
        reject(new Error(`Upload failed with status ${xhr.status}`));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Network error during upload'));
    });

    xhr.addEventListener('abort', () => {
      reject(new Error('Upload cancelled.'));
    });

    xhr.open('POST', '/api/upload');
    xhr.send(formData);

    controller.signal.addEventListener('abort', () => {
      xhr.abort();
    });
  });

  const cancel = () => {
    controller.abort();
  };

  return { promise, cancel };
};

/**
 * Fetches the status of a pipeline execution
 */
export const getPipelineStatus = async (executionId: string) => {
  const response = await fetch(`/api/pipeline/${executionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch pipeline status: ${response.statusText}`);
  }
  return response.json();
};