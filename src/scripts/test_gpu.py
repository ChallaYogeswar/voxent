#!/usr/bin/env python
"""Test GPU and PyTorch Installation"""

import torch
import sys

print("\n" + "="*80)
print("GPU & PYTORCH VERIFICATION")
print("="*80)

try:
    print(f"\nPyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print("\n✅ GPU READY FOR ACCELERATION")
    else:
        print("\n⚠️  GPU not available, CPU will be used")
    
    # Test tensor operations
    x = torch.randn(100, 100)
    if torch.cuda.is_available():
        x_gpu = x.cuda()
        result = torch.matmul(x_gpu, x_gpu.T)
        print(f"✅ GPU Tensor Operations: OK")
    
    print("\n" + "="*80)
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("="*80)
    sys.exit(1)
