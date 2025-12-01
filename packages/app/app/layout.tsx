import './globals.css';
import React from 'react';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-gray-100 flex items-center justify-center min-h-screen p-4">
      {children}
    </div>
  );
}