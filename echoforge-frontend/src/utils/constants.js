// Constants
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const SUPPORTED_FORMATS = ['audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/flac'];

export const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB

export const STATUS_VALUES = {
  QUEUED: 'queued',
  PREPROCESSING: 'preprocessing',
  DIARIZATION: 'diarization',
  CLASSIFICATION: 'classification',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

export const POLLING_INTERVAL = 2000; // 2 seconds

export const POLLING_TIMEOUT = 5 * 60 * 1000; // 5 minutes
