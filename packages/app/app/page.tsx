"use client"; // This component uses client-side hooks like useState and useCallback

import React, { useCallback, useState } from 'react';
import FileUpload from '../components/FileUpload'; // Updated path

const Home: React.FC = () => {
  const [globalMessage, setGlobalMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');

  const handleUploadComplete = useCallback((message: string) => {
    setGlobalMessage(message);
    setMessageType('success');
    setTimeout(() => setGlobalMessage(''), 5000); // Clear message after 5 seconds
  }, []);

  const handleUploadError = useCallback((error: string) => {
    setGlobalMessage(error);
    setMessageType('error');
    setTimeout(() => setGlobalMessage(''), 5000); // Clear message after 5 seconds
  }, []);

  const getMessageClasses = (type: 'success' | 'error' | ''): string => {
    switch (type) {
      case 'success':
        return 'bg-green-100 text-green-800 border-green-400';
      case 'error':
        return 'bg-red-100 text-red-800 border-red-400';
      default:
        return 'hidden';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full max-w-2xl mx-auto p-4 md:p-8">
      <header className="mb-8 md:mb-12 text-center">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-800 leading-tight">
          ESIA.ai
        </h1>
        <p className="mt-3 text-lg sm:text-xl text-gray-600">
          Intelligent Environmental Impact Assessment
        </p>
      </header>

      {globalMessage && (
        <div
          className={`w-full max-w-md sm:max-w-lg md:max-w-xl p-4 mb-6 rounded-md border text-center ${getMessageClasses(messageType)}`}
          role="alert"
        >
          {globalMessage}
        </div>
      )}

      <FileUpload onUploadComplete={handleUploadComplete} onUploadError={handleUploadError} />
    </div>
  );
};

export default Home;