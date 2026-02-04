import React from 'react';
import UploadSection from '../components/UploadSection';

const DashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-12">
        <div className="container mx-auto px-6">
          <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
          <p className="text-indigo-100">Process your audio files with advanced speaker diarization</p>
        </div>
      </div>
      <UploadSection />
    </div>
  );
};

export default DashboardPage;
