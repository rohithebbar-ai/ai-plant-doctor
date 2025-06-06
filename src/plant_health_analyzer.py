# plant_health_analyzer.py - Part 1 (First Half) - FIXED VERSION

import re
import logging
from typing import Dict, List, Any
from plant_database import PlantDatabase

logger = logging.getLogger(__name__)

class PlantHealthAnalyzer:
    def __init__(self):
        """Initialize plant health analyzer with improved diagnostic logic"""
        self.plant_db = PlantDatabase()
        
        # Get all conditions from database for dynamic symptom patterns
        self.all_conditions = self.plant_db.get_all_conditions()
        
        # Build dynamic symptom patterns from database
        self.symptom_patterns = self._build_symptom_patterns_from_db()
        
        # Severity assessment keywords (enhanced from database)
        self.severity_keywords = {
            "critical": ["dying", "dead", "severe", "extensive", "widespread", "covering most", "emergency"],
            "high": ["spreading rapidly", "many leaves", "progressing", "getting worse", "significant", "urgent"],
            "moderate": ["several leaves", "noticeable", "some spread", "moderate", "multiple"],
            "mild": ["few leaves", "early stage", "beginning", "slight", "minor", "starting"]
        }
        
        # Diagnostic exclusion rules - conditions that rarely occur together
        self.exclusion_rules = {
            "fungal_leaf_spot": ["bacterial_spot", "viral_mosaic"],  # Reduce likelihood of co-occurrence
            "bacterial_spot": ["fungal_leaf_spot", "viral_mosaic"],
            "powdery_mildew": ["bacterial_wilt", "root_rot"],
            "viral_mosaic": ["bacterial_spot", "fungal_leaf_spot"],
            "insect_damage": [],  # Can co-occur with diseases as secondary issue
        }
        
        # Condition categories for better logic
        self.condition_categories = {
            "fungal": ["fungal_leaf_spot", "powdery_mildew", "rust_disease", "black_spot", "root_rot"],
            "bacterial": ["bacterial_spot", "bacterial_wilt", "fire_blight"],
            "viral": ["viral_mosaic", "leaf_curl_virus", "stunting_virus"],
            "insect": ["insect_damage", "aphid_damage", "spider_mites"],
            "environmental": ["nutrient_deficiency", "water_stress", "light_stress", "heat_stress"],
            "nutritional": ["nitrogen_deficiency", "potassium_deficiency", "iron_deficiency", "magnesium_deficiency"]
        }
    
    def _build_symptom_patterns_from_db(self) -> Dict[str, str]:
        """Build more specific symptom detection patterns from database"""
        patterns = {}
        
        # Extract patterns from all database conditions
        for condition_name, condition_info in self.all_conditions.items():
            # Add condition name as pattern
            clean_name = condition_name.replace('_', ' ')
            patterns[condition_name] = rf"\b({re.escape(clean_name)}|{re.escape(condition_name)})\b"
            
            # Add symptoms from database with higher specificity
            for symptom in condition_info.get("symptoms", []):
                symptom_key = f"{condition_name}_{symptom.replace(' ', '_')}"
                # Make patterns more specific to reduce false matches
                patterns[symptom_key] = rf"\b{re.escape(symptom)}\b"
            
            # Add keywords from database
            for keyword in condition_info.get("keywords", []):
                keyword_key = f"{condition_name}_keyword_{keyword.replace(' ', '_')}"
                patterns[keyword_key] = rf"\b{re.escape(keyword)}\b"
        
        # Add more specific general symptom patterns
        specific_patterns = {
            # More specific fungal indicators
            "fungal_infection": r"\b(fungal infection|fungal disease|fungus growing|moldy|mold growth)\b",
            "fungal_spots": r"\b(fuzzy spots|circular spots with.*center|brown spots.*fuzzy)\b",
            
            # More specific bacterial indicators  
            "bacterial_infection": r"\b(bacterial infection|bacterial disease|water-soaked|oozing|bacterial ooze)\b",
            "bacterial_spots": r"\b(water.soaked.*spots|dark spots.*yellow halo|shot.hole)\b",
            
            # More specific viral indicators
            "viral_infection": r"\b(viral infection|viral disease|mosaic pattern|mottled leaves)\b",
            "viral_symptoms": r"\b(mosaic|mottling|stunted.*growth|leaf.*curl.*virus)\b",
            
            # More specific insect indicators
            "insect_damage": r"\b(chewed.*leaves|holes.*eaten|insect.*bite|pest.*damage)\b",
            "insect_feeding": r"\b(feeding.*damage|eaten.*holes|nibbled|gnawed)\b",
            
            # Keep general patterns but make them less aggressive
            "general_browning": r"\b(brown|browning)\b.*\b(edges?|margins?|tips?)\b",
            "general_yellowing": r"\b(yellow|yellowing)\b.*\b(leaves?|foliage)\b",
            "general_spots": r"\b(spots?|lesions?)\b(?!\s*of\s)",  # Exclude "spots of" 
            "general_wilting": r"\b(wilt|wilting|drooping)\b"
        }
        
        patterns.update(specific_patterns)
        return patterns
    
    def process_analysis(self, raw_analysis: str, analysis_type: str, plant_context: str) -> Dict[str, Any]:
        """Process analysis with improved diagnostic logic - FIXED VERSION"""
        try:
            logger.info(f"Processing {analysis_type} analysis with improved diagnostic logic")
            logger.info(f"Raw analysis: {raw_analysis}")
            
            # Handle empty or error cases
            if not raw_analysis or len(raw_analysis.strip()) < 10:
                logger.warning("Raw analysis is too short or empty")
                return self._create_fallback_response(raw_analysis, analysis_type)
            
            # Clean and normalize the analysis text
            cleaned_analysis = self._clean_analysis_text(raw_analysis)
            
            # Extract symptoms from the analysis using database patterns
            detected_symptoms = self._extract_symptoms_from_db(cleaned_analysis)
            
            # Assess initial severity using database information
            initial_severity = self._assess_severity_with_db(cleaned_analysis, detected_symptoms)
            
            # NEW: Improved condition matching with realistic scoring
            possible_conditions = self._match_conditions_realistically(detected_symptoms, plant_context, cleaned_analysis)
            
            # ADJUST SEVERITY BASED ON CONFIDENCE
            if possible_conditions:
                primary_confidence = possible_conditions[0].get("confidence", 0.3)
                severity_level = self._adjust_severity_for_confidence(initial_severity, primary_confidence)
                logger.info(f"Adjusted severity from {initial_severity} to {severity_level} based on confidence {primary_confidence:.2f}")
            else:
                severity_level = initial_severity
            
            # Generate treatments with confidence-adjusted urgency
            treatments = self._generate_treatments_from_db_with_confidence(possible_conditions, severity_level)
            
            # Create actionable advice from database
            immediate_actions = self._generate_immediate_actions_from_db(detected_symptoms, severity_level, possible_conditions)
            prevention_tips = self._generate_prevention_tips_from_db(possible_conditions)
            
            # Calculate overall confidence (fixed version)
            confidence = self._calculate_overall_confidence(detected_symptoms, possible_conditions)
            
            return {
                "raw_analysis": raw_analysis,
                "detected_symptoms": detected_symptoms,
                "severity_level": severity_level,
                "possible_conditions": possible_conditions,
                "treatments": treatments,
                "immediate_actions": immediate_actions,
                "prevention_tips": prevention_tips,
                "confidence_score": confidence,
                "analysis_type": analysis_type,
                "recommendations": self._format_realistic_recommendations(
                    possible_conditions, treatments, immediate_actions, severity_level
                )
            }
            
        except Exception as e:
            logger.error(f"Error in process_analysis: {e}")
            return self._create_fallback_response(raw_analysis, analysis_type, str(e))
    
    def _match_conditions_realistically(self, symptoms: List[Dict], plant_context: str, analysis_text: str) -> List[Dict[str, Any]]:
        """NEW: Match conditions with realistic diagnostic logic"""
        
        # Handle healthy plants first
        if any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
            return [{
                "name": "healthy_plant",
                "score": 10.0,
                "matched_symptoms": ["healthy_plant"],
                "info": {
                    "description": "Plant appears healthy with no visible signs of disease or stress",
                    "treatments": [],
                    "prevention": self.plant_db.get_general_advice("preventive")
                },
                "confidence": 0.9,
                "source": "database_healthy",
                "category": "healthy"
            }]
        
        # Get initial matches from database
        symptom_names = [s["name"] for s in symptoms]
        database_matches = self.plant_db.search_by_symptoms(symptom_names)
        
        # Score all conditions
        condition_scores = {}
        for condition_name, condition_info, base_score in database_matches:
            enhanced_score = self._calculate_enhanced_condition_score(
                condition_info, symptoms, plant_context, analysis_text, base_score
            )
            
            if enhanced_score > 0:
                # Determine condition category
                category = self._get_condition_category(condition_name)
                
                condition_scores[condition_name] = {
                    "name": condition_name,
                    "score": enhanced_score,
                    "matched_symptoms": self._get_matched_symptoms(condition_info, symptoms),
                    "info": condition_info,
                    "confidence": min(enhanced_score / 10.0, 1.0),
                    "source": "database_match",
                    "category": category
                }
        
        # Apply realistic diagnostic logic
        final_conditions = self._apply_diagnostic_hierarchy(condition_scores, symptoms, analysis_text)
        
        # Add plant-specific conditions if relevant
        if plant_context:
            plant_specific = self._get_plant_specific_conditions(plant_context, symptoms)
            final_conditions.extend(plant_specific)
        
        # If no conditions found, create generic ones
        if not final_conditions:
            final_conditions = self._create_generic_conditions(symptoms, analysis_text)
        
        # Sort by score and return top matches
        return sorted(final_conditions, key=lambda x: x["score"], reverse=True)[:3]
    
    def _apply_diagnostic_hierarchy(self, condition_scores: Dict, symptoms: List[Dict], analysis_text: str) -> List[Dict]:
        """Apply realistic diagnostic hierarchy and exclusion rules"""
        
        if not condition_scores:
            return []
        
        # Sort conditions by score
        sorted_conditions = sorted(condition_scores.values(), key=lambda x: x["score"], reverse=True)
        
        # Start with the highest scoring condition as primary
        primary_condition = sorted_conditions[0]
        final_conditions = [primary_condition]
        
        logger.info(f"Primary diagnosis: {primary_condition['name']} (score: {primary_condition['score']:.1f})")
        
        # For remaining conditions, apply exclusion rules and category logic
        for condition in sorted_conditions[1:]:
            should_include = True
            adjusted_confidence = condition["confidence"]
            
            # Check exclusion rules with primary condition
            primary_name = primary_condition["name"]
            condition_name = condition["name"]
            
            # Apply exclusion rules - reduce confidence if conditions typically don't co-occur
            if primary_name in self.exclusion_rules:
                if condition_name in self.exclusion_rules[primary_name]:
                    # Reduce confidence significantly for excluded combinations
                    adjusted_confidence *= 0.3
                    logger.info(f"Reduced confidence for {condition_name} due to exclusion with {primary_name}")
            
            # Category-based logic
            primary_category = primary_condition["category"]
            condition_category = condition["category"]
            
            # If same category (e.g., both fungal), reduce confidence of secondary
            if primary_category == condition_category and primary_category in ["fungal", "bacterial", "viral"]:
                adjusted_confidence *= 0.4
                logger.info(f"Reduced confidence for {condition_name} - same category as primary")
            
            # Environmental and nutritional can co-occur with diseases
            if condition_category in ["environmental", "nutritional"]:
                # These can be secondary to primary diseases
                adjusted_confidence *= 0.7
            
            # Insect damage can be secondary to diseases (stress attracts pests)
            if condition_category == "insect" and primary_category in ["fungal", "bacterial"]:
                adjusted_confidence *= 0.6
                condition["info"]["description"] += " (possibly secondary to primary condition)"
            
            # Only include if confidence is still reasonable after adjustments
            if adjusted_confidence > 0.25:  # Minimum threshold
                condition["confidence"] = adjusted_confidence
                condition["score"] = condition["score"] * adjusted_confidence  # Adjust score too
                
                # Mark as secondary condition
                if len(final_conditions) >= 1:
                    condition["role"] = "secondary"
                else:
                    condition["role"] = "primary"
                
                final_conditions.append(condition)
                logger.info(f"Added secondary condition: {condition_name} (adjusted confidence: {adjusted_confidence:.2f})")
            else:
                logger.info(f"Excluded {condition_name} - confidence too low after adjustments ({adjusted_confidence:.2f})")
            
            # Limit to maximum 3 conditions total
            if len(final_conditions) >= 3:
                break
        
        return final_conditions
    
    def _adjust_severity_for_confidence(self, severity: str, primary_confidence: float) -> str:
        """Adjust severity based on diagnostic confidence"""
        
        # If confidence is very low, reduce severity
        if primary_confidence < 0.4:  # Less than 40% confidence
            if severity == "critical":
                return "high"
            elif severity == "high":
                return "moderate"
            elif severity == "moderate":
                return "mild"
            else:
                return severity
        
        # If confidence is low, slightly reduce severity
        elif primary_confidence < 0.6:  # Less than 60% confidence
            if severity == "critical":
                return "high"
            elif severity == "high":
                return "moderate"
            else:
                return severity
        
        # Good confidence, keep original severity
        return severity
    
    def _get_condition_category(self, condition_name: str) -> str:
        """Determine the category of a condition"""
        for category, conditions in self.condition_categories.items():
            if condition_name in conditions:
                return category
        return "other"
    
    def _calculate_enhanced_condition_score(self, condition_info: Dict, symptoms: List[Dict], 
                                         plant_context: str, analysis_text: str, base_score: float) -> float:
        """Calculate enhanced condition score with better specificity"""
        score = base_score
        
        # Symptom matching with better weighting
        condition_symptoms = set(condition_info.get("symptoms", []))
        condition_keywords = set(condition_info.get("keywords", []))
        
        specific_matches = 0
        general_matches = 0
        
        for symptom in symptoms:
            symptom_name = symptom["name"]
            symptom_confidence = symptom["confidence"]
            
            # Check for specific symptom matches (higher weight)
            if symptom_name in condition_symptoms:
                score += symptom_confidence * 4  # Higher weight for specific matches
                specific_matches += 1
            
            # Check for keyword matches (lower weight)
            for keyword in condition_keywords:
                if keyword in symptom["text_match"]:
                    score += symptom_confidence * 1.5  # Lower weight for keyword matches
                    general_matches += 1
        
        # Bonus for specific matches, penalty for only general matches
        if specific_matches > 0:
            score += specific_matches * 2  # Bonus for specific diagnostic features
        elif general_matches > 0:
            score *= 0.7  # Reduce score if only general symptoms
        
        # Plant context bonus (smaller impact)
        if plant_context:
            common_plants = condition_info.get("common_plants", [])
            for plant in common_plants:
                if plant.lower() in plant_context.lower():
                    score += 1
        
        # Analysis text keyword matching (reduced impact)
        analysis_lower = analysis_text.lower()
        keyword_matches = 0
        for keyword in condition_keywords:
            if keyword.lower() in analysis_lower:
                keyword_matches += 1
        
        # Diminishing returns for keyword matches
        if keyword_matches > 0:
            score += min(keyword_matches * 0.5, 2.0)  # Cap keyword bonus
        
        return max(score, 0)  # Ensure non-negative
    
    def _determine_treatment_urgency(self, treatment: Dict, severity: str, confidence: float = 0.7) -> str:
        """FIXED: Determine treatment urgency based on type, severity, AND confidence"""
        treatment_type = treatment.get("type", "general")
        
        # Lower urgency if confidence is low
        confidence_modifier = 1.0
        if confidence < 0.4:
            confidence_modifier = 0.5  # Much lower urgency
        elif confidence < 0.6:
            confidence_modifier = 0.75  # Somewhat lower urgency
        
        # Base urgency
        if treatment_type in ["emergency", "removal"] or severity == "critical":
            base_urgency = "emergency"
        elif treatment_type in ["fungicide", "bactericide", "antibiotic"] or severity == "high":
            base_urgency = "high"
        elif treatment_type in ["cultural", "organic", "fertilizer"] or severity == "moderate":
            base_urgency = "medium"
        else:
            base_urgency = "low"
        
        # Apply confidence modifier
        urgency_levels = ["low", "medium", "high", "emergency"]
        current_level = urgency_levels.index(base_urgency)
        
        # Reduce urgency based on confidence
        if confidence_modifier < 1.0:
            reduction = int((1.0 - confidence_modifier) * 2)  # Reduce by 1-2 levels
            new_level = max(0, current_level - reduction)
            return urgency_levels[new_level]
        
        return base_urgency
    
    def _calculate_overall_confidence(self, symptoms: List[Dict], conditions: List[Dict]) -> str:
        """Calculate overall confidence - FIXED VERSION"""
        try:
            if not symptoms or not conditions:
                return "low"
            
            # Get primary condition confidence
            primary_condition = conditions[0]
            primary_confidence = primary_condition.get("confidence", 0.3)
            
            # Convert to descriptive confidence based on actual numbers
            if primary_confidence > 0.7:
                return "high"
            elif primary_confidence > 0.5:
                return "medium"
            elif primary_confidence > 0.3:
                return "moderate"
            else:
                return "low"
                
        except Exception:
            return "low"
    
    def _generate_treatments_from_db_with_confidence(self, conditions: List[Dict], severity: str) -> List[Dict[str, Any]]:
        """Generate treatments considering both severity and confidence"""
        treatments = []
        
        try:
            primary_confidence = conditions[0].get("confidence", 0.3) if conditions else 0.3
            
            # Only use primary condition for low confidence diagnoses
            conditions_to_process = conditions[:1] if primary_confidence < 0.5 else conditions[:2]
            
            for condition in conditions_to_process:
                condition_info = condition.get("info", {})
                condition_treatments = condition_info.get("treatments", [])
                
                for treatment in condition_treatments:
                    # FIXED: Pass confidence parameter
                    urgency = self._determine_treatment_urgency(treatment, severity, primary_confidence)
                    
                    # Modify action text based on confidence
                    action = treatment.get("action", "")
                    if primary_confidence < 0.4:
                        # Very low confidence - suggest consideration only
                        if action:
                            action = f"Consider {action.lower()}" if not action.lower().startswith('consider') else action
                        else:
                            action = "Monitor and consider treatment options"
                    elif primary_confidence < 0.6:
                        # Low confidence - suggest probable need
                        if action:
                            action = f"Likely need to {action.lower()}" if not action.lower().startswith('likely') else action
                        else:
                            action = "Probably needs treatment"
                    
                    treatments.append({
                        "type": treatment.get("type", "general"),
                        "action": action,
                        "details": treatment.get("details", []),
                        "products": treatment.get("products", []),
                        "urgency": urgency,
                        "condition": condition["name"],
                        "source": "database"
                    })
            
            # Add monitoring advice for low confidence
            if primary_confidence < 0.5:
                treatments.append({
                    "type": "monitoring",
                    "action": "Monitor closely and gather more evidence before treatment",
                    "details": [
                        "Take daily photos to track symptom progression",
                        "Note environmental conditions (watering, light, temperature)",
                        "Document any changes over 3-5 days",
                        "Consider consulting a local plant expert for confirmation"
                    ],
                    "urgency": "medium",
                    "source": "low_confidence_advice"
                })
            
            # Add general care if no specific treatments
            if not treatments:
                general_advice = self.plant_db.get_general_advice("moderate")
                treatments.append({
                    "type": "general_care",
                    "action": "Provide general plant care while monitoring",
                    "details": general_advice[:3],
                    "urgency": "medium",
                    "source": "database_general"
                })
                    
        except Exception as e:
            logger.error(f"Error generating treatments from database: {e}")
            treatments = [{
                "type": "general_care",
                "action": "Monitor plant and provide basic care",
                "details": ["Water appropriately", "Ensure good light", "Watch for changes"],
                "urgency": "low",
                "source": "fallback"
            }]
        
        return treatments
    
    def _format_realistic_recommendations(self, conditions: List[Dict], treatments: List[Dict], 
                                        actions: List[str], severity: str) -> str:
        """Format recommendations with realistic diagnostic confidence"""
        try:
            recommendations = []
            
            # Primary diagnosis
            if conditions:
                primary_condition = conditions[0]
                condition_name = primary_condition['name'].replace('_', ' ').title()
                confidence = primary_condition.get('confidence', 0.5)
                role = primary_condition.get('role', 'primary')
                
                recommendations.append(f"**Primary Diagnosis**: {condition_name}")
                recommendations.append(f"**Confidence**: {confidence:.0%}")
                
                # Secondary conditions
                if len(conditions) > 1:
                    secondary_conditions = []
                    for condition in conditions[1:]:
                        sec_name = condition['name'].replace('_', ' ').title()
                        sec_confidence = condition.get('confidence', 0.3)
                        secondary_conditions.append(f"{sec_name} ({sec_confidence:.0%})")
                    
                    recommendations.append(f"**Secondary Concerns**: {', '.join(secondary_conditions)}")
                
                # Recovery time if available
                condition_info = primary_condition.get("info", {})
                recovery_time = condition_info.get("recovery_time", {})
                if recovery_time and severity in recovery_time:
                    recommendations.append(f"**Expected Recovery**: {recovery_time[severity]}")
            
            # Severity with realistic assessment
            severity_desc = {
                "critical": "Immediate attention required",
                "high": "Prompt treatment needed", 
                "moderate": "Monitor and treat",
                "mild": "Watch closely",
                "none": "No immediate concerns"
            }
            recommendations.append(f"**Severity**: {severity.title()} - {severity_desc.get(severity, 'Assessment needed')}")
            
            # Key treatments from primary diagnosis
            if treatments:
                recommendations.append("**Recommended Actions**:")
                for treatment in treatments[:2]:  # Top 2 treatments
                    action = treatment.get('action', 'No action specified')
                    urgency = treatment.get('urgency', 'medium')
                    urgency_icon = {"emergency": "🚨", "high": "⚠️", "medium": "⚖️", "low": "📋"}.get(urgency, "📋")
                    recommendations.append(f"• {urgency_icon} {action}")
            
            # Immediate actions (top 3)
            if actions:
                recommendations.append("**Next Steps**:")
                for action in actions[:3]:
                    recommendations.append(f"• {action}")
            
            return "\n".join(recommendations)
            
        except Exception as e:
            logger.error(f"Error formatting recommendations: {e}")
            return f"**Analysis Type**: {severity}\n**Status**: Analysis completed\n**Recommendation**: Follow care instructions and monitor plant condition"
    
    def _extract_symptoms_from_db(self, analysis: str) -> List[Dict[str, Any]]:
        """Extract symptoms using database-driven patterns"""
        symptoms = []
        
        if not analysis or len(analysis.strip()) < 5:
            logger.warning("Analysis text too short for symptom extraction")
            return symptoms
            
        analysis_lower = analysis.lower()
        logger.info(f"Analyzing text for symptoms using database patterns")
        
        # Check for healthy indicators first
        healthy_indicators = [
            r"\bhealthy\s+plant\b", r"\bappears\s+healthy\b", r"\blooks\s+healthy\b", 
            r"\bno\s+signs?\s+of\s+(disease|problems|issues)\b",
            r"\bno\s+visible\s+(problems|disease|damage)\b",
            r"\bplant\s+is\s+healthy\b", r"\bgood\s+health\b"
        ]
        
        has_explicit_healthy = any(re.search(pattern, analysis_lower) for pattern in healthy_indicators)
        
        if has_explicit_healthy and not self._has_definitive_problems(analysis_lower):
            logger.info("Plant identified as explicitly healthy")
            return [{
                "name": "healthy_plant",
                "text_match": "plant appears healthy",
                "confidence": 0.9,
                "source": "direct_observation"
            }]
        
        # Extract symptoms using database patterns
        for symptom_name, pattern in self.symptom_patterns.items():
            try:
                matches = list(re.finditer(pattern, analysis_lower, re.IGNORECASE))
                for match in matches:
                    match_text = match.group()
                    
                    # Skip if in negative context
                    surrounding_text = analysis_lower[max(0, match.start()-30):match.end()+30]
                    if self._is_negative_context(surrounding_text, match_text):
                        continue
                    
                    confidence = self._calculate_symptom_confidence_with_db(match_text, symptom_name, analysis_lower)
                    
                    symptoms.append({
                        "name": symptom_name,
                        "text_match": match_text,
                        "confidence": confidence,
                        "source": "database_pattern"
                    })
                    
                    logger.info(f"Found symptom: {symptom_name} - '{match_text}' (confidence: {confidence})")
            except Exception as e:
                logger.warning(f"Error processing symptom pattern {symptom_name}: {e}")
                continue
        
        # Remove duplicates and sort by confidence
        unique_symptoms = self._deduplicate_symptoms(symptoms)
        
        # If no symptoms found, create default response
        if not unique_symptoms and len(analysis.strip()) > 10:
            if self._has_implicit_problems(analysis_lower):
                unique_symptoms.append({
                    "name": "general_stress",
                    "text_match": "unspecified plant stress detected",
                    "confidence": 0.5,
                    "source": "implicit_detection"
                })
            else:
                unique_symptoms.append({
                    "name": "healthy_plant",
                    "text_match": "no specific problems identified",
                    "confidence": 0.6,
                    "source": "default_assessment"
                })
        
        return sorted(unique_symptoms, key=lambda x: x["confidence"], reverse=True)
    
    def _generate_treatments_from_db(self, conditions: List[Dict], severity: str) -> List[Dict[str, Any]]:
        """LEGACY: Generate treatments using database treatment information (backward compatibility)"""
        treatments = []
        
        try:
            for condition in conditions[:2]:  # Top 2 conditions
                condition_info = condition.get("info", {})
                condition_treatments = condition_info.get("treatments", [])
                
                for treatment in condition_treatments:
                    # FIXED: Use the old method signature for backward compatibility
                    urgency = self._determine_treatment_urgency_legacy(treatment, severity)
                    
                    # Get treatment category info from database
                    treatment_info = self.plant_db.get_treatment_info(treatment.get("type", "general"))
                    
                    treatments.append({
                        "type": treatment.get("type", "general"),
                        "action": treatment.get("action", ""),
                        "details": treatment.get("details", []),
                        "products": treatment.get("products", []),
                        "urgency": urgency,
                        "condition": condition["name"],
                        "category_info": treatment_info,
                        "source": "database"
                    })
            
            # Add general care if no specific treatments
            if not treatments:
                general_advice = self.plant_db.get_general_advice("moderate")
                treatments.append({
                    "type": "general_care",
                    "action": "Provide general plant care",
                    "details": general_advice[:3],
                    "urgency": "medium",
                    "source": "database_general"
                })
                
        except Exception as e:
            logger.error(f"Error generating treatments from database: {e}")
            treatments = [{
                "type": "general_care",
                "action": "Monitor plant and provide basic care",
                "details": ["Water appropriately", "Ensure good light", "Watch for changes"],
                "urgency": "medium",
                "source": "fallback"
            }]
        
        return treatments
    
    def _determine_treatment_urgency_legacy(self, treatment: Dict, severity: str) -> str:
        """LEGACY: Determine treatment urgency (old method for backward compatibility)"""
        treatment_type = treatment.get("type", "general")
        
        # Emergency treatments
        if treatment_type in ["emergency", "removal"] or severity == "critical":
            return "emergency"
        
        # High urgency treatments
        if treatment_type in ["fungicide", "bactericide", "antibiotic"] or severity == "high":
            return "high"
        
        # Medium urgency treatments
        if treatment_type in ["cultural", "organic", "fertilizer"] or severity == "moderate":
            return "medium"
        
        # Low urgency treatments
        return "low"
    
    def _generate_immediate_actions_from_db(self, symptoms: List[Dict], severity: str, conditions: List[Dict]) -> List[str]:
        """Generate immediate actions using database information - UPDATED for confidence"""
        actions = []
        
        try:
            # Handle healthy plants
            if severity == "none" or any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
                return [
                    "✅ Great news! Your plant appears healthy",
                    "🔍 Continue regular monitoring for any changes",
                    "💧 Maintain current watering and care routine",
                    "🌱 Keep up the good work with plant care!"
                ]
            
            # Get confidence level for action modification
            primary_confidence = conditions[0].get("confidence", 0.3) if conditions else 0.3
            
            # Adjust actions based on confidence
            if primary_confidence < 0.4:
                # Very low confidence - conservative actions
                actions = [
                    "🔍 Monitor plant closely - diagnosis uncertain",
                    "📸 Take daily photos to track any changes",
                    "📝 Document symptoms and environmental conditions",
                    "📱 Consider consulting a plant expert for confirmation"
                ]
            elif primary_confidence < 0.6:
                # Low confidence - cautious actions
                actions = [
                    "🔍 Monitor plant closely - likely needs attention",
                    "📸 Document symptoms with photos",
                    "⚠️ Prepare for possible treatment based on symptom progression"
                ]
            else:
                # Good confidence - normal severity-based actions
                severity_advice = self.plant_db.get_general_advice(severity)
                if severity_advice:
                    actions.extend(severity_advice[:2])
                
                # Add emergency actions if needed and confidence is sufficient
                if severity in ["critical", "high"]:
                    emergency_advice = self.plant_db.get_general_advice("emergency")
                    actions.extend(emergency_advice[:1])
                
                # Add condition-specific immediate actions (only primary condition)
                if conditions:
                    primary_condition = conditions[0]
                    condition_info = primary_condition.get("info", {})
                    treatments = condition_info.get("treatments", [])
                    
                    # Find high-urgency treatments
                    for treatment in treatments[:1]:
                        if treatment.get("type") in ["emergency", "removal", "pruning"]:
                            action_text = f"🚨 {treatment.get('action', 'Take immediate action')}"
                            if action_text not in actions:
                                actions.append(action_text)
            
            # Always add monitoring
            if "📋 Take photos to monitor progress" not in actions:
                actions.append("📋 Take photos to monitor progress over next few days")
            
            # Remove duplicates while preserving order
            seen = set()
            unique_actions = []
            for action in actions:
                if action not in seen:
                    seen.add(action)
                    unique_actions.append(action)
            
            return unique_actions[:4]  # Limit to 4 actions
            
        except Exception as e:
            logger.error(f"Error generating immediate actions from database: {e}")
            return [
                "🔍 Monitor plant closely for changes",
                "💧 Check watering needs",
                "📱 Consult plant expert if needed"
            ]
    
    def _generate_prevention_tips_from_db(self, conditions: List[Dict]) -> List[str]:
        """Generate prevention tips using database information"""
        tips = set()
        
        try:
            # Get prevention tips from matched conditions (only primary)
            if conditions:
                primary_condition = conditions[0]
                condition_info = primary_condition.get("info", {})
                condition_prevention = condition_info.get("prevention", [])
                tips.update(condition_prevention[:3])  # Reduced from all to 3
            
            # Add general preventive advice from database
            general_prevention = self.plant_db.get_general_advice("preventive")
            tips.update(general_prevention[:3])  # Reduced from 5 to 3
            
            # Add seasonal advice if available
            import datetime
            current_season = self._get_current_season()
            seasonal_advice = self.plant_db.get_seasonal_advice(current_season)
            tips.update(seasonal_advice[:2])  # Reduced from 3 to 2
            
        except Exception as e:
            logger.error(f"Error generating prevention tips from database: {e}")
            tips = {
                "🔍 Regular plant inspection",
                "💧 Proper watering practices", 
                "🌱 Good plant nutrition"
            }
        
        return list(tips)[:6]  # Reduced from 8 to 6 tips
    
    def _get_plant_specific_conditions(self, plant_context: str, symptoms: List[Dict]) -> List[Dict]:
        """Get conditions specific to mentioned plants"""
        conditions = []
        
        # Extract plant type from context
        plant_words = plant_context.lower().split()
        
        for plant_word in plant_words:
            plant_conditions = self.plant_db.search_by_plant_type(plant_word)
            
            for condition_name, condition_info in plant_conditions:
                # Score based on symptom matches
                score = self._calculate_enhanced_condition_score(condition_info, symptoms, plant_context, "", 1.0)
                
                if score > 0:
                    conditions.append({
                        "name": condition_name,
                        "score": score + 1,  # Bonus for plant-specific
                        "matched_symptoms": self._get_matched_symptoms(condition_info, symptoms),
                        "info": condition_info,
                        "confidence": min(score / 8.0, 1.0),
                        "source": f"plant_specific_{plant_word}",
                        "category": self._get_condition_category(condition_name)
                    })
        
        return conditions
    
    def _create_generic_conditions(self, symptoms: List[Dict], analysis_text: str) -> List[Dict]:
        """Create generic conditions when no database matches found"""
        conditions = []
        
        symptom_names = [s["name"] for s in symptoms]
        
        # Determine generic condition type
        if any("infection" in name for name in symptom_names):
            condition_type = "infection"
            description = "Possible plant infection requiring treatment"
            category = "pathogenic"
        elif any("deficiency" in name for name in symptom_names):
            condition_type = "nutrient_deficiency"
            description = "Possible nutrient deficiency affecting plant health"
            category = "nutritional"
        elif any(name in ["browning", "burning", "wilting"] for name in symptom_names):
            condition_type = "environmental_stress"
            description = "Environmental stress affecting plant condition"
            category = "environmental"
        else:
            condition_type = "general_stress"
            description = "General plant stress condition requiring attention"
            category = "other"
        
        # Get appropriate general advice from database
        general_advice = self.plant_db.get_general_advice("moderate")
        
        conditions.append({
            "name": condition_type,
            "score": 5.0,
            "matched_symptoms": symptom_names,
            "info": {
                "description": description,
                "treatments": [
                    {"type": "general", "action": "Monitor and adjust care", "details": general_advice[:3], "urgency": "medium"}
                ],
                "prevention": self.plant_db.get_general_advice("preventive")[:5]
            },
            "confidence": 0.4,
            "source": "generic_fallback",
            "category": category
        })
        
        return conditions
    
    # Helper methods
    def _get_current_season(self) -> str:
        """Get current season for seasonal advice"""
        import datetime
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"
    
    def _create_fallback_response(self, raw_analysis: str, analysis_type: str, error_msg: str = None) -> Dict[str, Any]:
        """Create fallback response using database general advice"""
        logger.info("Creating fallback response using database")
        
        try:
            general_advice = self.plant_db.get_general_advice("moderate")
            preventive_advice = self.plant_db.get_general_advice("preventive")
            
            return {
                "raw_analysis": raw_analysis or "No analysis available",
                "detected_symptoms": [],
                "severity_level": "unknown",
                "possible_conditions": [{
                    "name": "analysis_incomplete",
                    "score": 3.0,
                    "matched_symptoms": [],
                    "info": {
                        "description": "Unable to complete analysis. Please try with a clearer image or consult an expert.",
                        "treatments": [{"type": "general", "action": "Monitor plant closely", "details": general_advice[:3], "urgency": "medium"}],
                        "prevention": preventive_advice[:5]
                    },
                    "confidence": 0.3,
                    "source": "database_fallback",
                    "category": "unknown"
                }],
                "treatments": [{"type": "general_care", "action": "Provide basic plant care", "details": general_advice[:3], "urgency": "medium", "source": "database_general"}],
                "immediate_actions": ["🔍 Monitor plant daily for any changes", "💧 Maintain consistent watering schedule", "📱 Consider consulting a plant expert for detailed diagnosis"],
                "prevention_tips": preventive_advice[:5],
                "confidence_score": "low",
                "analysis_type": analysis_type,
                "recommendations": f"**Analysis Type**: {analysis_type.replace('_', ' ').title()}\n**Status**: Analysis incomplete\n**Recommendation**: Follow database general care guidelines and monitor closely"
            }
        except Exception as e:
            logger.error(f"Error creating fallback response: {e}")
            return {
                "raw_analysis": raw_analysis or "No analysis available",
                "detected_symptoms": [],
                "severity_level": "unknown",
                "possible_conditions": [],
                "treatments": [],
                "immediate_actions": ["Monitor plant", "Provide basic care"],
                "prevention_tips": ["Regular inspection", "Proper watering"],
                "confidence_score": "low",
                "analysis_type": analysis_type,
                "recommendations": "Analysis failed - consult plant expert"
            }
    
    # Core helper methods (keep all existing ones)
    def _clean_analysis_text(self, analysis: str) -> str:
        """Clean and normalize the analysis text"""
        if not analysis:
            return ""
        analysis = re.sub(r'^.*?Answer:\s*', '', analysis, flags=re.IGNORECASE)
        analysis = re.sub(r'^.*?assistant[:\s]*', '', analysis, flags=re.IGNORECASE)
        analysis = ' '.join(analysis.split())
        return analysis.strip()
    
    def _has_definitive_problems(self, analysis_lower: str) -> bool:
        """Check if analysis contains definitive problems"""
        definitive_problems = [
            r"\bfungal\s+infection\b", r"\bbacterial\s+infection\b", r"\bviral\s+infection\b", 
            r"\bdisease\b(?!\s+resistant)", r"\binfection\b", r"\bblight\b", r"\brust\b(?!\s+resistant)",
            r"\bmildew\b", r"\brot\b(?:ting)?\b", r"\bfungal\b", r"\bbacterial\b", r"\bviral\b"
        ]
        return any(re.search(pattern, analysis_lower) for pattern in definitive_problems)
    
    def _has_implicit_problems(self, analysis_lower: str) -> bool:
        """Check for implicit problem indicators"""
        implicit_problems = [
            r"\bbrown\b.*\b(edge|tip|spot)\b", r"\byellow\b.*\b(leaf|leave)\b", 
            r"\bwilt\b", r"\bdamage\b", r"\bstress\b", r"\bproblem\b", r"\bissue\b"
        ]
        return any(re.search(pattern, analysis_lower) for pattern in implicit_problems)
    
    def _is_negative_context(self, surrounding_text: str, match_text: str) -> bool:
        """Check if symptom match is in negative context"""
        negative_indicators = ['no', 'without', 'absence of', 'not', 'free from', 'clear of']
        try:
            match_pos = surrounding_text.find(match_text)
            if match_pos == -1:
                return False
            words_before = surrounding_text[:match_pos].split()
            recent_words = words_before[-3:] if len(words_before) >= 3 else words_before
            return any(neg_word in recent_words for neg_word in negative_indicators)
        except Exception:
            return False
    
    def _assess_severity_with_db(self, analysis: str, symptoms: List[Dict]) -> str:
        """Assess severity using database information"""
        if not analysis:
            return "none"
            
        analysis_lower = analysis.lower()
        
        if any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
            return "none"
        
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if keyword in analysis_lower:
                    logger.info(f"Found severity keyword '{keyword}' -> {severity}")
                    return severity
        
        for symptom in symptoms:
            symptom_name = symptom["name"]
            for condition_name, condition_info in self.all_conditions.items():
                if symptom_name.startswith(condition_name):
                    treatments = condition_info.get("treatments", [])
                    if any(t.get("type") == "emergency" for t in treatments):
                        return "critical"
                    elif any(t.get("type") in ["removal", "antibiotic"] for t in treatments):
                        return "high"
        
        if len(symptoms) >= 3:
            return "moderate"
        elif len(symptoms) >= 1:
            return "mild"
        else:
            return "none"
    
    def _deduplicate_symptoms(self, symptoms: List[Dict]) -> List[Dict]:
        """Remove duplicate symptoms while preserving highest confidence"""
        seen = {}
        for symptom in symptoms:
            name = symptom["name"]
            if name not in seen or symptom["confidence"] > seen[name]["confidence"]:
                seen[name] = symptom
        return list(seen.values())
    
    def _calculate_symptom_confidence_with_db(self, text_match: str, symptom_name: str, full_analysis: str) -> float:
        """Calculate confidence using database information"""
        base_confidence = 0.7
        
        for condition_name, condition_info in self.all_conditions.items():
            if symptom_name.startswith(condition_name):
                base_confidence = 0.8
                break
        
        if len(text_match) > 10:
            base_confidence += 0.1
        
        if len(text_match) < 5:
            base_confidence -= 0.2
        
        return min(max(base_confidence, 0.1), 1.0)
    
    def _get_matched_symptoms(self, condition_info: Dict, symptoms: List[Dict]) -> List[str]:
        """Get list of symptoms that match this condition"""
        matched = []
        condition_symptoms = set(condition_info.get("symptoms", []))
        condition_keywords = set(condition_info.get("keywords", []))
        
        for symptom in symptoms:
            if (symptom["name"] in condition_symptoms or 
                any(keyword in symptom["text_match"] for keyword in condition_keywords)):
                matched.append(symptom["name"])
        
        return matched