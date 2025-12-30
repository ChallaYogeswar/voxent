"""
Batch Organizer Module
Organizes audio files into duration-based batches for GPU-optimized processing

Key Features:
- Sorts files by duration (smallest to largest)
- Groups into batches respecting GPU memory limits
- Creates physical batch folders
- Monitors and reports batch statistics
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import json
import librosa
from datetime import datetime


class BatchOrganizer:
    """
    Organizes audio files into batches based on duration
    """
    
    def __init__(self, config: Dict):
        """
        Initialize batch organizer
        
        Args:
            config: Configuration dictionary with batch settings
        """
        self.config = config
        
        # Batch configuration
        self.files_per_batch = config.get('files_per_batch', 10)
        self.batch_size_minutes = config.get('batch_size_minutes', 2.0)
        self.batch_size_seconds = self.batch_size_minutes * 60
        
        print(f"Batch Organizer initialized:")
        print(f"  - Files per batch: {self.files_per_batch}")
        print(f"  - Max batch duration: {self.batch_size_minutes} minutes")
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            duration = librosa.get_duration(path=audio_path)
            return duration
        except Exception as e:
            print(f"Error getting duration for {audio_path}: {e}")
            return 0.0
    
    def scan_audio_files(self, input_dir: str) -> List[Dict]:
        """
        Scan directory for audio files and get their durations
        
        Args:
            input_dir: Directory containing audio files
            
        Returns:
            List of file info dictionaries sorted by duration
        """
        print(f"\nScanning audio files in: {input_dir}")
        
        # Supported audio formats
        audio_extensions = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac'}
        
        # Collect file info
        file_info = []
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if Path(filename).suffix.lower() in audio_extensions:
                    file_path = os.path.join(root, filename)
                    duration = self.get_audio_duration(file_path)
                    
                    if duration > 0:
                        file_info.append({
                            'path': file_path,
                            'filename': filename,
                            'duration': duration,
                            'size_mb': os.path.getsize(file_path) / (1024 * 1024)
                        })
        
        # Sort by duration (smallest to largest)
        file_info.sort(key=lambda x: x['duration'])
        
        print(f"Found {len(file_info)} audio files")
        if file_info:
            total_duration = sum(f['duration'] for f in file_info)
            print(f"Total duration: {total_duration/60:.2f} minutes")
            print(f"Duration range: {file_info[0]['duration']:.1f}s - {file_info[-1]['duration']:.1f}s")
        
        return file_info
    
    def create_batches(self, file_info: List[Dict]) -> List[List[Dict]]:
        """
        Create batches from file info list
        
        Args:
            file_info: List of file info dictionaries
            
        Returns:
            List of batches (each batch is a list of file info)
        """
        batches = []
        current_batch = []
        current_batch_duration = 0.0
        
        for file in file_info:
            # Check if adding this file would exceed limits
            would_exceed_duration = (current_batch_duration + file['duration']) > self.batch_size_seconds
            would_exceed_count = len(current_batch) >= self.files_per_batch
            
            # Start new batch if necessary
            if current_batch and (would_exceed_duration or would_exceed_count):
                batches.append(current_batch)
                current_batch = []
                current_batch_duration = 0.0
            
            # Add file to current batch
            current_batch.append(file)
            current_batch_duration += file['duration']
        
        # Add last batch if not empty
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def organize_into_folders(
        self, 
        batches: List[List[Dict]], 
        output_dir: str,
        copy_files: bool = True
    ) -> List[str]:
        """
        Create batch folders and organize files
        
        Args:
            batches: List of batches from create_batches()
            output_dir: Base directory for batch folders
            copy_files: If True, copy files; if False, move files
            
        Returns:
            List of created batch folder paths
        """
        print(f"\nOrganizing into batch folders: {output_dir}")
        
        # Create base output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        batch_folders = []
        
        for batch_idx, batch in enumerate(batches, 1):
            # Create batch folder
            batch_name = f"batch_{batch_idx:03d}"
            batch_path = os.path.join(output_dir, batch_name)
            Path(batch_path).mkdir(parents=True, exist_ok=True)
            
            # Copy/move files to batch folder
            batch_duration = 0.0
            for file_info in batch:
                src_path = file_info['path']
                dst_path = os.path.join(batch_path, file_info['filename'])
                
                if copy_files:
                    shutil.copy2(src_path, dst_path)
                else:
                    shutil.move(src_path, dst_path)
                
                batch_duration += file_info['duration']
            
            # Save batch metadata
            batch_metadata = {
                'batch_number': batch_idx,
                'num_files': len(batch),
                'total_duration_seconds': batch_duration,
                'total_duration_minutes': batch_duration / 60,
                'files': [
                    {
                        'filename': f['filename'],
                        'duration': f['duration'],
                        'size_mb': f['size_mb']
                    }
                    for f in batch
                ],
                'created_timestamp': datetime.now().isoformat()
            }
            
            metadata_path = os.path.join(batch_path, 'batch_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(batch_metadata, f, indent=2)
            
            batch_folders.append(batch_path)
            
            print(f"  ✓ {batch_name}: {len(batch)} files, {batch_duration:.1f}s total")
        
        print(f"\n✅ Created {len(batch_folders)} batches")
        return batch_folders
    
    def organize_directory(
        self, 
        input_dir: str, 
        output_dir: str,
        copy_files: bool = True
    ) -> Dict:
        """
        Complete pipeline: scan, batch, and organize
        
        Args:
            input_dir: Directory containing audio files to organize
            output_dir: Base directory for batch folders
            copy_files: If True, copy files; if False, move files
            
        Returns:
            Dictionary with organization results
        """
        print(f"\n{'='*60}")
        print(f"BATCH ORGANIZATION")
        print(f"{'='*60}")
        print(f"Input directory: {input_dir}")
        print(f"Output directory: {output_dir}")
        print(f"Mode: {'COPY' if copy_files else 'MOVE'}")
        
        # Step 1: Scan files
        file_info = self.scan_audio_files(input_dir)
        
        if not file_info:
            print("❌ No audio files found!")
            return {'error': 'No audio files found', 'batches': []}
        
        # Step 2: Create batches
        batches = self.create_batches(file_info)
        print(f"\nCreated {len(batches)} batches")
        
        # Step 3: Organize into folders
        batch_folders = self.organize_into_folders(batches, output_dir, copy_files)
        
        # Summary
        total_files = sum(len(batch) for batch in batches)
        total_duration = sum(sum(f['duration'] for f in batch) for batch in batches)
        
        result = {
            'input_dir': input_dir,
            'output_dir': output_dir,
            'num_batches': len(batches),
            'total_files': total_files,
            'total_duration_minutes': total_duration / 60,
            'batch_folders': batch_folders,
            'batches': [
                {
                    'batch_number': idx + 1,
                    'num_files': len(batch),
                    'duration_seconds': sum(f['duration'] for f in batch)
                }
                for idx, batch in enumerate(batches)
            ]
        }
        
        # Save overall summary
        summary_path = os.path.join(output_dir, 'organization_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"ORGANIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total batches: {len(batches)}")
        print(f"Total files: {total_files}")
        print(f"Total duration: {total_duration/60:.2f} minutes")
        print(f"Summary saved: {summary_path}")
        
        return result


def main():
    """Example usage"""
    
    # Configuration
    config = {
        'files_per_batch': 10,
        'batch_size_minutes': 2.0
    }
    
    # Initialize organizer
    organizer = BatchOrganizer(config)
    
    # Organize files
    input_directory = "data/input_calls"
    output_directory = "data/batches"
    
    result = organizer.organize_directory(
        input_dir=input_directory,
        output_dir=output_directory,
        copy_files=True  # Set to False to move instead of copy
    )
    
    print(f"\nOrganization result: {result}")


if __name__ == "__main__":
    main()
