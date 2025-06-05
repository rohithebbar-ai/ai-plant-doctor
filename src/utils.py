# utils.py - Helper Functions for AI Plant Doctor

import re
from typing import Dict, Any, List
from PIL import Image
import io
import base64

def ensure_confidence_string(confidence) -> str:
    """
    Ensure confidence is always returned as a string
    """
    if isinstance(confidence, float):
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        else:
            return "low"
    elif isinstance(confidence, str):
        return confidence.lower()
    else:
        return "low"

def format_diagnosis_report(results: Dict[str, Any]) -> str:
    """
    Format the diagnosis results into a nice HTML report
    """
    if not results or "error" in results:
        return "<div class='emergency-alert'>❌ Unable to generate diagnosis report</div>"
    
    # Extract key information
    severity = results.get("severity_level", "unknown")
    confidence = ensure_confidence_string(results.get("confidence_score", "low"))
    conditions = results.get("possible_conditions", [])
    symptoms = results.get("detected_symptoms", [])
    treatments = results.get("treatments", [])
    immediate_actions = results.get("immediate_actions", [])
    
    # Start building the HTML report
    html_parts = []
    
    # Severity indicator
    severity_class = f"severity-{severity}"
    severity_emoji = {
        "critical": "🚨",
        "high": "⚠️", 
        "moderate": "⚖️",
        "mild": "✅",
        "none": "🌱"  # New emoji for healthy plants
    }.get(severity, "📊")
    
    # Special handling for healthy plants
    if severity == "none":
        severity_display = "Healthy"
        severity_class = "severity-healthy"
    else:
        severity_display = severity.title()
    
    html_parts.append(f"""
    <div class="diagnosis-card {severity_class}">
        <h3>{severity_emoji} Plant Health Assessment</h3>
        <p><strong>Severity Level:</strong> {severity_display}</p>
        <p><strong>Confidence:</strong> {confidence.title()}</p>
    </div>
    """)
    
    # Most likely conditions
    if conditions:
        # Check if this is a healthy plant
        is_healthy = (severity == "none" or 
                     any(condition.get("name") == "healthy_plant" for condition in conditions))
        
        if is_healthy:
            html_parts.append("<div class='diagnosis-card'>")
            html_parts.append("<h3>🌱 Plant Health Status</h3>")
        else:
            html_parts.append("<div class='diagnosis-card'>")
            html_parts.append("<h3>🔍 Most Likely Issues</h3>")
        
        for i, condition in enumerate(conditions[:3], 1):
            condition_name = condition.get("name", "Unknown").replace("_", " ").title()
            condition_confidence = condition.get("confidence", 0)
            condition_info = condition.get("info", {})
            
            # Special handling for healthy plants
            if condition_name == "Healthy Plant":
                html_parts.append(f"""
                <div class="treatment-card" style="background: #e8f5e8; border-left: 4px solid #4CAF50;">
                    <h4>🌱 {condition_name}</h4>
                    <p><strong>Assessment Confidence:</strong> {condition_confidence:.0%}</p>
                    <p><strong>Status:</strong> {condition_info.get('description', 'Plant is in good health')}</p>
                </div>
                """)
            else:
                html_parts.append(f"""
                <div class="treatment-card">
                    <h4>{i}. {condition_name}</h4>
                    <p><strong>Match Confidence:</strong> {condition_confidence:.0%}</p>
                    <p><strong>Description:</strong> {condition_info.get('description', 'No description available')}</p>
                </div>
                """)
        
        html_parts.append("</div>")
    
    # Detected symptoms
    if symptoms:
        # Check if this is a healthy plant
        is_healthy = (severity == "none" or 
                     any(symptom.get("name") == "healthy_plant" for symptom in symptoms))
        
        if is_healthy:
            html_parts.append("<div class='diagnosis-card'>")
            html_parts.append("<h3>🌱 Health Indicators</h3>")
            html_parts.append("<ul>")
            html_parts.append("<li><strong>✅ Healthy Appearance</strong> (confidence: 90%)</li>")
            html_parts.append("<li><strong>🍃 Good Leaf Condition</strong></li>") 
            html_parts.append("<li><strong>🌿 No Visible Problems</strong></li>")
            html_parts.append("</ul>")
            html_parts.append("</div>")
        else:
            html_parts.append("<div class='diagnosis-card'>")
            html_parts.append("<h3>🍃 Detected Symptoms</h3>")
            html_parts.append("<ul>")
            
            for symptom in symptoms[:5]:  # Show top 5 symptoms
                symptom_name = symptom.get("name", "").replace("_", " ").title()
                symptom_confidence = symptom.get("confidence", 0)
                html_parts.append(f"<li><strong>{symptom_name}</strong> (confidence: {symptom_confidence:.0%})</li>")
            
            html_parts.append("</ul>")
            html_parts.append("</div>")
    
    # Immediate actions
    if immediate_actions:
        # Check if emergency actions are needed
        has_emergency = any("URGENT" in action for action in immediate_actions)
        
        if has_emergency:
            html_parts.append("<div class='emergency-alert'>")
            html_parts.append("<h3>🚨 URGENT ACTIONS NEEDED</h3>")
        else:
            html_parts.append("<div class='diagnosis-card'>")
            html_parts.append("<h3>⚡ Immediate Actions</h3>")
        
        html_parts.append("<ul>")
        for action in immediate_actions:
            html_parts.append(f"<li>{action}</li>")
        html_parts.append("</ul>")
        html_parts.append("</div>")
    
    # Treatment recommendations
    if treatments:
        html_parts.append("<div class='diagnosis-card'>")
        html_parts.append("<h3>💊 Treatment Options</h3>")
        
        for treatment in treatments[:3]:  # Show top 3 treatments
            treatment_type = treatment.get("type", "general").replace("_", " ").title()
            action = treatment.get("action", "No action specified")
            urgency = treatment.get("urgency", "medium")
            details = treatment.get("details", [])
            
            urgency_emoji = {
                "high": "🔴",
                "medium": "🟡", 
                "low": "🟢"
            }.get(urgency, "⭕")
            
            html_parts.append(f"""
            <div class="treatment-card">
                <h4>{urgency_emoji} {treatment_type}</h4>
                <p><strong>Action:</strong> {action}</p>
                <p><strong>Urgency:</strong> {urgency.title()}</p>
            """)
            
            if details:
                html_parts.append("<p><strong>Details:</strong></p><ul>")
                for detail in details:
                    html_parts.append(f"<li>{detail}</li>")
                html_parts.append("</ul>")
            
            html_parts.append("</div>")
        
        html_parts.append("</div>")
    
    # Confidence and next steps
    html_parts.append(f"""
    <div class="diagnosis-card">
        <h3>📈 Analysis Summary</h3>
        <p><strong>Overall Confidence:</strong> {confidence.title()}</p>
        <p><strong>Recommendation:</strong> 
        {get_confidence_recommendation(confidence, severity)}
        </p>
    </div>
    """)
    
    return "".join(html_parts)

def get_confidence_recommendation(confidence: str, severity: str) -> str:
    """
    Get recommendation based on confidence and severity levels
    """
    # Handle healthy plants first
    if severity == "none" or severity == "healthy":
        if confidence == "high":
            return "High confidence that your plant is healthy! Continue your excellent care routine."
        elif confidence == "medium":
            return "Plant appears healthy. Keep monitoring and maintain current care practices."
        else:
            return "Plant seems okay, but consider getting a second opinion if you notice any changes."
    
    # Handle problem plants
    if confidence == "high" and severity in ["mild", "moderate"]:
        return "Diagnosis appears reliable. Follow treatment recommendations and monitor progress."
    elif confidence == "high" and severity in ["high", "critical"]:
        return "High confidence diagnosis of serious issue. Take immediate action and consider professional consultation."
    elif confidence == "medium":
        return "Moderate confidence in diagnosis. Try recommended treatments and monitor closely. Consider getting a second opinion."
    else:
        return "Low confidence diagnosis. Consider consulting a local plant expert or extension service for professional advice."

def format_symptoms_list(symptoms: List[Dict]) -> str:
    """
    Format symptoms into a readable list
    """
    if not symptoms:
        return "No specific symptoms detected."
    
    formatted = []
    for symptom in symptoms:
        name = symptom.get("name", "").replace("_", " ").title()
        confidence = symptom.get("confidence", 0)
        formatted.append(f"• {name} ({confidence:.0%} confidence)")
    
    return "\n".join(formatted)

def format_treatments_text(treatments: List[Dict]) -> str:
    """
    Format treatments into readable text
    """
    if not treatments:
        return "No specific treatments recommended."
    
    formatted = []
    for i, treatment in enumerate(treatments, 1):
        action = treatment.get("action", "No action specified")
        urgency = treatment.get("urgency", "medium")
        details = treatment.get("details", [])
        
        formatted.append(f"{i}. **{action}** ({urgency} priority)")
        
        if details:
            for detail in details:
                formatted.append(f"   - {detail}")
        
        formatted.append("")  # Add blank line between treatments
    
    return "\n".join(formatted)

def resize_image_for_analysis(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """
    Resize image for optimal analysis while maintaining aspect ratio
    """
    if max(image.size) <= max_size:
        return image
    
    # Calculate new size maintaining aspect ratio
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int((height * max_size) / width)
    else:
        new_height = max_size
        new_width = int((width * max_size) / height)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def validate_image(image: Image.Image) -> tuple[bool, str]:
    """
    Validate if the image is suitable for plant analysis
    """
    if image is None:
        return False, "No image provided"
    
    try:
        # Check if image can be processed
        width, height = image.size
        
        # Check minimum size
        if width < 100 or height < 100:
            return False, "Image is too small. Please upload a larger image (at least 100x100 pixels)."
        
        # Check if image is too large (memory concerns)
        if width * height > 10000000:  # 10MP limit
            return False, "Image is too large. Please upload a smaller image."
        
        # Check image mode
        if image.mode not in ['RGB', 'RGBA', 'L']:
            return False, "Unsupported image format. Please use RGB, RGBA, or grayscale images."
        
        return True, "Image is valid"
        
    except Exception as e:
        return False, f"Error validating image: {str(e)}"

def extract_plant_keywords(text: str) -> List[str]:
    """
    Extract plant-related keywords from user input
    """
    plant_keywords = [
        # Common plants
        'tomato', 'pepper', 'cucumber', 'lettuce', 'spinach', 'carrot', 'potato',
        'rose', 'tulip', 'sunflower', 'marigold', 'petunia', 'geranium',
        'oak', 'maple', 'pine', 'birch', 'cherry', 'apple', 'orange',
        'basil', 'oregano', 'thyme', 'parsley', 'mint', 'rosemary',
        
        # Plant parts
        'leaf', 'leaves', 'stem', 'branch', 'flower', 'bud', 'fruit', 'root',
        
        # Growing conditions
        'indoor', 'outdoor', 'garden', 'greenhouse', 'pot', 'container',
        'shade', 'sun', 'partial', 'full', 'morning', 'afternoon',
        'humid', 'dry', 'wet', 'moist', 'drought', 'rain',
        
        # Care activities
        'watering', 'fertilizer', 'pruning', 'repotting', 'transplant',
        'mulch', 'compost', 'pesticide', 'fungicide'
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for keyword in plant_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def create_severity_badge(severity: str) -> str:
    """
    Create a colored badge for severity level
    """
    badges = {
        "critical": "🔴 CRITICAL",
        "high": "🟠 HIGH", 
        "moderate": "🟡 MODERATE",
        "mild": "🟢 MILD",
        "none": "🌱 HEALTHY",
        "unknown": "⚪ UNKNOWN"
    }
    return badges.get(severity, "⚪ UNKNOWN")

def format_confidence_indicator(confidence: str) -> str:
    """
    Format confidence level with appropriate emoji
    """
    indicators = {
        "high": "🎯 High Confidence",
        "medium": "🎲 Medium Confidence", 
        "low": "❓ Low Confidence"
    }
    return indicators.get(confidence, "❓ Unknown Confidence")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "plant_image"
    
    return filename

def create_diagnosis_summary(results: Dict[str, Any]) -> str:
    """
    Create a concise one-line summary of the diagnosis
    """
    if not results or "error" in results:
        return "❌ Diagnosis failed"
    
    severity = results.get("severity_level", "unknown")
    conditions = results.get("possible_conditions", [])
    confidence = ensure_confidence_string(results.get("confidence_score", "low"))
    
    # Handle healthy plants
    if severity == "none" or any(c.get("name") == "healthy_plant" for c in conditions):
        return f"🌱 HEALTHY - Plant appears to be in excellent condition ({confidence} confidence)"
    
    # Handle problem plants
    if conditions:
        top_condition = conditions[0].get("name", "unknown issue").replace("_", " ").title()
        return f"{create_severity_badge(severity)} - Likely {top_condition} ({confidence} confidence)"
    else:
        return f"{create_severity_badge(severity)} - General plant stress detected ({confidence} confidence)"

def format_prevention_tips(tips: List[str]) -> str:
    """
    Format prevention tips into readable markdown
    """
    if not tips:
        return "No specific prevention tips available."
    
    formatted_tips = []
    for tip in tips:
        # Add emoji if not already present
        if not any(emoji in tip for emoji in ['🔍', '💧', '🌬️', '🧹', '🌱', '📅', '🌡️', '🧪']):
            tip = f"• {tip}"
        formatted_tips.append(tip)
    
    return "\n".join(formatted_tips)

def estimate_recovery_time(severity: str, condition_type: str) -> str:
    """
    Estimate recovery time based on severity and condition type
    """
    base_times = {
        "fungal": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "high": "4-8 weeks", "critical": "8+ weeks"},
        "bacterial": {"mild": "2-3 weeks", "moderate": "3-6 weeks", "high": "6-12 weeks", "critical": "12+ weeks"},
        "nutrient": {"mild": "1-2 weeks", "moderate": "2-3 weeks", "high": "3-4 weeks", "critical": "4+ weeks"},
        "environmental": {"mild": "few days", "moderate": "1-2 weeks", "high": "2-4 weeks", "critical": "4+ weeks"},
        "pest": {"mild": "1 week", "moderate": "2-3 weeks", "high": "3-6 weeks", "critical": "6+ weeks"}
    }
    
    # Extract condition category
    category = "environmental"  # default
    if "fungal" in condition_type.lower():
        category = "fungal"
    elif "bacterial" in condition_type.lower():
        category = "bacterial"
    elif "nutrient" in condition_type.lower() or "deficiency" in condition_type.lower():
        category = "nutrient"
    elif "pest" in condition_type.lower() or "insect" in condition_type.lower():
        category = "pest"
    
    return base_times.get(category, {}).get(severity, "timeframe varies")

def create_treatment_timeline(treatments: List[Dict]) -> str:
    """
    Create a timeline for treatment applications
    """
    if not treatments:
        return "No treatment timeline available."
    
    timeline = []
    timeline.append("📅 **Treatment Timeline:**\n")
    
    immediate_treatments = [t for t in treatments if t.get("urgency") == "high"]
    regular_treatments = [t for t in treatments if t.get("urgency") != "high"]
    
    if immediate_treatments:
        timeline.append("**Immediate (within 24 hours):**")
        for treatment in immediate_treatments:
            timeline.append(f"• {treatment.get('action', 'Action not specified')}")
        timeline.append("")
    
    if regular_treatments:
        timeline.append("**Ongoing treatment:**")
        for treatment in regular_treatments:
            timeline.append(f"• {treatment.get('action', 'Action not specified')}")
    
    timeline.append("\n📋 **Follow-up:** Monitor progress and repeat treatments as recommended")
    
    return "\n".join(timeline)

def generate_care_checklist(results: Dict[str, Any]) -> str:
    """
    Generate a daily care checklist based on diagnosis
    """
    checklist_items = [
        "□ Check soil moisture level",
        "□ Inspect leaves for changes", 
        "□ Remove any new affected plant material",
        "□ Monitor environmental conditions"
    ]
    
    # Add specific items based on diagnosis
    symptoms = results.get("detected_symptoms", [])
    severity = results.get("severity_level", "mild")
    
    symptom_names = [s.get("name", "") for s in symptoms]
    
    if "wilting" in symptom_names:
        checklist_items.append("□ Adjust watering schedule")
    
    if any(s in symptom_names for s in ["spots", "browning", "blackening"]):
        checklist_items.append("□ Apply fungicide treatment")
        checklist_items.append("□ Clean up fallen debris")
    
    if "yellowing" in symptom_names:
        checklist_items.append("□ Check fertilizer needs")
    
    if severity in ["high", "critical"]:
        checklist_items.append("□ Take photos to track progress")
        checklist_items.append("□ Consider professional consultation")
    
    return "**Daily Care Checklist:**\n" + "\n".join(checklist_items)

def get_plant_care_schedule(plant_type: str, season: str) -> str:
    """
    Generate a care schedule based on plant type and season
    """
    schedules = {
        "tomato": {
            "spring": ["Start seeds indoors", "Prepare soil", "Plan garden layout"],
            "summer": ["Water consistently", "Stake plants", "Monitor for pests", "Harvest regularly"],
            "fall": ["Collect seeds", "Remove plants", "Prepare soil for winter"],
            "winter": ["Plan next year", "Order seeds", "Maintain tools"]
        },
        "rose": {
            "spring": ["Prune dead canes", "Apply fertilizer", "Mulch around base"],
            "summer": ["Water regularly", "Deadhead flowers", "Monitor for diseases"],
            "fall": ["Reduce watering", "Clean up leaves", "Apply winter protection"],
            "winter": ["Dormant season care", "Plan pruning", "Order new varieties"]
        },
        "general": {
            "spring": ["Clean up winter damage", "Apply fertilizer", "Start pest monitoring"],
            "summer": ["Maintain watering", "Monitor plant health", "Harvest/deadhead"],
            "fall": ["Prepare for winter", "Clean up debris", "Plant cover crops"],
            "winter": ["Protect tender plants", "Plan next year", "Maintain tools"]
        }
    }
    
    schedule = schedules.get(plant_type.lower(), schedules["general"])
    tasks = schedule.get(season.lower(), ["No specific tasks for this season"])
    
    return f"**{season.title()} Care for {plant_type.title()}:**\n" + "\n".join([f"• {task}" for task in tasks])

def format_scientific_info(condition_name: str) -> str:
    """
    Format scientific information about a plant condition
    """
    scientific_info = {
        "fungal_leaf_spot": {
            "pathogen": "Various fungi (Septoria, Alternaria, Cercospora species)",
            "lifecycle": "Spores spread by water, wind, and infected plant material",
            "conditions": "Thrives in warm, humid conditions with poor air circulation"
        },
        "rust_disease": {
            "pathogen": "Various rust fungi (Puccinia, Uromyces species)",
            "lifecycle": "Complex lifecycle often involving alternate hosts",
            "conditions": "Cool, moist conditions favor spore germination"
        },
        "powdery_mildew": {
            "pathogen": "Various fungi (Erysiphe, Podosphaera, Sphaerotheca species)",
            "lifecycle": "Spreads rapidly in warm, dry conditions with high humidity",
            "conditions": "Unlike other fungi, doesn't require free water on leaves"
        },
        "bacterial_spot": {
            "pathogen": "Various bacteria (Xanthomonas, Pseudomonas species)",
            "lifecycle": "Spreads through water splash and contaminated tools",
            "conditions": "Warm, wet conditions with poor air circulation"
        },
        "mosaic_virus": {
            "pathogen": "Various viruses (TMV, CMV, TSWV)",
            "lifecycle": "Transmitted by insects, contaminated tools, or infected seeds",
            "conditions": "No environmental requirements - spreads through vectors"
        }
    }
    
    info = scientific_info.get(condition_name)
    if not info:
        return "Scientific information not available for this condition."
    
    return f"""
**Scientific Information:**
• **Pathogen:** {info['pathogen']}
• **Lifecycle:** {info['lifecycle']}
• **Optimal Conditions:** {info['conditions']}
"""

def calculate_treatment_cost(treatments: List[Dict]) -> Dict[str, str]:
    """
    Estimate treatment costs (rough estimates)
    """
    cost_estimates = {
        "organic": {"low": "$5-15", "medium": "$15-30", "high": "$30-50"},
        "fungicide": {"low": "$10-25", "medium": "$25-50", "high": "$50-100"},
        "bactericide": {"low": "$15-30", "medium": "$30-60", "high": "$60-120"},
        "fertilizer": {"low": "$10-20", "medium": "$20-40", "high": "$40-80"},
        "cultural": {"low": "$0-10", "medium": "$10-25", "high": "$25-50"}
    }
    
    total_costs = {"low": 0, "medium": 0, "high": 0}
    
    for treatment in treatments:
        treatment_type = treatment.get("type", "cultural")
        costs = cost_estimates.get(treatment_type, cost_estimates["cultural"])
        
        # Add to total (simplified calculation)
        for level in ["low", "medium", "high"]:
            range_str = costs[level]
            # Extract middle value from range like "$10-25"
            numbers = re.findall(r'\d+', range_str)
            if len(numbers) >= 2:
                avg_cost = (int(numbers[0]) + int(numbers[1])) / 2
                total_costs[level] += avg_cost
    
    return {
        "budget": f"${total_costs['low']:.0f}-{total_costs['medium']:.0f}",
        "standard": f"${total_costs['medium']:.0f}-{total_costs['high']:.0f}",
        "premium": f"${total_costs['high']:.0f}+"
    }

def get_seasonal_advice(season: str) -> List[str]:
    """
    Get general seasonal plant care advice
    """
    seasonal_advice = {
        "spring": [
            "🌱 Start regular monitoring as plants become active",
            "💊 Apply preventive treatments before problems start", 
            "🧹 Clean up winter debris that can harbor diseases",
            "✂️ Prune damaged or dead growth from winter",
            "🌿 Begin fertilization program for growing season"
        ],
        "summer": [
            "💧 Monitor watering needs closely in hot weather",
            "🌡️ Watch for heat stress symptoms on plants",
            "🦠 Be vigilant for disease in humid conditions",
            "🐛 Check for increased pest activity",
            "🌳 Provide shade for sensitive plants during heat waves"
        ],
        "fall": [
            "🧹 Clean up fallen leaves to prevent disease carryover",
            "💧 Adjust watering as temperatures cool",
            "🌱 Prepare plants for winter dormancy",
            "✂️ Do final pruning before dormant season",
            "🏠 Begin protecting tender plants from cold"
        ],
        "winter": [
            "🏠 Protect tender plants from freezing temperatures",
            "💧 Reduce watering for dormant plants",
            "📚 Plan for next year's prevention strategies",
            "🔍 Monitor houseplants more closely",
            "🛠️ Clean and maintain garden tools"
        ]
    }
    
    return seasonal_advice.get(season.lower(), [])

def format_emergency_response(severity: str, condition_name: str) -> str:
    """
    Format emergency response instructions
    """
    if severity not in ["high", "critical"]:
        return "No emergency response needed for this severity level."
    
    emergency_responses = {
        "fire_blight": [
            "🚨 STOP all watering immediately",
            "✂️ Prune infected branches 12+ inches below symptoms", 
            "🧴 Disinfect tools with 70% alcohol between each cut",
            "🔥 Burn or bag all infected material - DO NOT COMPOST",
            "📱 Contact extension service for professional guidance"
        ],
        "crown_gall": [
            "🚨 Remove entire plant including all roots",
            "🚫 Do not replant susceptible species in same location for 3-4 years",
            "🧹 Sterilize soil if possible",
            "🧴 Disinfect all tools thoroughly"
        ],
        "viral_disease": [
            "🚨 Isolate plant immediately from other plants",
            "🦠 Control insect vectors (aphids, whiteflies) aggressively",
            "✂️ Remove infected plant entirely",
            "🧴 Disinfect tools with 10% bleach solution"
        ]
    }
    
    default_emergency = [
        "🚨 Take immediate action to prevent spread",
        "✂️ Remove all affected plant material",
        "🧹 Clean up area thoroughly",
        "📱 Consider professional consultation",
        "📸 Document progression with photos"
    ]
    
    response = emergency_responses.get(condition_name, default_emergency)
    
    return "**EMERGENCY RESPONSE PROTOCOL:**\n" + "\n".join([f"{i+1}. {action}" for i, action in enumerate(response)])

def validate_plant_image_content(description: str) -> tuple[bool, str, float]:
    """
    Validate if the image description indicates it's actually a plant
    """
    # Plant-related keywords that should be present
    plant_keywords = [
        'plant', 'leaf', 'leaves', 'stem', 'branch', 'flower', 'tree', 'bush', 
        'vegetation', 'foliage', 'garden', 'crop', 'herb', 'shrub', 'vine'
    ]
    
    # Non-plant keywords that indicate it's not a plant
    non_plant_keywords = [
        'person', 'people', 'face', 'car', 'building', 'phone', 'computer',
        'food', 'meal', 'pizza', 'bread', 'animal', 'dog', 'cat', 'bird'
    ]
    
    description_lower = description.lower()
    
    # Count plant vs non-plant keywords
    plant_score = sum(1 for keyword in plant_keywords if keyword in description_lower)
    non_plant_score = sum(1 for keyword in non_plant_keywords if keyword in description_lower)
    
    # Calculate confidence (0-1 scale)
    total_keywords = plant_score + non_plant_score
    if total_keywords == 0:
        confidence = 0.5  # Neutral if no keywords found
    else:
        confidence = plant_score / total_keywords
    
    # Determine if it's a plant image
    is_plant = plant_score > non_plant_score and confidence > 0.3
    
    if not is_plant:
        if non_plant_score > 0:
            message = f"This appears to be a {non_plant_keywords[0]} image rather than a plant. Please upload an image of a plant for analysis."
        else:
            message = "Unable to identify plant content in this image. Please upload a clear photo of a plant."
    else:
        message = "Plant content detected successfully."
    
    return is_plant, message, confidence