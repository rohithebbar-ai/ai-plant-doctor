"""
Unit tests for utils.py

Tests utility functions for formatting, validation, and helper operations.
"""

import unittest
from unittest.mock import Mock, patch
from PIL import Image
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from utils import (
        format_diagnosis_report, ensure_confidence_string, validate_image,
        resize_image_for_analysis, format_symptoms_list, format_treatments_text,
        extract_plant_keywords, create_severity_badge, format_confidence_indicator,
        sanitize_filename, create_diagnosis_summary, get_confidence_recommendation
    )
except ImportError as e:
    print(f"Import warning: {e}")


class TestConfidenceHandling(unittest.TestCase):
    """Test confidence score handling"""
    
    def test_ensure_confidence_string_float_input(self):
        """Test confidence conversion from float values"""
        test_cases = [
            (0.9, "high"),
            (0.85, "high"),
            (0.8, "high"),
            (0.75, "medium"),
            (0.65, "medium"),
            (0.6, "medium"),
            (0.5, "low"),
            (0.3, "low"),
            (0.1, "low"),
            (0.0, "low"),
            (1.0, "high")
        ]
        
        for input_val, expected in test_cases:
            result = ensure_confidence_string(input_val)
            self.assertEqual(result, expected, 
                           f"Input {input_val} should return {expected}, got {result}")
    
    def test_ensure_confidence_string_string_input(self):
        """Test confidence conversion from string values"""
        test_cases = [
            ("high", "high"),
            ("HIGH", "high"),
            ("Medium", "medium"),
            ("MEDIUM", "medium"),
            ("low", "low"),
            ("Low", "low")
        ]
        
        for input_val, expected in test_cases:
            result = ensure_confidence_string(input_val)
            self.assertEqual(result, expected)
    
    def test_ensure_confidence_string_invalid_input(self):
        """Test confidence conversion with invalid inputs"""
        invalid_inputs = [None, "", "invalid", -1, 2.0, [], {}]
        
        for invalid_input in invalid_inputs:
            result = ensure_confidence_string(invalid_input)
            self.assertEqual(result, "low")


class TestDiagnosisReportFormatting(unittest.TestCase):
    """Test diagnosis report formatting"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_results = {
            "severity_level": "moderate",
            "confidence_score": "high",
            "possible_conditions": [
                {
                    "name": "fungal_leaf_spot",
                    "confidence": 0.85,
                    "info": {
                        "description": "Fungal infection causing leaf spots",
                        "treatments": [
                            {
                                "type": "fungicide",
                                "action": "Apply copper fungicide",
                                "details": ["Spray weekly", "Remove affected leaves"]
                            }
                        ]
                    }
                }
            ],
            "detected_symptoms": [
                {"name": "spots", "confidence": 0.8},
                {"name": "browning", "confidence": 0.7}
            ],
            "treatments": [
                {
                    "type": "fungicide",
                    "action": "Apply fungicide treatment",
                    "urgency": "medium",
                    "details": ["Apply every 7 days"]
                }
            ],
            "immediate_actions": [
                "Remove affected leaves immediately",
                "Improve air circulation"
            ]
        }
        
        self.healthy_results = {
            "severity_level": "none",
            "confidence_score": "high",
            "possible_conditions": [
                {
                    "name": "healthy_plant",
                    "confidence": 0.9,
                    "info": {
                        "description": "Plant appears healthy"
                    }
                }
            ],
            "detected_symptoms": [
                {"name": "healthy_plant", "confidence": 0.9}
            ],
            "treatments": [],
            "immediate_actions": [
                "✅ Great news! Your plant appears healthy"
            ]
        }
    
    def test_format_diagnosis_report_normal(self):
        """Test formatting of normal diagnosis report"""
        report = format_diagnosis_report(self.sample_results)
        
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        
        # Check for key elements
        self.assertIn("moderate", report.lower())
        self.assertIn("fungal", report.lower())
        self.assertIn("diagnosis-card", report)
        self.assertIn("high", report.lower())
    
    def test_format_diagnosis_report_healthy(self):
        """Test formatting of healthy plant report"""
        report = format_diagnosis_report(self.healthy_results)
        
        self.assertIn("healthy", report.lower())
        self.assertIn("severity-healthy", report)
        self.assertIn("great news", report.lower())
    
    def test_format_diagnosis_report_error(self):
        """Test formatting with error results"""
        error_results = {"error": "Analysis failed"}
        report = format_diagnosis_report(error_results)
        
        self.assertIn("Unable to generate", report)
        self.assertIn("emergency-alert", report)
    
    def test_format_diagnosis_report_empty(self):
        """Test formatting with empty results"""
        empty_results = {}
        report = format_diagnosis_report(empty_results)
        
        self.assertIn("Unable to generate", report)


class TestImageValidation(unittest.TestCase):
    """Test image validation functions"""
    
    def test_validate_image_valid(self):
        """Test validation of valid images"""
        # Test RGB image
        rgb_image = Image.new('RGB', (500, 400), color='green')
        is_valid, message = validate_image(rgb_image)
        self.assertTrue(is_valid)
        self.assertIn("valid", message.lower())
        
        # Test RGBA image
        rgba_image = Image.new('RGBA', (300, 300), color=(0, 255, 0, 255))
        is_valid, message = validate_image(rgba_image)
        self.assertTrue(is_valid)
        
        # Test grayscale image
        gray_image = Image.new('L', (200, 200), color=128)
        is_valid, message = validate_image(gray_image)
        self.assertTrue(is_valid)
    
    def test_validate_image_invalid(self):
        """Test validation of invalid images"""
        # Test None
        is_valid, message = validate_image(None)
        self.assertFalse(is_valid)
        self.assertIn("no image", message.lower())
        
        # Test too small image
        small_image = Image.new('RGB', (50, 50), color='green')
        is_valid, message = validate_image(small_image)
        self.assertFalse(is_valid)
        self.assertIn("too small", message.lower())
        
        # Test too large image
        # Create very large image dimensions (simulate without actual large image)
        large_image = Mock()
        large_image.size = (5000, 5000)  # 25MP
        
        with patch('utils.Image.Image', return_value=large_image):
            is_valid, message = validate_image(large_image)
            self.assertFalse(is_valid)
            self.assertIn("too large", message.lower())
    
    def test_resize_image_for_analysis(self):
        """Test image resizing functionality"""
        # Test large image resizing
        large_image = Image.new('RGB', (2000, 1500), color='blue')
        resized = resize_image_for_analysis(large_image, max_size=512)
        
        self.assertLessEqual(max(resized.size), 512)
        self.assertEqual(resized.mode, 'RGB')
        
        # Test small image (should not resize)
        small_image = Image.new('RGB', (300, 200), color='red')
        not_resized = resize_image_for_analysis(small_image, max_size=512)
        self.assertEqual(small_image.size, not_resized.size)
        
        # Test aspect ratio preservation
        wide_image = Image.new('RGB', (1000, 500), color='yellow')
        resized_wide = resize_image_for_analysis(wide_image, max_size=400)
        
        # Should maintain aspect ratio (2:1)
        width, height = resized_wide.size
        aspect_ratio = width / height
        self.assertAlmostEqual(aspect_ratio, 2.0, places=1)


class TestTextFormatting(unittest.TestCase):
    """Test text formatting utilities"""
    
    def test_format_symptoms_list(self):
        """Test symptom list formatting"""
        symptoms = [
            {"name": "yellowing", "confidence": 0.8},
            {"name": "spots", "confidence": 0.7},
            {"name": "wilting", "confidence": 0.6}
        ]
        
        formatted = format_symptoms_list(symptoms)
        
        self.assertIn("Yellowing", formatted)
        self.assertIn("80%", formatted)
        self.assertIn("Spots", formatted)
        self.assertIn("70%", formatted)
        
        # Test empty list
        empty_formatted = format_symptoms_list([])
        self.assertIn("No specific symptoms", empty_formatted)
    
    def test_format_treatments_text(self):
        """Test treatment text formatting"""
        treatments = [
            {
                "action": "Apply fungicide",
                "urgency": "high",
                "details": ["Spray weekly", "Use copper-based"]
            },
            {
                "action": "Improve drainage",
                "urgency": "medium",
                "details": ["Add drainage holes"]
            }
        ]
        
        formatted = format_treatments_text(treatments)
        
        self.assertIn("Apply fungicide", formatted)
        self.assertIn("high priority", formatted)
        self.assertIn("Spray weekly", formatted)
        self.assertIn("Improve drainage", formatted)
        
        # Test empty list
        empty_formatted = format_treatments_text([])
        self.assertIn("No specific treatments", empty_formatted)
    
    def test_extract_plant_keywords(self):
        """Test plant keyword extraction"""
        test_text = "My tomato plant in the greenhouse is showing yellowing leaves"
        keywords = extract_plant_keywords(test_text)
        
        expected_keywords = ["tomato", "greenhouse", "yellowing", "leaves"]
        for keyword in expected_keywords:
            self.assertIn(keyword, keywords)
        
        # Test empty text
        empty_keywords = extract_plant_keywords("")
        self.assertEqual(empty_keywords, [])
    
    def test_create_severity_badge(self):
        """Test severity badge creation"""
        test_cases = [
            ("critical", "🔴 CRITICAL"),
            ("high", "🟠 HIGH"),
            ("moderate", "🟡 MODERATE"),
            ("mild", "🟢 MILD"),
            ("none", "🌱 HEALTHY"),
            ("unknown", "⚪ UNKNOWN")
        ]
        
        for severity, expected in test_cases:
            badge = create_severity_badge(severity)
            self.assertEqual(badge, expected)
    
    def test_format_confidence_indicator(self):
        """Test confidence indicator formatting"""
        test_cases = [
            ("high", "🎯 High Confidence"),
            ("medium", "🎲 Medium Confidence"),
            ("low", "❓ Low Confidence"),
            ("unknown", "❓ Unknown Confidence")
        ]
        
        for confidence, expected in test_cases:
            indicator = format_confidence_indicator(confidence)
            self.assertEqual(indicator, expected)
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        test_cases = [
            ("plant_image.jpg", "plant_image.jpg"),
            ("plant<>image?.jpg", "plant__image_.jpg"),
            ("plant|image/file.png", "plant_image_file.png"),
            ("  .hidden_file  ", "hidden_file"),
            ("", "plant_image"),
            ("normal_filename", "normal_filename")
        ]
        
        for input_name, expected in test_cases:
            sanitized = sanitize_filename(input_name)
            self.assertEqual(sanitized, expected)
    
    def test_create_diagnosis_summary(self):
        """Test diagnosis summary creation"""
        # Test healthy plant
        healthy_results = {
            "severity_level": "none",
            "possible_conditions": [{"name": "healthy_plant"}],
            "confidence_score": "high"
        }
        
        summary = create_diagnosis_summary(healthy_results)
        self.assertIn("HEALTHY", summary)
        self.assertIn("excellent condition", summary)
        
        # Test disease condition
        disease_results = {
            "severity_level": "moderate",
            "possible_conditions": [{"name": "fungal_leaf_spot"}],
            "confidence_score": "medium"
        }
        
        summary = create_diagnosis_summary(disease_results)
        self.assertIn("MODERATE", summary)
        self.assertIn("Fungal Leaf Spot", summary)
        
        # Test error condition
        error_results = {"error": "Analysis failed"}
        summary = create_diagnosis_summary(error_results)
        self.assertIn("Diagnosis failed", summary)
    
    def test_get_confidence_recommendation(self):
        """Test confidence-based recommendations"""
        # Test healthy plant recommendations
        healthy_high = get_confidence_recommendation("high", "none")
        self.assertIn("healthy", healthy_high.lower())
        self.assertIn("excellent", healthy_high.lower())
        
        # Test problem plant recommendations
        problem_high = get_confidence_recommendation("high", "moderate")
        self.assertIn("reliable", problem_high.lower())
        self.assertIn("follow treatment", problem_high.lower())
        
        # Test low confidence
        low_conf = get_confidence_recommendation("low", "mild")
        self.assertIn("low confidence", low_conf.lower())
        self.assertIn("expert", low_conf.lower())


class TestAdvancedFormatting(unittest.TestCase):
    """Test advanced formatting utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_results = {
            "severity_level": "moderate",
            "possible_conditions": [
                {
                    "name": "fungal_leaf_spot",
                    "confidence": 0.8,
                    "info": {"description": "Fungal infection"}
                }
            ],
            "detected_symptoms": [
                {"name": "spots", "confidence": 0.8}
            ]
        }
    
    def test_format_prevention_tips(self):
        """Test prevention tips formatting"""
        from utils import format_prevention_tips
        
        tips = [
            "Water at soil level to avoid wetting leaves",
            "Ensure good air circulation",
            "Remove infected debris"
        ]
        
        formatted = format_prevention_tips(tips)
        self.assertIn("Water at soil level", formatted)
        self.assertIn("air circulation", formatted)
        
        # Test empty tips
        empty_formatted = format_prevention_tips([])
        self.assertIn("No specific prevention", empty_formatted)
    
    def test_estimate_recovery_time(self):
        """Test recovery time estimation"""
        from utils import estimate_recovery_time
        
        # Test different condition types and severities
        fungal_mild = estimate_recovery_time("mild", "fungal_leaf_spot")
        self.assertIn("week", fungal_mild.lower())
        
        bacterial_high = estimate_recovery_time("high", "bacterial_infection")
        self.assertIn("week", bacterial_high.lower())
        
        nutrient_moderate = estimate_recovery_time("moderate", "nutrient_deficiency")
        self.assertIn("week", nutrient_moderate.lower())
    
    def test_create_treatment_timeline(self):
        """Test treatment timeline creation"""
        from utils import create_treatment_timeline
        
        treatments = [
            {"action": "Remove affected leaves", "urgency": "high"},
            {"action": "Apply fungicide", "urgency": "medium"},
            {"action": "Improve ventilation", "urgency": "low"}
        ]
        
        timeline = create_treatment_timeline(treatments)
        self.assertIn("Treatment Timeline", timeline)
        self.assertIn("Immediate", timeline)
        self.assertIn("Remove affected leaves", timeline)
        
        # Test empty treatments
        empty_timeline = create_treatment_timeline([])
        self.assertIn("No treatment timeline", empty_timeline)
    
    def test_generate_care_checklist(self):
        """Test care checklist generation"""
        from utils import generate_care_checklist
        
        checklist = generate_care_checklist(self.sample_results)
        
        self.assertIn("Daily Care Checklist", checklist)
        self.assertIn("□", checklist)  # Checkbox character
        self.assertIn("soil moisture", checklist.lower())
        self.assertIn("inspect leaves", checklist.lower())
    
    def test_get_plant_care_schedule(self):
        """Test plant care schedule generation"""
        from utils import get_plant_care_schedule
        
        # Test specific plant and season
        tomato_spring = get_plant_care_schedule("tomato", "spring")
        self.assertIn("Spring Care", tomato_spring)
        self.assertIn("Tomato", tomato_spring)
        
        # Test general plant care
        general_summer = get_plant_care_schedule("unknown", "summer")
        self.assertIn("Summer Care", general_summer)
        self.assertIn("General", general_summer)
    
    def test_format_scientific_info(self):
        """Test scientific information formatting"""
        from utils import format_scientific_info
        
        # Test known condition
        fungal_info = format_scientific_info("fungal_leaf_spot")
        self.assertIn("Scientific Information", fungal_info)
        self.assertIn("Pathogen", fungal_info)
        
        # Test unknown condition
        unknown_info = format_scientific_info("unknown_condition")
        self.assertIn("not available", unknown_info.lower())
    
    def test_calculate_treatment_cost(self):
        """Test treatment cost calculation"""
        from utils import calculate_treatment_cost
        
        treatments = [
            {"type": "fungicide", "action": "Apply copper fungicide"},
            {"type": "cultural", "action": "Improve drainage"}
        ]
        
        costs = calculate_treatment_cost(treatments)
        
        self.assertIn("budget", costs)
        self.assertIn("standard", costs)
        self.assertIn("premium", costs)
        
        for cost_type, cost_range in costs.items():
            self.assertIn("$", cost_range)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in utility functions"""
    
    def test_format_diagnosis_report_with_none(self):
        """Test diagnosis report formatting with None input"""
        report = format_diagnosis_report(None)
        self.assertIn("Unable to generate", report)
    
    def test_validate_image_with_corrupted_image(self):
        """Test image validation with corrupted image"""
        # Create a mock corrupted image
        corrupted_image = Mock()
        corrupted_image.size = None  # Simulate corruption
        
        with patch.object(corrupted_image, 'size', side_effect=Exception("Corrupted")):
            is_valid, message = validate_image(corrupted_image)
            self.assertFalse(is_valid)
            self.assertIn("error", message.lower())
    
    def test_extract_plant_keywords_with_special_chars(self):
        """Test keyword extraction with special characters"""
        special_text = "My tømato plænt! has yelløwing leaves... #greenhouse"
        keywords = extract_plant_keywords(special_text)
        
        # Should handle special characters gracefully
        self.assertIsInstance(keywords, list)
    
    def test_sanitize_filename_edge_cases(self):
        """Test filename sanitization edge cases"""
        edge_cases = [
            None,  # Should not crash
            123,   # Non-string input
            ".",   # Just a dot
            "..",  # Double dot
            "...",  # Multiple dots
        ]
        
        for case in edge_cases:
            try:
                result = sanitize_filename(str(case) if case is not None else "")
                self.assertIsInstance(result, str)
            except Exception as e:
                self.fail(f"sanitize_filename failed on {case}: {e}")


class TestIntegrationUtilities(unittest.TestCase):
    """Test integration between utility functions"""
    
    def test_full_report_generation_pipeline(self):
        """Test complete report generation pipeline"""
        # Create comprehensive test results
        complete_results = {
            "severity_level": "moderate",
            "confidence_score": "high",
            "possible_conditions": [
                {
                    "name": "fungal_leaf_spot",
                    "confidence": 0.85,
                    "info": {
                        "description": "Fungal infection causing leaf spots",
                        "treatments": [
                            {"type": "fungicide", "action": "Apply copper fungicide"}
                        ],
                        "prevention": ["Improve air circulation"]
                    }
                }
            ],
            "detected_symptoms": [
                {"name": "spots", "confidence": 0.8},
                {"name": "browning", "confidence": 0.7}
            ],
            "treatments": [
                {
                    "type": "fungicide",
                    "action": "Apply fungicide treatment",
                    "urgency": "medium",
                    "details": ["Apply weekly"]
                }
            ],
            "immediate_actions": [
                "Remove affected leaves",
                "Improve air circulation"
            ],
            "prevention_tips": [
                "Water at soil level",
                "Ensure good ventilation"
            ]
        }
        
        # Test complete pipeline
        report = format_diagnosis_report(complete_results)
        summary = create_diagnosis_summary(complete_results)
        recommendation = get_confidence_recommendation("high", "moderate")
        
        # All should complete without error
        self.assertIsInstance(report, str)
        self.assertIsInstance(summary, str)
        self.assertIsInstance(recommendation, str)
        
        # Check integration
        self.assertGreater(len(report), 500)  # Should be substantial
        self.assertIn("moderate", summary.lower())
        self.assertIn("reliable", recommendation.lower())


if __name__ == '__main__':
    # Create comprehensive test suite
    test_classes = [
        TestConfidenceHandling,
        TestDiagnosisReportFormatting,
        TestImageValidation,
        TestTextFormatting,
        TestAdvancedFormatting,
        TestErrorHandling,
        TestIntegrationUtilities
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)