import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { uploadAPI, downloadAPI } from '../services/api';

const ResultsDisplay = () => {
  const { jobId } = useParams();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await uploadAPI.getStatus(jobId);
        setResults(response.data);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch results');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [jobId]);

  const handleDownloadSpeaker = async (speakerId) => {
    setDownloading(speakerId);
    try {
      const response = await downloadAPI.getSpeakerAudio(jobId, speakerId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${speakerId}.wav`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError('Download failed');
    } finally {
      setDownloading(null);
    }
  };

  const handleDownloadMetadata = async () => {
    try {
      const response = await downloadAPI.getMetadata(jobId);
      const url = window.URL.createObjectURL(
        new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
      );
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'metadata.json');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError('Download failed');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-6">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
            {error}
          </div>
        )}

        {results && (
          <div className="space-y-8">
            {/* Summary Section */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">Processing Results</h2>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-indigo-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Duration</p>
                  <p className="text-2xl font-bold text-indigo-600">
                    {Math.round(results.duration || 0)}s
                  </p>
                </div>
                <div className="bg-purple-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Speakers Found</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {results.speakers?.length || 0}
                  </p>
                </div>
                <div className="bg-orange-50 p-4 rounded">
                  <p className="text-sm text-gray-600">DER Score</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {(results.der_score || 0).toFixed(2)}%
                  </p>
                </div>
                <div className="bg-green-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Processing Time</p>
                  <p className="text-2xl font-bold text-green-600">
                    {(results.processing_time || 0).toFixed(1)}s
                  </p>
                </div>
              </div>
            </div>

            {/* Speakers Section */}
            {results.speakers && results.speakers.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-2xl font-bold mb-6 text-gray-800">Speakers</h3>
                <div className="space-y-4">
                  {results.speakers.map((speaker, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h4 className="text-lg font-semibold text-gray-800">
                            {speaker.speaker_id}
                          </h4>
                          <p className="text-sm text-gray-600">
                            Talk Time: {(speaker.total_duration || 0).toFixed(1)}s
                          </p>
                        </div>
                        <button
                          onClick={() => handleDownloadSpeaker(speaker.speaker_id)}
                          disabled={downloading === speaker.speaker_id}
                          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white px-4 py-2 rounded transition"
                        >
                          {downloading === speaker.speaker_id ? 'Downloading...' : 'Download Audio'}
                        </button>
                      </div>

                      {speaker.segments && speaker.segments.length > 0 && (
                        <div className="mt-4 bg-gray-50 p-4 rounded">
                          <p className="text-sm font-semibold text-gray-700 mb-2">
                            Segments ({speaker.segments.length})
                          </p>
                          <div className="space-y-2 text-sm">
                            {speaker.segments.slice(0, 3).map((seg, segIdx) => (
                              <div key={segIdx} className="text-gray-600">
                                {seg.start.toFixed(2)}s - {seg.end.toFixed(2)}s (
                                {(seg.end - seg.start).toFixed(2)}s)
                              </div>
                            ))}
                            {speaker.segments.length > 3 && (
                              <div className="text-gray-500 italic">
                                +{speaker.segments.length - 3} more segments
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Downloads Section */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold mb-6 text-gray-800">Downloads</h3>
              <div className="flex flex-col gap-3">
                <button
                  onClick={handleDownloadMetadata}
                  className="w-full md:w-auto bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded transition"
                >
                  📊 Download Metadata (JSON)
                </button>
                <button
                  onClick={() => handleDownloadSpeaker('original')}
                  className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded transition"
                >
                  🎵 Download Original Audio
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay;
