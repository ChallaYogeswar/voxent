"""
Integrated Batch Processor
Processes batches of audio files with speaker diarization, gender classification,
and GPU memory monitoring

Key Features:
- Processes batch folders sequentially
- GPU memory monitoring and management
- Speaker separation with gender classification
- VRAM usage tracking and batch size adjustment
- Progress tracking and error handling
"""

import os
import torch
import psutil
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import time


class GPUMonitor:
    """Monitor and manage GPU memory usage"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.has_gpu = torch.cuda.is_available()
        
        if self.has_gpu:
            self.gpu_name = torch.cuda.get_device_name(0)
            self.total_memory = torch.cuda.get_device_properties(0).total_memory
            print(f"GPU detected: {self.gpu_name}")
            print(f"Total VRAM: {self.total_memory / 1e9:.2f} GB")
        else:
            print("No GPU detected, using CPU")
    
    def get_memory_usage(self) -> Dict:
        """Get current GPU memory usage"""
        if not self.has_gpu:
            return {'has_gpu': False}
        
        allocated = torch.cuda.memory_allocated(0)
        reserved = torch.cuda.memory_reserved(0)
        free = self.total_memory - allocated
        
        return {
            'has_gpu': True,
            'allocated_mb': allocated / 1e6,
            'reserved_mb': reserved / 1e6,
            'free_mb': free / 1e6,
            'total_mb': self.total_memory / 1e6,
            'usage_percent': (allocated / self.total_memory) * 100
        }
    
    def clear_cache(self):
        """Clear GPU cache"""
        if self.has_gpu:
            torch.cuda.empty_cache()
            print("  ✓ GPU cache cleared")
    
    def is_memory_warning(self, threshold: float = 80.0) -> bool:
        """Check if GPU memory usage exceeds threshold"""
        if not self.has_gpu:
            return False
        
        usage = self.get_memory_usage()
        return usage['usage_percent'] > threshold
    
    def print_memory_status(self):
        """Print current memory status"""
        usage = self.get_memory_usage()
        
        if not usage['has_gpu']:
            print("  GPU: Not available")
            return
        
        print(f"  GPU Memory: {usage['allocated_mb']:.1f}/{usage['total_mb']:.1f} MB "
              f"({usage['usage_percent']:.1f}% used)")


class IntegratedBatchProcessor:
    """
    Processes batches of audio files with speaker diarization
    """
    
    def __init__(self, diarizer, config: Dict):
        """
        Initialize batch processor
        
        Args:
            diarizer: EnhancedSpeakerDiarizer instance
            config: Configuration dictionary
        """
        self.diarizer = diarizer
        self.config = config
        self.gpu_monitor = GPUMonitor()
        
        # Batch processing config
        self.batch_size_gpu = config.get('batch_size_gpu', 10)
        self.gpu_memory_threshold = config.get('gpu_memory_threshold', 80.0)
        self.clear_cache_between_batches = config.get('clear_cache_between_batches', True)
        
        print(f"\nBatch Processor initialized:")
        print(f"  - GPU batch size: {self.batch_size_gpu}")
        print(f"  - Memory threshold: {self.gpu_memory_threshold}%")
        print(f"  - Clear cache between batches: {self.clear_cache_between_batches}")
    
    def process_single_file(
        self, 
        audio_path: str, 
        output_dir: str
    ) -> Optional[Dict]:
        """
        Process a single audio file
        
        Args:
            audio_path: Path to audio file
            output_dir: Output directory for this file
            
        Returns:
            Processing results or None if error
        """
        try:
            # Check GPU memory before processing
            if self.gpu_monitor.is_memory_warning(self.gpu_memory_threshold):
                print(f"  ⚠️  High GPU memory usage detected")
                self.gpu_monitor.clear_cache()
            
            # Process file
            result = self.diarizer.process_audio_file(
                audio_path=audio_path,
                output_base_dir=output_dir,
                organize_by_gender=True
            )
            
            return result
            
        except Exception as e:
            print(f"  ❌ Error processing {audio_path}: {e}")
            return None
    
    def process_batch_folder(
        self, 
        batch_folder: str, 
        output_base_dir: str
    ) -> Dict:
        """
        Process all files in a batch folder
        
        Args:
            batch_folder: Path to batch folder
            output_base_dir: Base directory for outputs
            
        Returns:
            Batch processing results
        """
        batch_name = os.path.basename(batch_folder)
        print(f"\n{'='*60}")
        print(f"PROCESSING BATCH: {batch_name}")
        print(f"{'='*60}")
        
        # Get audio files in batch
        audio_files = []
        for filename in os.listdir(batch_folder):
            if filename.endswith(('.wav', '.mp3', '.flac', '.m4a')):
                audio_files.append(os.path.join(batch_folder, filename))
        
        print(f"Files to process: {len(audio_files)}")
        
        # Create output directory for this batch
        batch_output_dir = os.path.join(output_base_dir, batch_name)
        Path(batch_output_dir).mkdir(parents=True, exist_ok=True)
        
        # Process each file
        results = []
        successful = 0
        failed = 0
        start_time = time.time()
        
        for idx, audio_path in enumerate(audio_files, 1):
            print(f"\n[{idx}/{len(audio_files)}] Processing: {os.path.basename(audio_path)}")
            
            # Show GPU status
            self.gpu_monitor.print_memory_status()
            
            # Create output directory for this file
            file_output_dir = os.path.join(
                batch_output_dir,
                Path(audio_path).stem
            )
            
            # Process file
            result = self.process_single_file(audio_path, file_output_dir)
            
            if result:
                results.append(result)
                successful += 1
            else:
                failed += 1
        
        # Clear GPU cache after batch
        if self.clear_cache_between_batches:
            self.gpu_monitor.clear_cache()
        
        # Calculate statistics
        processing_time = time.time() - start_time
        
        batch_result = {
            'batch_name': batch_name,
            'batch_folder': batch_folder,
            'output_dir': batch_output_dir,
            'total_files': len(audio_files),
            'successful': successful,
            'failed': failed,
            'processing_time_seconds': processing_time,
            'files': results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save batch results
        results_path = os.path.join(batch_output_dir, 'batch_results.json')
        with open(results_path, 'w') as f:
            json.dump(batch_result, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE: {batch_name}")
        print(f"{'='*60}")
        print(f"Successful: {successful}/{len(audio_files)}")
        print(f"Failed: {failed}/{len(audio_files)}")
        print(f"Processing time: {processing_time/60:.2f} minutes")
        print(f"Results saved: {results_path}")
        
        return batch_result
    
    def process_all_batches(
        self, 
        batches_dir: str, 
        output_base_dir: str
    ) -> Dict:
        """
        Process all batch folders
        
        Args:
            batches_dir: Directory containing batch folders
            output_base_dir: Base directory for all outputs
            
        Returns:
            Overall processing results
        """
        print(f"\n{'='*70}")
        print(f"STARTING BATCH PROCESSING")
        print(f"{'='*70}")
        print(f"Batches directory: {batches_dir}")
        print(f"Output directory: {output_base_dir}")
        
        # Find all batch folders
        batch_folders = sorted([
            os.path.join(batches_dir, d)
            for d in os.listdir(batches_dir)
            if os.path.isdir(os.path.join(batches_dir, d)) and d.startswith('batch_')
        ])
        
        if not batch_folders:
            print("❌ No batch folders found!")
            return {'error': 'No batch folders found'}
        
        print(f"\nFound {len(batch_folders)} batch folders")
        
        # Process each batch
        all_results = []
        total_files = 0
        total_successful = 0
        total_failed = 0
        overall_start = time.time()
        
        for batch_idx, batch_folder in enumerate(batch_folders, 1):
            print(f"\n{'#'*70}")
            print(f"BATCH {batch_idx}/{len(batch_folders)}")
            print(f"{'#'*70}")
            
            # Process batch
            batch_result = self.process_batch_folder(batch_folder, output_base_dir)
            all_results.append(batch_result)
            
            # Update totals
            total_files += batch_result['total_files']
            total_successful += batch_result['successful']
            total_failed += batch_result['failed']
            
            # Show progress
            print(f"\n📊 Overall progress: {batch_idx}/{len(batch_folders)} batches")
            print(f"   Total files processed: {total_successful + total_failed}/{total_files}")
            
            # Clear GPU cache between batches
            if self.clear_cache_between_batches and batch_idx < len(batch_folders):
                print("\n🔄 Preparing for next batch...")
                self.gpu_monitor.clear_cache()
                time.sleep(2)  # Brief pause
        
        # Final statistics
        total_time = time.time() - overall_start
        
        overall_result = {
            'batches_processed': len(batch_folders),
            'total_files': total_files,
            'successful': total_successful,
            'failed': total_failed,
            'success_rate': (total_successful / total_files * 100) if total_files > 0 else 0,
            'total_processing_time_minutes': total_time / 60,
            'batches': all_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save overall results
        summary_path = os.path.join(output_base_dir, 'processing_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(overall_result, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"ALL BATCHES COMPLETE")
        print(f"{'='*70}")
        print(f"Batches processed: {len(batch_folders)}")
        print(f"Total files: {total_files}")
        print(f"Successful: {total_successful} ({overall_result['success_rate']:.1f}%)")
        print(f"Failed: {total_failed}")
        print(f"Total time: {total_time/60:.2f} minutes")
        print(f"Average per file: {total_time/total_files:.1f} seconds")
        print(f"\nSummary saved: {summary_path}")
        
        return overall_result


def main():
    """Example usage"""
    
    # Import the diarizer
    from enhanced_diarizer import EnhancedSpeakerDiarizer
    
    # Configuration
    config = {
        # Diarization config
        'min_speakers': 2,
        'max_speakers': 2,
        'hf_token': None,  # Set your HuggingFace token
        
        # Batch processing config
        'batch_size_gpu': 10,
        'gpu_memory_threshold': 80.0,
        'clear_cache_between_batches': True
    }
    
    # Initialize diarizer
    diarizer = EnhancedSpeakerDiarizer(config)
    
    # Initialize batch processor
    processor = IntegratedBatchProcessor(diarizer, config)
    
    # Process all batches
    batches_directory = "data/batches"
    output_directory = "data/voice_dataset"
    
    result = processor.process_all_batches(
        batches_dir=batches_directory,
        output_base_dir=output_directory
    )
    
    print(f"\nFinal result: {result}")


if __name__ == "__main__":
    main()
