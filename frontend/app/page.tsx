'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import ExportButtons from '../components/ExportButtons';
import FileUpload from '../components/FileUpload';
import JDInput from '../components/JDInput';
import api from '../utils/apiClient';

const HomePage = () => {
  const [jdText, setJdText] = useState('');
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (apiResponse) {
      localStorage.setItem('tailoredResult', JSON.stringify(apiResponse));
    }
  }, [apiResponse]);

  const tailorResume = async () => {
    setError('');
    if (!jdText) {
      setError('Please add a job description before tailoring.');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/tailor', { jd_text: jdText });
      setApiResponse(response.data);
    } catch (err) {
      console.error('Tailoring failed', err);
      setError('Unable to tailor resume at this time.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h1>AI Resume Tailoring Engine</h1>
      <section>
        <h2>Upload Resume</h2>
        <FileUpload />
      </section>

      <section>
        <JDInput onChange={setJdText} />
      </section>

      <button type="button" onClick={tailorResume} disabled={loading}>
        {loading ? 'Tailoring...' : 'Tailor Resume'}
      </button>

      {error && <p>{error}</p>}

      {apiResponse && (
        <section>
          <h2>Tailored Result</h2>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
          <ExportButtons sections={apiResponse} />
          <div>
            <Link href="/preview">Go to preview page</Link>
          </div>
        </section>
      )}
    </main>
  );
};

export default HomePage;
