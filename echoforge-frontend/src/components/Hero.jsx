import React from 'react';

const Hero = () => {
  return (
    <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-20">
      <div className="container mx-auto px-6 text-center">
        <h1 className="text-5xl font-bold mb-4">Welcome to EchoForge</h1>
        <p className="text-xl text-indigo-100 mb-8">
          Advanced Speaker Diarization Platform - Separate voices with AI precision
        </p>
        <p className="text-lg text-indigo-200">
          Upload audio files and instantly identify, separate, and analyze multiple speakers
        </p>
      </div>
    </div>
  );
};

export default Hero;
