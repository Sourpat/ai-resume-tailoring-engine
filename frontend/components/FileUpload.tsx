'use client';

import { ChangeEvent, useState } from 'react';
import api from '../utils/apiClient';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setStatusMessage('');
  };

  const uploadResume = async () => {
    if (!selectedFile) {
      setStatusMessage('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
      await api.post('/upload-resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatusMessage('Uploaded successfully');
    } catch (error) {
      console.error('Failed to upload resume', error);
      setStatusMessage('Upload failed');
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleFileChange} />
      <button type="button" onClick={uploadResume}>
        Upload Resume
      </button>
      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
};

export default FileUpload;
