import '../styles/globals.css';
import type { Metadata } from 'next';
import { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'AI Resume Tailoring Engine',
  description: 'Tailor your resume to any job description in seconds.',
};

const RootLayout = ({ children }: { children: ReactNode }) => {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <div className="min-h-screen flex justify-center px-4 py-10">
          <main className="w-full max-w-5xl space-y-8">{children}</main>
        </div>
      </body>
    </html>
  );
};

export default RootLayout;
