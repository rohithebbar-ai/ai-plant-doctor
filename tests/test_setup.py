"""
Simple working test for AI Plant Doctor
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasicSetup(unittest.TestCase):
    """Test that basic setup is working"""
    
    def test_imports(self):
        """Test that we can import basic modules"""
        try:
            from PIL import Image
            self.assertTrue(True, "PIL imported successfully")
        except ImportError:
            self.fail("PIL/Pillow not available")
    
    def test_torch(self):
        """Test that PyTorch is available"""
        try:
            import torch
            self.assertTrue(True, "PyTorch imported successfully")
        except ImportError:
            self.fail("PyTorch not available")
    
    def test_image_creation(self):
        """Test basic image operations"""
        from PIL import Image
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='green')
        self.assertEqual(img.size, (100, 100))
        self.assertEqual(img.mode, 'RGB')
    
    def test_project_structure(self):
        """Test that project structure exists"""
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # Check for src directory
        src_dir = os.path.join(project_root, 'src')
        self.assertTrue(os.path.exists(src_dir), "src/ directory should exist")
        
        # Check for tests directory
        tests_dir = os.path.join(project_root, 'tests')
        self.assertTrue(os.path.exists(tests_dir), "tests/ directory should exist")

if __name__ == '__main__':
    unittest.main(verbosity=2)
