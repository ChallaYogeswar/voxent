def get_dataset_files(label):
    """Get files in a dataset category."""
    try:
        dataset_dir = f"data/voice_dataset/{label}"
        if not os.path.exists(dataset_dir):
            return jsonify({"error": "Dataset category not found"}), 404

        files = []
        for file in os.listdir(dataset_dir):
            if file.endswith('.wav'):
                file_path = os.path.join(dataset_dir, file)
                size = os.path.getsize(file_path)
                files.append({
                    "name": file,
                    "size": size,
                    "url": f"/audio/{label}/{file}"
                })

        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
=======
@app.route('/dataset/<label>')
def get_dataset_files(label):
    """Get files in a dataset category."""
    try:
        dataset_dir = f"data/voice_dataset/{label}"
        if not os.path.exists(dataset_dir):
            return jsonify({"error": "Dataset category not found"}), 404

        files = []
        for file in os.listdir(dataset_dir):
            if file.endswith('.wav'):
                file_path = os.path.join(dataset_dir, file)
                size = os.path.getsize(file_path)
                # Parse metadata from filename
                parts = file.replace('.wav', '').split('_')
                confidence = 0
                for part in parts:
                    if part.startswith('conf'):
                        confidence = int(part[4:])

                files.append({
                    "name": file,
                    "size": size,
                    "url": f"/audio/{label}/{file}",
                    "confidence": confidence
                })

        # Sort by confidence descending
        files.sort(key=lambda x: x['confidence'], reverse=True)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<label>/<filename>')
def get_audio_file(label, filename):
    """Serve audio files for preview."""
    try:
        return send_from_directory(f"data/voice_dataset/{label}", filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
