"""
Unit tests for plant_health_analyzer.py

Tests symptom detection, condition matching, and treatment generation.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from plant_health_analyzer import PlantHealthAnalyzer
    from plant_database import PlantDatabase
except ImportError as e:
    print(f"Import warning: {e}")


class TestPlantHealthAnalyzer(unittest.TestCase):
    """Test PlantHealthAnalyzer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = PlantHealthAnalyzer()
        
        # Sample analysis texts for testing
        self.healthy_analysis = "The plant appears healthy with no visible signs of disease or problems. Leaves are green and vibrant."
        
        self.fungal_analysis = "The plant shows clear signs of fungal infection with brown circular spots on the leaves. The spots have dark borders and appear to be spreading."
        
        self.nutrient_analysis = "The plant displays yellowing of older leaves starting from the tips, indicating possible nitrogen deficiency."
        
        self.bacterial_analysis = "Water-soaked lesions with yellow halos are visible on the leaves, suggesting bacterial infection."
        
        self.environmental_analysis = "The plant shows wilting and brown leaf edges, likely from water stress or excessive heat."
    
    def test_analyzer_initialization(self):
        """Test analyzer initializes with proper patterns"""
        self.assertIsNotNone(self.analyzer.symptom_patterns)
        self.assertIsNotNone(self.analyzer.severity_keywords)
        self.assertIsInstance(self.analyzer.symptom_patterns, dict)
        self.assertIsInstance(self.analyzer.severity_keywords, dict)
        
        # Check key patterns exist
        expected_patterns = [
            "fungal_infection", "bacterial_infection", "yellowing", 
            "browning", "spots", "wilting"
        ]
        for pattern in expected_patterns:
            self.assertIn(pattern, self.analyzer.symptom_patterns)
    
    def test_healthy_plant_detection(self):
        """Test detection of healthy plants"""
        result = self.analyzer.process_analysis(
            self.healthy_analysis, "general_diagnosis", ""
        )
        
        self.assertEqual(result["severity_level"], "none")
        self.assertTrue(any(
            symptom["name"] == "healthy_plant" 
            for symptom in result["detected_symptoms"]
        ))
        self.assertIn("confidence_score", result)
    
    def test_fungal_infection_detection(self):
        """Test detection of fungal infections"""
        result = self.analyzer.process_analysis(
            self.fungal_analysis, "disease_focused", ""
        )
        
        self.assertNotEqual(result["severity_level"], "none")
        
        # Check for fungal symptoms
        symptom_names = [s["name"] for s in result["detected_symptoms"]]
        self.assertTrue(
            "fungal_infection" in symptom_names or 
            "spots" in symptom_names or 
            "browning" in symptom_names
        )
        
        # Check conditions
        self.assertGreater(len(result["possible_conditions"]), 0)
        self.assertGreater(len(result["treatments"]), 0)
    
    def test_nutrient_deficiency_detection(self):
        """Test detection of nutrient deficiencies"""
        result = self.analyzer.process_analysis(
            self.nutrient_analysis, "nutrient_focused", ""
        )
        
        symptom_names = [s["name"] for s in result["detected_symptoms"]]
        self.assertIn("yellowing", symptom_names)
        
        # Should suggest nutrient-related treatments
        self.assertGreater(len(result["treatments"]), 0)
    
    def test_bacterial_infection_detection(self):
        """Test detection of bacterial infections"""
        result = self.analyzer.process_analysis(
            self.bacterial_analysis, "disease_focused", ""
        )
        
        symptom_names = [s["name"] for s in result["detected_symptoms"]]
        self.assertTrue(
            "bacterial_infection" in symptom_names or
            any("bacterial" in name for name in symptom_names)
        )
    
    def test_environmental_stress_detection(self):
        """Test detection of environmental stress"""
        result = self.analyzer.process_analysis(
            self.environmental_analysis, "environmental_focused", ""
        )
        
        symptom_names = [s["name"] for s in result["detected_symptoms"]]
        self.assertTrue(
            "wilting" in symptom_names or 
            "browning" in symptom_names
        )
    
    def test_severity_assessment(self):
        """Test severity level assessment"""
        # Test mild severity
        mild_analysis = "The plant has a few yellow spots on lower leaves."
        result = self.analyzer.process_analysis(mild_analysis, "general_diagnosis", "")
        
        # Should be mild or none
        self.assertIn(result["severity_level"], ["none", "mild", "moderate"])
        
        # Test severe analysis
        severe_analysis = "The plant is dying with extensive black rot covering most leaves and severe wilting."
        result = self.analyzer.process_analysis(severe_analysis, "general_diagnosis", "")
        
        # Should detect higher severity
        self.assertIn(result["severity_level"], ["moderate", "high", "critical"])
    
    def test_symptom_extraction_patterns(self):
        """Test individual symptom pattern matching"""
        test_cases = [
            ("The leaves are yellowing", "yellowing"),
            ("Brown spots on foliage", "spots"),
            ("Plant is wilting badly", "wilting"),
            ("Fungal infection detected", "fungal_infection"),
            ("Bacterial lesions present", "bacterial_infection")
        ]
        
        for text, expected_symptom in test_cases:
            symptoms = self.analyzer._extract_symptoms(text)
            symptom_names = [s["name"] for s in symptoms]
            self.assertIn(expected_symptom, symptom_names, 
                         f"Failed to detect {expected_symptom} in '{text}'")
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # Test with clear symptoms
        clear_analysis = "The plant has definite fungal infection with multiple brown spots."
        result = self.analyzer.process_analysis(clear_analysis, "disease_focused", "")
        
        self.assertIn("confidence_score", result)
        self.assertIn(result["confidence_score"], ["low", "medium", "high"])
    
    def test_treatment_generation(self):
        """Test treatment recommendation generation"""
        disease_analysis = "Fungal leaf spot disease with brown circular lesions."
        result = self.analyzer.process_analysis(disease_analysis, "disease_focused", "")
        
        self.assertGreater(len(result["treatments"]), 0)
        
        for treatment in result["treatments"]:
            self.assertIn("type", treatment)
            self.assertIn("action", treatment)
            self.assertIn("urgency", treatment)
    
    def test_immediate_actions_generation(self):
        """Test immediate action recommendations"""
        urgent_analysis = "Severe fungal infection spreading rapidly across leaves."
        result = self.analyzer.process_analysis(urgent_analysis, "disease_focused", "")
        
        self.assertGreater(len(result["immediate_actions"]), 0)
        
        # Should contain actionable items
        actions = result["immediate_actions"]
        self.assertTrue(any("remove" in action.lower() for action in actions))
    
    def test_prevention_tips_generation(self):
        """Test prevention tip generation"""
        result = self.analyzer.process_analysis(
            self.fungal_analysis, "disease_focused", ""
        )
        
        self.assertGreater(len(result["prevention_tips"]), 0)
        
        # Should contain preventive measures
        tips = result["prevention_tips"]
        self.assertTrue(any("prevent" in tip.lower() or "avoid" in tip.lower() for tip in tips))
    
    def test_context_consideration(self):
        """Test plant context consideration"""
        context = "tomato plant in greenhouse"
        result = self.analyzer.process_analysis(
            self.fungal_analysis, "disease_focused", context
        )
        
        # Should process without error and include context
        self.assertIsInstance(result, dict)
        self.assertIn("analysis_type", result)
    
    def test_empty_analysis_handling(self):
        """Test handling of empty or minimal analysis"""
        empty_result = self.analyzer.process_analysis("", "general_diagnosis", "")
        
        # Should handle gracefully
        self.assertIsInstance(empty_result, dict)
        self.assertIn("severity_level", empty_result)
        
        minimal_result = self.analyzer.process_analysis("plant", "general_diagnosis", "")
        self.assertIsInstance(minimal_result, dict)
    
    def test_multiple_symptoms_detection(self):
        """Test detection of multiple symptoms"""
        complex_analysis = "The plant has yellowing leaves with brown spots and shows signs of wilting."
        result = self.analyzer.process_analysis(complex_analysis, "general_diagnosis", "")
        
        symptom_names = [s["name"] for s in result["detected_symptoms"]]
        
        # Should detect multiple symptoms
        expected_symptoms = ["yellowing", "spots", "wilting"]
        detected_count = sum(1 for symptom in expected_symptoms if symptom in symptom_names)
        self.assertGreater(detected_count, 1)
    
    def test_negative_context_handling(self):
        """Test handling of negative contexts (no disease present)"""
        negative_analysis = "No signs of disease visible, no spots, no wilting, plant looks healthy."
        result = self.analyzer.process_analysis(negative_analysis, "general_diagnosis", "")
        
        # Should detect as healthy despite mentioning symptoms in negative context
        self.assertEqual(result["severity_level"], "none")


class TestSymptomPatternMatching(unittest.TestCase):
    """Test symptom pattern matching specifically"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = PlantHealthAnalyzer()
    
    def test_pattern_regex_validity(self):
        """Test that all symptom patterns are valid regex"""
        import re
        
        for symptom_name, pattern in self.analyzer.symptom_patterns.items():
            try:
                re.compile(pattern)
            except re.error as e:
                self.fail(f"Invalid regex pattern for {symptom_name}: {e}")
    
    def test_symptom_confidence_scoring(self):
        """Test symptom confidence scoring"""
        # Test specific symptom matches
        test_text = "clear signs of fungal infection"
        symptoms = self.analyzer._extract_symptoms(test_text)
        
        if symptoms:
            for symptom in symptoms:
                self.assertIn("confidence", symptom)
                self.assertIsInstance(symptom["confidence"], (int, float))
                self.assertGreaterEqual(symptom["confidence"], 0)
                self.assertLessEqual(symptom["confidence"], 1)
    
    def test_definitive_problem_detection(self):
        """Test detection of definitive problems"""
        definitive_cases = [
            "fungal infection",
            "bacterial disease", 
            "viral infection",
            "severe blight"
        ]
        
        for case in definitive_cases:
            has_problems = self.analyzer._has_definitive_problems(case)
            self.assertTrue(has_problems, f"Failed to detect definitive problem in: {case}")
    
    def test_implicit_problem_detection(self):
        """Test detection of implicit problems"""
        implicit_cases = [
            "brown leaf edges",
            "yellow leaf tips",
            "plant damage visible"
        ]
        
        for case in implicit_cases:
            has_problems = self.analyzer._has_implicit_problems(case)
            self.assertTrue(has_problems, f"Failed to detect implicit problem in: {case}")


class TestConditionMatching(unittest.TestCase):
    """Test condition matching and scoring"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = PlantHealthAnalyzer()
    
    def test_healthy_condition_matching(self):
        """Test matching for healthy plants"""
        healthy_symptoms = [{"name": "healthy_plant", "confidence": 0.9}]
        conditions = self.analyzer._match_conditions(healthy_symptoms, "", "")
        
        self.assertGreater(len(conditions), 0)
        self.assertEqual(conditions[0]["name"], "healthy_plant")
        self.assertGreater(conditions[0]["score"], 5)
    
    def test_disease_condition_matching(self):
        """Test matching for disease conditions"""
        disease_symptoms = [
            {"name": "fungal_infection", "confidence": 0.8},
            {"name": "spots", "confidence": 0.7}
        ]
        
        conditions = self.analyzer._match_conditions(disease_symptoms, "tomato", "fungal infection")
        
        self.assertGreater(len(conditions), 0)
        
        # Should prioritize conditions with higher scores
        scores = [c["score"] for c in conditions]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_condition_info_structure(self):
        """Test that condition info has proper structure"""
        symptoms = [{"name": "fungal_infection", "confidence": 0.8}]
        conditions = self.analyzer._match_conditions(symptoms, "", "")
        
        if conditions:
            condition = conditions[0]
            self.assertIn("name", condition)
            self.assertIn("score", condition)
            self.assertIn("info", condition)
            self.assertIn("confidence", condition)
            
            info = condition["info"]
            self.assertIn("description", info)


if __name__ == '__main__':
    unittest.main(verbosity=2)