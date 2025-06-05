# plant_health_analyzer_fixed.py - Fixed Plant Health Analysis Processing

import re
import logging
from typing import Dict, List, Any
from plant_database import PlantDatabase

logger = logging.getLogger(__name__)

class PlantHealthAnalyzer:
    def __init__(self):
        """Initialize plant health analyzer with disease database"""
        self.plant_db = PlantDatabase()
        
        # Enhanced symptom detection patterns
        self.symptom_patterns = {
            # Direct disease mentions
            "fungal_infection": r"\b(fungal infection|fungal disease|fungus|fungi)\b",
            "bacterial_infection": r"\b(bacterial infection|bacterial disease|bacteria)\b",
            "viral_infection": r"\b(viral infection|viral disease|virus)\b",
            
            # Specific conditions
            "leaf_spot": r"\b(leaf spot|leaf spots|spots on leaves)\b",
            "rust_disease": r"\b(rust|rust disease|orange spots)\b", 
            "blight": r"\b(blight|blighting)\b",
            "mildew": r"\b(mildew|powdery mildew)\b",
            "soft_rot": r"\b(soft rot|rot|rotting)\b",
            
            # Visual symptoms
            "browning": r"\b(brown|browning|necrosis|necrotic)\b.*\b(edges?|margins?|tips?|leaves?|spots?)\b",
            "yellowing": r"\b(yellow|yellowing|chlorosis|pale)\b.*\b(leaves?|foliage)\b",
            "blackening": r"\b(black|blackening|dark)\b.*\b(spots?|lesions?|areas?|leaves?)\b",
            "burning": r"\b(burn|burning|burnt|scorched|scorch)\b.*\b(edges?|tips?|leaves?)\b",
            "wilting": r"\b(wilt|wilting|drooping|sagging)\b",
            "curling": r"\b(curl|curling|rolled|twisted)\b.*\b(leaves?)\b",
            "spots": r"\b(spots?|lesions?|patches?)\b(?!\s+of)",  # Avoid "no spots"
            "holes": r"\b(holes?|eaten|chewed|damaged)\b.*\b(leaves?)\b",
            "fuzzy_growth": r"\b(fuzzy|moldy|mold|cottony|white growth)\b",
            "rust_colored": r"\b(rust|rusty|orange|reddish-orange)\b.*\b(spots?|powder)\b",
            "powdery": r"\b(powdery|dusty|white powder)\b",
            "discoloration": r"\b(discolor|discoloration|unusual color|color change)\b",
            
            # Severity indicators
            "spreading": r"\b(spreading|advancing|getting worse|progressing)\b",
            "severe": r"\b(severe|extensive|widespread|covering)\b",
            "mild": r"\b(mild|slight|beginning|early)\b"
        }
        
        # Severity assessment keywords
        self.severity_keywords = {
            "critical": ["dying", "dead", "severe", "extensive", "widespread", "covering most"],
            "high": ["spreading rapidly", "many leaves", "progressing", "getting worse", "significant"],
            "moderate": ["several leaves", "noticeable", "some spread", "moderate"],
            "mild": ["few leaves", "early stage", "beginning", "slight", "minor"]
        }
    
    def process_analysis(self, raw_analysis: str, analysis_type: str, plant_context: str) -> Dict[str, Any]:
        """
        Process the raw SmolVLM analysis into structured plant health report
        """
        logger.info(f"Processing {analysis_type} analysis")
        logger.info(f"Raw analysis: {raw_analysis}")
        
        # Clean and normalize the analysis text
        cleaned_analysis = self._clean_analysis_text(raw_analysis)
        
        # Extract symptoms from the analysis
        detected_symptoms = self._extract_symptoms(cleaned_analysis)
        
        # Assess severity
        severity_level = self._assess_severity(cleaned_analysis, detected_symptoms)
        
        # Match to known conditions
        possible_conditions = self._match_conditions(detected_symptoms, plant_context, cleaned_analysis)
        
        # Generate treatment recommendations
        treatments = self._generate_treatments(possible_conditions, severity_level)
        
        # Create actionable advice
        immediate_actions = self._generate_immediate_actions(detected_symptoms, severity_level)
        prevention_tips = self._generate_prevention_tips(possible_conditions)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(detected_symptoms, possible_conditions)
        
        return {
            "raw_analysis": raw_analysis,
            "detected_symptoms": detected_symptoms,
            "severity_level": severity_level,
            "possible_conditions": possible_conditions[:3],  # Top 3 matches
            "treatments": treatments,
            "immediate_actions": immediate_actions,
            "prevention_tips": prevention_tips,
            "confidence_score": confidence,
            "analysis_type": analysis_type,
            "recommendations": self._format_recommendations(
                possible_conditions, treatments, immediate_actions, severity_level
            )
        }
    
    def _clean_analysis_text(self, analysis: str) -> str:
        """Clean and normalize the analysis text"""
        # Remove common prefixes and suffixes
        analysis = re.sub(r'^.*?Answer:\s*', '', analysis, flags=re.IGNORECASE)
        analysis = re.sub(r'^.*?assistant[:\s]*', '', analysis, flags=re.IGNORECASE)
        analysis = re.sub(r'^.*?user.*?IMPORTANT:.*?$', '', analysis, flags=re.MULTILINE | re.DOTALL)
        
        # Clean up whitespace
        analysis = ' '.join(analysis.split())
        
        return analysis.strip()
    
    def _extract_symptoms(self, analysis: str) -> List[Dict[str, Any]]:
        """Extract symptoms from the analysis text using enhanced pattern matching"""
        symptoms = []
        analysis_lower = analysis.lower()
        
        logger.info(f"Analyzing text: '{analysis_lower}'")
        
        # First, check for explicit healthy indicators  
        healthy_indicators = [
            r"\bhealthy\s+plant\b",
            r"\bappears\s+healthy\b",
            r"\blooks\s+healthy\b", 
            r"\bno\s+signs?\s+of\s+(disease|problems|issues)\b",
            r"\bno\s+visible\s+(problems|disease|damage)\b",
            r"\bplant\s+is\s+healthy\b"
        ]
        
        # Check for negative contexts (explicitly saying NO problems)
        negative_contexts = [
            r"no\s+signs?\s+of.*\b(disease|infection|fungal|bacterial|viral)\b",
            r"no\s+visible.*\b(damage|problems|disease|symptoms)\b",
            r"appears.*healthy",
            r"looks.*healthy",
            r"healthy.*plant"
        ]
        
        has_explicit_healthy = any(re.search(pattern, analysis_lower) for pattern in healthy_indicators)
        has_negative_context = any(re.search(pattern, analysis_lower) for pattern in negative_contexts)
        
        # If there are explicit healthy statements, check if they outweigh problems
        if has_explicit_healthy and not self._has_definitive_problems(analysis_lower):
            logger.info("Plant identified as explicitly healthy")
            return [{
                "name": "healthy_plant",
                "text_match": "plant appears healthy",
                "confidence": 0.9
            }]
        
        # Look for definitive disease/problem statements
        definitive_problems = [
            r"\bfungal\s+infection\b",
            r"\bbacterial\s+infection\b", 
            r"\bviral\s+infection\b",
            r"\bdisease\b",
            r"\binfection\b"
        ]
        
        has_definitive_problems = any(re.search(pattern, analysis_lower) for pattern in definitive_problems)
        
        if has_definitive_problems:
            logger.info("Definitive problems detected, analyzing symptoms...")
        elif has_negative_context and not has_definitive_problems:
            logger.info("Negative context detected, treating as healthy")
            return [{
                "name": "healthy_plant", 
                "text_match": "no signs of disease mentioned",
                "confidence": 0.8
            }]
        
        # Extract specific symptoms using enhanced patterns
        for symptom_name, pattern in self.symptom_patterns.items():
            matches = list(re.finditer(pattern, analysis_lower, re.IGNORECASE))
            for match in matches:
                match_text = match.group()
                
                # Skip if this appears to be in a negative context
                surrounding_text = analysis_lower[max(0, match.start()-20):match.end()+20]
                if self._is_negative_context(surrounding_text, match_text):
                    continue
                
                confidence = self._calculate_symptom_confidence(match_text, symptom_name, analysis_lower)
                
                symptoms.append({
                    "name": symptom_name,
                    "text_match": match_text,
                    "confidence": confidence
                })
                
                logger.info(f"Found symptom: {symptom_name} - '{match_text}' (confidence: {confidence})")
        
        # Remove duplicates and sort by confidence
        unique_symptoms = []
        seen_symptoms = set()
        for symptom in symptoms:
            if symptom["name"] not in seen_symptoms:
                unique_symptoms.append(symptom)
                seen_symptoms.add(symptom["name"])
        
        # If no symptoms found but we have analysis text, check for implicit problems
        if not unique_symptoms and len(analysis.strip()) > 10:
            if self._has_implicit_problems(analysis_lower):
                unique_symptoms.append({
                    "name": "general_stress",
                    "text_match": "unspecified plant stress detected",
                    "confidence": 0.5
                })
        
        return sorted(unique_symptoms, key=lambda x: x["confidence"], reverse=True)
    
    def _has_definitive_problems(self, analysis_lower: str) -> bool:
        """Check if the analysis contains definitive problem statements"""
        definitive_problems = [
            r"\bfungal\s+infection\b",
            r"\bbacterial\s+infection\b",
            r"\bviral\s+infection\b", 
            r"\bdisease\b(?!\s+resistant)",
            r"\binfection\b",
            r"\bblight\b",
            r"\brust\b(?!\s+resistant)",
            r"\bmildew\b",
            r"\brot\b(?:ting)?\b"
        ]
        return any(re.search(pattern, analysis_lower) for pattern in definitive_problems)
    
    def _has_implicit_problems(self, analysis_lower: str) -> bool:
        """Check for implicit problem indicators"""
        implicit_problems = [
            r"\bbrown\b.*\b(edge|tip|spot)\b",
            r"\byellow\b.*\b(leaf|leave)\b", 
            r"\bwilt\b",
            r"\bdamage\b",
            r"\bstress\b"
        ]
        return any(re.search(pattern, analysis_lower) for pattern in implicit_problems)
    
    def _is_negative_context(self, surrounding_text: str, match_text: str) -> bool:
        """Check if a symptom match is in a negative context"""
        negative_indicators = ['no', 'without', 'absence of', 'not', 'free from', 'clear of']
        
        # Look for negative words before the match
        words_before = surrounding_text[:surrounding_text.find(match_text)].split()
        recent_words = words_before[-3:] if len(words_before) >= 3 else words_before
        
        return any(neg_word in recent_words for neg_word in negative_indicators)
    
    def _assess_severity(self, analysis: str, symptoms: List[Dict]) -> str:
        """Assess the severity level of the plant condition"""
        analysis_lower = analysis.lower()
        
        # Check if plant is explicitly healthy
        if any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
            return "none"
        
        # Check for explicit severity keywords
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if keyword in analysis_lower:
                    logger.info(f"Found severity keyword '{keyword}' -> {severity}")
                    return severity
        
        # Assess based on symptoms
        if not symptoms or len(symptoms) == 0:
            return "none"
        
        # Disease-based severity assessment
        disease_symptoms = ["fungal_infection", "bacterial_infection", "viral_infection", "blight", "rust_disease"]
        stress_symptoms = ["browning", "burning", "yellowing", "wilting"]
        mild_symptoms = ["spots", "discoloration"]
        
        disease_count = sum(1 for s in symptoms if s["name"] in disease_symptoms)
        stress_count = sum(1 for s in symptoms if s["name"] in stress_symptoms)
        
        # Severity logic
        if disease_count >= 1:
            # If we have definitive disease, assess based on additional symptoms
            if stress_count >= 2:
                return "high"
            elif stress_count >= 1:
                return "moderate"
            else:
                return "mild"
        elif stress_count >= 2:
            return "moderate"
        elif stress_count >= 1 or len(symptoms) >= 1:
            return "mild"
        else:
            return "none"
    
    def _match_conditions(self, symptoms: List[Dict], plant_context: str, analysis_text: str) -> List[Dict[str, Any]]:
        """Match detected symptoms to known plant conditions"""
        
        # Handle healthy plants first
        if any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
            return [{
                "name": "healthy_plant",
                "score": 10.0,
                "matched_symptoms": ["healthy_plant"],
                "info": {
                    "description": "Plant appears healthy with no visible signs of disease or stress",
                    "treatments": [],
                    "prevention": [
                        "Continue current care routine",
                        "Monitor regularly for any changes", 
                        "Maintain proper watering and nutrition"
                    ]
                },
                "confidence": 0.9
            }]
        
        # If no symptoms detected, also treat as healthy
        if not symptoms or len(symptoms) == 0:
            return [{
                "name": "healthy_plant",
                "score": 8.0,
                "matched_symptoms": [],
                "info": {
                    "description": "No concerning symptoms detected",
                    "treatments": [],
                    "prevention": ["Continue regular plant care"]
                },
                "confidence": 0.7
            }]
        
        # Match to specific conditions based on symptoms and analysis text
        conditions = []
        analysis_lower = analysis_text.lower()
        
        # Direct disease identification
        if "fungal infection" in analysis_lower or any(s["name"] == "fungal_infection" for s in symptoms):
            conditions.append({
                "name": "fungal_leaf_spot",
                "score": 9.0,
                "matched_symptoms": ["fungal_infection"],
                "info": {
                    "description": "Fungal infection affecting plant tissue, commonly causing leaf spots and tissue damage",
                    "treatments": [
                        {"type": "fungicide", "action": "Apply copper-based fungicide", "details": ["Spray affected areas", "Repeat every 7-14 days"]},
                        {"type": "cultural", "action": "Improve air circulation", "details": ["Space plants properly", "Prune dense growth"]}
                    ],
                    "prevention": ["Avoid overhead watering", "Ensure good drainage", "Remove infected debris"]
                },
                "confidence": 0.9
            })
        
        if "bacterial infection" in analysis_lower or any(s["name"] == "bacterial_infection" for s in symptoms):
            conditions.append({
                "name": "bacterial_leaf_spot",
                "score": 9.0,
                "matched_symptoms": ["bacterial_infection"],
                "info": {
                    "description": "Bacterial infection causing leaf spotting and potential systemic damage",
                    "treatments": [
                        {"type": "bactericide", "action": "Apply copper bactericide", "details": ["Early morning application preferred"]},
                        {"type": "cultural", "action": "Remove infected material", "details": ["Prune affected areas", "Disinfect tools"]}
                    ],
                    "prevention": ["Avoid overhead watering", "Improve sanitation", "Use pathogen-free seeds"]
                },
                "confidence": 0.9
            })
        
        # Symptom-based matching for other conditions
        symptom_names = [s["name"] for s in symptoms]
        
        if "browning" in symptom_names or "burning" in symptom_names:
            conditions.append({
                "name": "leaf_scorch",
                "score": 7.0,
                "matched_symptoms": ["browning", "burning"],
                "info": {
                    "description": "Leaf burn or scorch, often from environmental stress or nutrient issues",
                    "treatments": [
                        {"type": "environmental", "action": "Adjust watering schedule", "details": ["Check soil moisture", "Avoid overwatering"]},
                        {"type": "cultural", "action": "Provide shade if needed", "details": ["Protect from intense sun"]}
                    ],
                    "prevention": ["Monitor environmental conditions", "Gradual acclimatization to sun"]
                },
                "confidence": 0.7
            })
        
        if "yellowing" in symptom_names:
            conditions.append({
                "name": "nutrient_deficiency",
                "score": 6.0,
                "matched_symptoms": ["yellowing"],
                "info": {
                    "description": "Possible nutrient deficiency, commonly nitrogen deficiency",
                    "treatments": [
                        {"type": "fertilizer", "action": "Apply balanced fertilizer", "details": ["Use N-P-K fertilizer", "Follow package directions"]}
                    ],
                    "prevention": ["Regular fertilization schedule", "Soil testing"]
                },
                "confidence": 0.6
            })
        
        # Sort by score and return
        return sorted(conditions, key=lambda x: x["score"], reverse=True)
    
    def _generate_treatments(self, conditions: List[Dict], severity: str) -> List[Dict[str, Any]]:
        """Generate treatment recommendations based on conditions and severity"""
        treatments = []
        
        if not conditions:
            # Generic treatments for unknown conditions
            treatments.append({
                "type": "general_care",
                "action": "Improve general plant care",
                "details": ["Ensure proper watering", "Check soil drainage", "Provide adequate light"],
                "urgency": "medium"
            })
        else:
            # Specific treatments for identified conditions
            for condition in conditions[:2]:  # Top 2 conditions
                condition_info = condition["info"]
                
                for treatment in condition_info.get("treatments", []):
                    urgency = "high" if severity in ["critical", "high"] else "medium"
                    
                    treatments.append({
                        "type": treatment.get("type", "general"),
                        "action": treatment.get("action", ""),
                        "details": treatment.get("details", []),
                        "urgency": urgency,
                        "condition": condition["name"]
                    })
        
        return treatments
    
    def _generate_immediate_actions(self, symptoms: List[Dict], severity: str) -> List[str]:
        """Generate immediate action items based on symptoms and severity"""
        actions = []
        
        # Handle healthy plants
        if severity == "none" or any(symptom.get("name") == "healthy_plant" for symptom in symptoms):
            return [
                "✅ Great news! Your plant appears healthy",
                "🔍 Continue regular monitoring for any changes",
                "💧 Maintain current watering and care routine",
                "🌱 Keep up the good work with plant care!"
            ]
        
        # Severity-based actions for actual problems
        if severity in ["critical", "high"]:
            actions.append("🚨 URGENT: This plant needs immediate attention!")
            actions.append("🔍 Consider consulting a local plant expert or extension office")
        
        # Symptom-specific actions
        symptom_names = [s["name"] for s in symptoms]
        
        if any(s in symptom_names for s in ["fungal_infection", "bacterial_infection"]):
            actions.append("✂️ Remove all affected leaves immediately to prevent spread")
            actions.append("🧹 Clean up fallen debris around the plant")
            actions.append("💊 Apply appropriate treatment (fungicide/bactericide)")
        
        if "wilting" in symptom_names:
            actions.append("💧 Check soil moisture immediately - adjust watering as needed")
        
        if any(s in symptom_names for s in ["browning", "burning"]):
            actions.append("🌤️ Check environmental conditions - may need shade or wind protection")
        
        if "yellowing" in symptom_names:
            actions.append("🌱 Check fertilization schedule and soil nutrition")
        
        # General actions for problems
        if actions:  # Only add if there are actual problems
            actions.append("📋 Take photos to monitor progress over next few days")
        
        return actions
    
    def _generate_prevention_tips(self, conditions: List[Dict]) -> List[str]:
        """Generate prevention tips based on identified conditions"""
        tips = set()  # Use set to avoid duplicates
        
        if conditions:
            for condition in conditions[:2]:
                condition_tips = condition["info"].get("prevention", [])
                tips.update(condition_tips)
        
        # Add general prevention tips
        general_tips = [
            "🔍 Inspect plants regularly for early problem detection",
            "💧 Water at soil level to avoid wetting leaves",
            "🌬️ Ensure good air circulation around plants",
            "🧹 Keep area clean of fallen leaves and debris",
            "🌱 Use disease-resistant plant varieties when possible"
        ]
        
        tips.update(general_tips[:3])  # Add a few general tips
        
        return list(tips)
    
    def _calculate_symptom_confidence(self, text_match: str, symptom_name: str, full_analysis: str) -> float:
        """Calculate confidence score for a symptom match"""
        base_confidence = 0.7
        
        # Higher confidence for disease mentions
        if symptom_name in ["fungal_infection", "bacterial_infection", "viral_infection"]:
            base_confidence = 0.9
        
        # Higher confidence for specific descriptive terms
        specific_terms = ["infection", "disease", "spots", "browning", "yellowing"]
        if any(term in text_match for term in specific_terms):
            base_confidence += 0.1
        
        # Reduce confidence for very short matches
        if len(text_match) < 5:
            base_confidence -= 0.2
        
        return min(max(base_confidence, 0.1), 1.0)
    
    def _calculate_confidence(self, symptoms: List[Dict], conditions: List[Dict]) -> str:
        """Calculate overall confidence in the diagnosis"""
        if not symptoms:
            return "low"
        
        # High confidence for definitive disease identification
        disease_symptoms = ["fungal_infection", "bacterial_infection", "viral_infection"]
        has_disease = any(s["name"] in disease_symptoms for s in symptoms)
        
        if has_disease:
            return "high"
        
        avg_symptom_confidence = sum(s["confidence"] for s in symptoms) / len(symptoms)
        
        if conditions and conditions[0]["score"] > 2.0 and avg_symptom_confidence > 0.8:
            return "high"
        elif conditions and conditions[0]["score"] > 1.0 and avg_symptom_confidence > 0.6:
            return "medium"
        else:
            return "low"
    
    def _format_recommendations(self, conditions: List[Dict], treatments: List[Dict], 
                              actions: List[str], severity: str) -> str:
        """Format final recommendations into readable text"""
        recommendations = []
        
        # Diagnosis summary
        if conditions:
            top_condition = conditions[0]
            recommendations.append(f"**Most Likely Issue**: {top_condition['name'].replace('_', ' ').title()}")
            recommendations.append(f"**Confidence**: {top_condition['confidence']:.0%}")
        
        # Severity
        recommendations.append(f"**Severity**: {severity.title()}")
        
        # Key treatments
        if treatments:
            recommendations.append("**Key Treatments**:")
            for treatment in treatments[:2]:
                recommendations.append(f"• {treatment['action']}")
        
        # Most important actions
        if actions:
            recommendations.append("**Immediate Actions**:")
            for action in actions[:3]:
                recommendations.append(f"• {action}")
        
        return "\n".join(recommendations)