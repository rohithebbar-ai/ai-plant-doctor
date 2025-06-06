"""
AI Plant Doctor Test Suite

This package contains unit tests for all modules of the AI Plant Doctor application.
Tests are organized by module and cover:
- Basic functionality
- Model handler operations
- Plant health analyzer logic
- Utility functions
- Error handling and edge cases

Run tests with: python -m pytest tests/
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

__version__ = "1.0.0"
__author__ = "AI Plant Doctor Contributors"