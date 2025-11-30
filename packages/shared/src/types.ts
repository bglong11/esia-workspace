/**
 * Shared types across ESIA packages
 */

export interface ESIADocument {
  id: string;
  filename: string;
  path: string;
  uploadedAt: Date;
  size: number;
}

export interface PipelineExecution {
  id: string;
  documentId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  startTime: Date;
  endTime?: Date;
  steps: PipelineStep[];
  error?: string;
}

export interface PipelineStep {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: Record<string, any>;
  error?: string;
}

export interface ExtractedFact {
  id: string;
  type: string;
  value: string;
  source: string;
  confidence: number;
  pageNumber?: number;
}

export interface AnalysisResult {
  documentId: string;
  executionId: string;
  facts: ExtractedFact[];
  issues: AnalysisIssue[];
  summary: string;
}

export interface AnalysisIssue {
  id: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  affectedFacts: string[];
}
