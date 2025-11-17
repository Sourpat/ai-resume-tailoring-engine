'use client';

import { useState } from 'react';
import LoadingSpinner from './LoadingSpinner';
import api from '../utils/apiClient';

interface ExportButtonsProps {
  sections: {
    product_owner?: string[];
    business_analyst?: string[];
    technical_ba?: string[];
    [key: string]: any;
  };
}

const downloadFile = (base64Data: string, filename: string, mimeType: string) => {
  const byteCharacters = atob(base64Data);
  const byteNumbers = new Array(byteCharacters.length).fill(0).map((_, i) => byteCharacters.charCodeAt(i));
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], { type: mimeType });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  window.URL.revokeObjectURL(url);
};

const ExportButtons = ({ sections }: ExportButtonsProps) => {
  const [loadingFormat, setLoadingFormat] = useState<'pdf' | 'docx' | 'md' | null>(null);

  const exportResume = async (format: 'pdf' | 'docx' | 'md') => {
    setLoadingFormat(format);
    try {
      const response = await api.post(
        '/export',
        { sections, format },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      const base64File = response.data?.file || response.data?.data || response.data;
      if (!base64File || typeof base64File !== 'string') {
        throw new Error('No file content returned.');
      }

      const mimeType =
        format === 'pdf'
          ? 'application/pdf'
          : format === 'docx'
          ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
          : 'text/markdown';
      const filename =
        format === 'pdf'
          ? 'tailored_resume.pdf'
          : format === 'docx'
          ? 'tailored_resume.docx'
          : 'tailored_resume.md';

      downloadFile(base64File, filename, mimeType);
    } catch (error) {
      console.error('Failed to export resume', error);
      alert('Export failed. Please try again.');
    } finally {
      setLoadingFormat(null);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-3">
      {(
        [
          { format: 'pdf', label: 'Download PDF' },
          { format: 'docx', label: 'Download DOCX' },
          { format: 'md', label: 'Download Markdown' },
        ] as const
      ).map(({ format, label }) => (
        <button
          key={format}
          type="button"
          onClick={() => exportResume(format)}
          disabled={loadingFormat === format}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loadingFormat === format && <LoadingSpinner />}
          <span>{loadingFormat === format ? 'Loading...' : label}</span>
        </button>
      ))}
    </div>
  );
};

export default ExportButtons;
