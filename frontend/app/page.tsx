'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import ExportButtons from '../components/ExportButtons';
import FileUpload from '../components/FileUpload';
import JDInput from '../components/JDInput';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../utils/apiClient';

const HomePage = () => {
  const [jdText, setJdText] = useState('');
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [error, setError] = useState('');
  const [isTailoring, setIsTailoring] = useState(false);

  useEffect(() => {
    if (apiResponse) {
      localStorage.setItem('tailoredResult', JSON.stringify(apiResponse));
    }
  }, [apiResponse]);

  const tailorResume = async () => {
    setError('');
    if (!jdText.trim()) {
      setError('Please add a job description before tailoring.');
      return;
    }

    setIsTailoring(true);
    try {
      const response = await api.post('/tailor', { jd_text: jdText });
      setApiResponse(response.data);
    } catch (err) {
      console.error('Tailoring failed', err);
      setError('Unable to tailor resume at this time.');
    } finally {
      setIsTailoring(false);
    }
  };

  return (
    <main className="space-y-8">
      <header className="space-y-3 text-center md:text-left">
        <p className="text-sm font-semibold uppercase tracking-wide text-blue-600">Tailored precision</p>
        <h1 className="text-3xl font-bold text-gray-900">AI Resume Tailoring Engine</h1>
        <p className="text-gray-600">
          Upload your resume, paste the job description, and generate a tailored version in seconds.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-2">
        <FileUpload />

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-gray-900">Paste Job Description</h2>
            <p className="text-sm text-gray-600">
              Provide the role details so we can align your experience to what matters most.
            </p>
          </div>
          <div className="mt-4">
            <JDInput onChange={setJdText} />
          </div>
        </div>
      </div>

      <div className="rounded-2xl border bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="space-y-1">
            <h2 className="text-xl font-semibold text-gray-900">Generate tailored resume</h2>
            <p className="text-sm text-gray-600">We will prepare role-specific bullet points for you.</p>
          </div>
          <button
            type="button"
            onClick={tailorResume}
            disabled={isTailoring}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isTailoring && <LoadingSpinner />}
            <span>{isTailoring ? 'Tailoring...' : 'Tailor Resume'}</span>
          </button>
        </div>

        {error && (
          <div className="mt-4 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
            {error}
          </div>
        )}

        {apiResponse && (
          <div className="mt-6 space-y-4">
            <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
              Resume generated — continue to Preview page.
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <Link
                href="/preview"
                className="inline-flex items-center justify-center rounded-lg border border-blue-100 bg-white px-4 py-2 text-sm font-semibold text-blue-600 shadow-sm transition hover:bg-blue-50"
              >
                Go to Preview
              </Link>
              <ExportButtons sections={apiResponse} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
};

export default HomePage;
