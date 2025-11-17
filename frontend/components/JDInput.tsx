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
    <div>
      <label htmlFor="jd-text">Job Description</label>
      <textarea
        id="jd-text"
        value={jdText}
        onChange={handleChange}
        rows={6}
        placeholder="Paste the job description here"
      />
    </div>
  );
};

export default JDInput;
