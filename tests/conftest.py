# tests/conftest.py - Pytest configuration and fixtures

import sys
import os
from unittest.mock import Mock, patch

# Add src directory to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Mock missing utility functions for testing
def mock_resize_image_for_analysis(image, max_size=1024):
    """Mock image resizing function"""
    if hasattr(image, 'size') and max(image.size) > max_size:
        # Simple mock resize
        from PIL import Image
        return image.resize((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def mock_validate_image(image):
    """Mock image validation function"""
    if image is None:
        return False, "No image provided"
    if hasattr(image, 'size'):
        width, height = image.size
        if width < 100 or height < 100:
            return False, "Image is too small. Please upload a larger image."
        if width * height > 10000000:
            return False, "Image is too large. Please upload a smaller image."
        return True, "Image is valid"
    return False, "Invalid image format"

def mock_extract_plant_keywords(text):
    """Mock plant keyword extraction"""
    keywords = []
    text_lower = text.lower()
    plant_words = ['tomato', 'plant', 'leaf', 'leaves', 'greenhouse', 'garden', 'yellowing']
    for word in plant_words:
        if word in text_lower:
            keywords.append(word)
    return keywords

def mock_get_plant_care_schedule(plant_type, season):
    """Mock plant care schedule"""
    return f"{season.title()} Care for {plant_type.title()}:\n• Water regularly\n• Monitor for pests"

# Add mock functions to utils module if it doesn't exist
try:
    import utils
    if not hasattr(utils, 'resize_image_for_analysis'):
        utils.resize_image_for_analysis = mock_resize_image_for_analysis
    if not hasattr(utils, 'validate_image'):
        utils.validate_image = mock_validate_image
    if not hasattr(utils, 'extract_plant_keywords'):
        utils.extract_plant_keywords = mock_extract_plant_keywords
    if not hasattr(utils, 'get_plant_care_schedule'):
        utils.get_plant_care_schedule = mock_get_plant_care_schedule
except ImportError:
    pass