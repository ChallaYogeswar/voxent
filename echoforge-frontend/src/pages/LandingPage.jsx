import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Hero from '../components/Hero';

const LandingPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  if (user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
        <Hero />
        <div className="container mx-auto px-6 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Ready to Process Audio?
            </h2>
            <p className="text-lg text-gray-600">
              Upload your audio files and start speaker diarization instantly
            </p>
          </div>
          <div className="flex flex-col md:flex-row gap-6 justify-center">
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Hero />
      <div className="container mx-auto px-6 py-16">
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-4xl mb-4">🎙️</div>
            <h3 className="text-xl font-bold mb-2">Upload Audio</h3>
            <p className="text-gray-600">
              Support for multiple audio formats with up to 500MB file size
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold mb-2">AI Powered</h3>
            <p className="text-gray-600">
              Advanced machine learning algorithms for accurate speaker separation
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Detailed Analytics</h3>
            <p className="text-gray-600">
              Get comprehensive metrics and visualization of speaker patterns
            </p>
          </div>
        </div>

        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Get Started Today</h2>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              Sign Up Now
            </Link>
            <Link
              to="/login"
              className="bg-white hover:bg-gray-100 text-indigo-600 border-2 border-indigo-600 px-8 py-3 rounded-lg font-semibold transition"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
