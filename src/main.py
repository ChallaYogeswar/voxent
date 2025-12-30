"""
VOXENT Main Entry Point
Primary interface for running the VOXENT pipeline
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import VoxentPipeline


def main():
    """Main entry point for VOXENT"""
    parser = argparse.ArgumentParser(
        description="VOXENT v2.0 - Voice Dataset Creation with Speaker Diarization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --config config/config.yaml
  python src/main.py --config config/config.yaml --skip-organize
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to YAML configuration file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--skip-organize',
        action='store_true',
        help='Skip batch organization step (use existing batches)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='VOXENT v2.0'
    )
    
    args = parser.parse_args()
    
    # Verify config file exists
    if not os.path.exists(args.config):
        print(f"❌ Configuration file not found: {args.config}")
        print(f"Please provide a valid config file path")
        sys.exit(1)
    
    try:
        # Initialize and run pipeline
        print("\n" + "="*70)
        print("VOXENT v2.0 - Voice Dataset Creation Pipeline")
        print("="*70)
        
        pipeline = VoxentPipeline(args.config)
        
        if args.skip_organize:
            print("\n⏭️  Skipping batch organization step...")
            print("   Using existing batches from configured directory")
            pipeline.step2_initialize_diarizer()
            pipeline.step3_process_batches()
        else:
            print("\n🚀 Running complete pipeline...")
            pipeline.run()
        
        print("\n✅ Pipeline execution completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
