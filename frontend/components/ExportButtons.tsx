'use client';

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
  const exportResume = async (format: 'pdf' | 'docx' | 'md') => {
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
        format === 'pdf' ? 'application/pdf' : format === 'docx' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 'text/markdown';
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
    }
  };

  return (
    <div>
      <button type="button" onClick={() => exportResume('pdf')}>
        Download PDF
      </button>
      <button type="button" onClick={() => exportResume('docx')}>
        Download DOCX
      </button>
      <button type="button" onClick={() => exportResume('md')}>
        Download Markdown
      </button>
    </div>
  );
};

export default ExportButtons;
