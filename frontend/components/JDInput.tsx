'use client';

import { ChangeEvent, useEffect, useState } from 'react';

interface JDInputProps {
  onChange?: (value: string) => void;
  initialValue?: string;
}

const JDInput = ({ onChange, initialValue = '' }: JDInputProps) => {
  const [jdText, setJdText] = useState(initialValue);

  useEffect(() => {
    if (onChange) {
      onChange(jdText);
    }
  }, [jdText, onChange]);

  const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setJdText(event.target.value);
  };

  return (
    <div className="space-y-2">
      <label htmlFor="jd-text" className="text-sm font-semibold text-gray-800">
        Job Description
      </label>
      <textarea
        id="jd-text"
        value={jdText}
        onChange={handleChange}
        rows={8}
        placeholder="Paste the job description here"
        className="w-full rounded-lg border border-gray-200 bg-white p-3 text-sm text-gray-800 shadow-sm focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-200"
      />
      <p className="text-xs text-gray-500">Include responsibilities, requirements, and preferred skills.</p>
    </div>
  );
};

export default JDInput;
