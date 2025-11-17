'use client';

import { ChangeEvent, useState } from 'react';
import LoadingSpinner from './LoadingSpinner';
import api from '../utils/apiClient';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [statusType, setStatusType] = useState<'idle' | 'success' | 'error'>('idle');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setStatusMessage('');
    setStatusType('idle');
  };

  const uploadResume = async () => {
    if (!selectedFile) {
      setStatusMessage('Please select a file first.');
      setStatusType('error');
      return;
    }

    const formData = new FormData();
    formData.append('resume', selectedFile);

    setIsUploading(true);
    setStatusMessage('');
    setStatusType('idle');

    try {
      await api.post('/upload-resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatusMessage('Uploaded successfully');
      setStatusType('success');
    } catch (error) {
      console.error('Failed to upload resume', error);
      setStatusMessage('Upload failed. Please try again.');
      setStatusType('error');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">
      <div className="space-y-2">
        <h2 className="text-xl font-semibold text-gray-900">Upload Resume</h2>
        <p className="text-sm text-gray-600">Attach your latest resume to get the most accurate tailoring.</p>
      </div>

      <div className="mt-4 space-y-3">
        <label className="flex cursor-pointer items-center justify-between rounded-lg border border-dashed border-gray-200 bg-gray-50 px-4 py-3 text-sm font-medium text-gray-700 transition hover:border-blue-200 hover:bg-white">
          <span>{selectedFile ? selectedFile.name : 'Choose a file (.pdf, .doc, .docx, .txt)'}</span>
          <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleFileChange} className="hidden" />
          <span className="rounded-md border border-gray-200 bg-white px-3 py-1 text-xs font-semibold text-blue-600 shadow-sm">Browse</span>
        </label>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={uploadResume}
            disabled={isUploading}
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isUploading && <LoadingSpinner />}
            <span>{isUploading ? 'Uploading...' : 'Upload Resume'}</span>
          </button>
          {statusMessage && (
            <span
              className={`text-sm ${
                statusType === 'success'
                  ? 'text-blue-700'
                  : statusType === 'error'
                  ? 'text-blue-900'
                  : 'text-gray-600'
              }`}
            >
              {statusMessage}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
