"""
VOXENT v2.0 - Voice Dataset Creation Pipeline
Complete pipeline for speaker diarization and voice dataset creation
"""

__version__ = "2.0.0"
__author__ = "VOXENT Team"
__description__ = "Voice dataset creation with speaker diarization and gender classification"

from src.pipeline.pipeline_runner import VoxentPipeline

__all__ = ['VoxentPipeline']
