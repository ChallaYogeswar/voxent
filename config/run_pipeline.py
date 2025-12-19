import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine.batch_runner import run

if __name__ == "__main__":
    run("config/config.yaml")
