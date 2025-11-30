/**
 * Shared utility functions across ESIA packages
 */

export function sanitizeFilename(filename: string): string {
  return filename
    .toLowerCase()
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_.-]/g, '')
    .replace(/_{2,}/g, '_');
}

export function generateExecutionId(pdfFilename: string): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  return `exec-${timestamp}-${random}`;
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export function createTimestampedFilename(originalName: string): string {
  const timestamp = Date.now();
  const sanitized = sanitizeFilename(originalName.replace(/\.[^.]+$/, ''));
  return `${timestamp}-${sanitized}`;
}

export function getFileExtension(filename: string): string {
  const match = filename.match(/\.[^.]+$/);
  return match ? match[0].toLowerCase() : '';
}

export async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
