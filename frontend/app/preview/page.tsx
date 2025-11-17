'use client';

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';

interface TailoredSections {
  product_owner?: string[];
  business_analyst?: string[];
  technical_ba?: string[];
  [key: string]: any;
}

const PreviewPage = () => {
  const searchParams = useSearchParams();
  const encodedState = searchParams.get('state');
  const [sections, setSections] = useState<TailoredSections | null>(null);

  const decodedState = useMemo(() => {
    if (!encodedState) return null;
    try {
      return JSON.parse(decodeURIComponent(encodedState));
    } catch (error) {
      console.error('Unable to parse preview state', error);
      return null;
    }
  }, [encodedState]);

  useEffect(() => {
    if (decodedState) {
      setSections(decodedState);
      return;
    }

    try {
      const stored = localStorage.getItem('tailoredResult');
      if (stored) {
        setSections(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Unable to read stored tailored result', error);
    }
  }, [decodedState]);

  const renderSection = (title: string, items?: string[]) => (
    <section>
      <h2>{title}</h2>
      {items && items.length > 0 ? (
        <ul>
          {items.map((item, index) => (
            <li key={`${title}-${index}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>No {title.toLowerCase()} content available.</p>
      )}
    </section>
  );

  return (
    <main>
      <h1>Tailored Resume Preview</h1>
      {sections ? (
        <div>
          {renderSection('Product Owner', sections.product_owner)}
          {renderSection('Business Analyst', sections.business_analyst)}
          {renderSection('Technical BA', sections.technical_ba)}
        </div>
      ) : (
        <p>No tailored resume data found.</p>
      )}
    </main>
  );
};

export default PreviewPage;
