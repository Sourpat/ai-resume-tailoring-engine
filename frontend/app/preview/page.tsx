'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import ResumePreview from '../../components/ResumePreview';

interface TailoredSections {
  product_owner?: string[];
  business_analyst?: string[];
  technical_ba?: string[];
  [key: string]: any;
}

const PreviewPage = () => {
  const [sections, setSections] = useState<TailoredSections | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const encodedState = params.get('state');
    if (!encodedState) return;

    try {
      const decoded = JSON.parse(decodeURIComponent(encodedState));
      setSections(decoded);
    } catch (err) {
      console.error('Unable to parse preview state', err);
      setError('Unable to load preview data from URL.');
    }
  }, []);

  useEffect(() => {
    if (sections) return;

    try {
      const stored = localStorage.getItem('tailoredResult');
      if (stored) {
        setSections(JSON.parse(stored));
      }
    } catch (err) {
      console.error('Unable to read stored tailored result', err);
      setError('Unable to load saved tailored result.');
    }
  }, [sections]);

  return (
    <main className="space-y-6 rounded-2xl border bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tailored Resume Preview</h1>
          <p className="text-sm text-gray-600">Review the tailored content by role specialization.</p>
        </div>
        <Link
          href="/"
          className="inline-flex items-center justify-center rounded-lg border border-gray-200 px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-100"
        >
          ← Back to editor
        </Link>
      </div>

      {error && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">{error}</div>
      )}

      {sections ? (
        <ResumePreview sections={sections} />
      ) : (
        <p className="text-sm text-gray-600">No tailored resume data found.</p>
      )}
    </main>
  );
};

export default PreviewPage;
