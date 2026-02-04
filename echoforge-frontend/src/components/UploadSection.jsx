import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadAPI } from '../services/api';

const UploadSection = () => {
  const [file, setFile] = useState(null);
  const [numSpeakers, setNumSpeakers] = useState(2);
  const [vadEnabled, setVadEnabled] = useState(true);
  const [highAccuracy, setHighAccuracy] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setError('');
    
    if (selectedFile) {
      const supportedFormats = ['audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/flac'];
      if (!supportedFormats.includes(selectedFile.type)) {
        setError('Unsupported file format. Please upload .wav, .mp3, .m4a, or .flac');
        return;
      }
      if (selectedFile.size > 500 * 1024 * 1024) {
        setError('File size exceeds 500MB limit');
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an audio file');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('audio_file', file);
      formData.append('num_speakers', numSpeakers);
      formData.append('vad_enabled', vadEnabled);
      formData.append('high_accuracy', highAccuracy);

      const response = await uploadAPI.uploadAudio(formData);
      const { job_id } = response.data;
      navigate(`/status/${job_id}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 py-12">
      <div className="container mx-auto px-6">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold mb-8 text-gray-800">Upload Audio File</h2>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleUpload} className="space-y-6">
            {/* File Input */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-500 transition">
              <input
                type="file"
                accept=".wav,.mp3,.m4a,.flac"
                onChange={handleFileChange}
                className="hidden"
                id="file-input"
              />
              <label htmlFor="file-input" className="cursor-pointer">
                <div className="text-4xl mb-2">📁</div>
                <p className="text-gray-600">
                  {file ? `Selected: ${file.name}` : 'Click to select or drag audio file'}
                </p>
                <p className="text-sm text-gray-400 mt-2">
                  Supported: .wav, .mp3, .m4a, .flac (Max 500MB)
                </p>
              </label>
            </div>

            {/* Number of Speakers */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Expected Number of Speakers
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setNumSpeakers(num)}
                    className={`px-4 py-2 rounded transition ${
                      numSpeakers === num
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                    }`}
                  >
                    {num}
                  </button>
                ))}
              </div>
            </div>

            {/* Options */}
            <div className="space-y-3">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={vadEnabled}
                  onChange={(e) => setVadEnabled(e.target.checked)}
                  className="w-4 h-4"
                />
                <span className="text-gray-700">Voice Activity Detection (VAD)</span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={highAccuracy}
                  onChange={(e) => setHighAccuracy(e.target.checked)}
                  className="w-4 h-4"
                />
                <span className="text-gray-700">High Accuracy Mode (Slower)</span>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !file}
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-3 rounded-lg transition"
            >
              {loading ? 'Uploading...' : 'Upload & Process'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UploadSection;
