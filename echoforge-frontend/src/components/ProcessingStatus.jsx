import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { uploadAPI } from '../services/api';

const ProcessingStatus = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let pollInterval;

    const fetchStatus = async () => {
      try {
        const response = await uploadAPI.getStatus(jobId);
        setStatus(response.data);

        if (response.data.status === 'completed' || response.data.status === 'failed') {
          clearInterval(pollInterval);
          if (response.data.status === 'completed') {
            setTimeout(() => navigate(`/results/${jobId}`), 2000);
          }
        }
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch status');
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    pollInterval = setInterval(fetchStatus, 2000);

    return () => clearInterval(pollInterval);
  }, [jobId, navigate]);

  const statusColors = {
    queued: 'bg-blue-100 text-blue-800',
    preprocessing: 'bg-yellow-100 text-yellow-800',
    diarization: 'bg-purple-100 text-purple-800',
    classification: 'bg-orange-100 text-orange-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-6">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold mb-8 text-gray-800">Processing Status</h2>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
              {error}
            </div>
          )}

          {status && (
            <div className="space-y-6">
              <div>
                <p className="text-sm text-gray-500 mb-2">Job ID</p>
                <p className="font-mono text-gray-800">{status.job_id}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-2">Status</p>
                <span className={`inline-block px-4 py-2 rounded-full font-semibold ${statusColors[status.status] || 'bg-gray-100'}`}>
                  {status.status.toUpperCase()}
                </span>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-2">Progress</p>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div
                    className="bg-indigo-600 h-4 rounded-full transition-all duration-300"
                    style={{ width: `${status.progress || 0}%` }}
                  ></div>
                </div>
                <p className="text-right mt-2 text-sm font-semibold text-gray-700">
                  {status.progress || 0}%
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-2">Current Stage</p>
                <p className="text-gray-800">{status.current_stage || 'Processing...'}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-2">Estimated Time Remaining</p>
                <p className="text-gray-800">
                  {status.estimated_time_remaining
                    ? `${Math.ceil(status.estimated_time_remaining / 60)} minutes`
                    : 'Calculating...'}
                </p>
              </div>

              {status.status === 'completed' && (
                <div className="mt-8 p-4 bg-green-50 border border-green-200 text-green-700 rounded">
                  Processing complete! Redirecting to results...
                </div>
              )}

              {status.status === 'failed' && (
                <div className="mt-8 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
                  <p className="font-semibold">Processing failed</p>
                  <p className="mt-2">{status.error_message || 'Unknown error'}</p>
                  <button
                    onClick={() => navigate('/')}
                    className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                  >
                    Try Again
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus;
