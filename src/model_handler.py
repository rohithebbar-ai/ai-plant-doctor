# model_handler.py - Fixed AI Plant Doctor with SmolVLM for Detailed Analysis

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import logging
import traceback
import re

from plant_health_analyzer import PlantHealthAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmolVLMPlantDoctor:
    def __init__(self, model_name="HuggingFaceTB/SmolVLM-Instruct"):
        """AI Plant Doctor using SmolVLM for plant health analysis"""
        self.device = self._get_device()
        self.model_name = model_name
        self.model = None
        self.processor = None
        self._load_model()
       
        # Initialize plant health analyzer
        self.plant_analyzer = PlantHealthAnalyzer()
        
        # Enhanced plant analysis prompts for different scenarios
        self.analysis_prompts = {
            "general_diagnosis": {
                "prompt": """You are a professional plant pathologist with 20 years of experience. Analyze this plant image and provide a comprehensive diagnostic report:

## VISUAL EXAMINATION:
Examine the plant systematically and describe in detail:
- **Leaf condition**: Color, texture, spots, patterns, edges, veins
- **Overall plant structure**: Growth pattern, branching, stem condition
- **Damage patterns**: Location, shape, size, distribution of any issues
- **Environmental indicators**: Signs of stress, nutrient status

## SYMPTOM ANALYSIS:
If you observe any problems, describe:
- **Primary symptoms**: What catches your attention first
- **Secondary symptoms**: Additional signs that support diagnosis
- **Pattern of spread**: How symptoms are distributed
- **Severity assessment**: Extent and progression of issues

## DIFFERENTIAL DIAGNOSIS:
Consider and discuss:
- **Most likely causes**: Based on visual evidence
- **Alternative possibilities**: Other conditions to consider
- **Ruling out factors**: Why certain diagnoses are less likely

## RECOMMENDATIONS:
Provide specific guidance on:
- **Immediate actions**: What should be done first
- **Treatment options**: Specific interventions
- **Monitoring**: What to watch for
- **Prevention**: How to avoid future issues

Be thorough and specific. If the plant appears healthy, explain why you reached that conclusion with supporting observations.""",
                "focus": "comprehensive health assessment"
            },
            
            "disease_focused": {
                "prompt": """You are a plant disease specialist. Conduct a detailed pathological examination of this plant:

## DISEASE INVESTIGATION:
Look systematically for signs of:

**FUNGAL PATHOGENS:**
- Examine for: spots, lesions, mold, rust, blight, mildew, rot
- Describe: size, shape, color, margins, spore presence
- Note: environmental conditions that favor fungal growth

**BACTERIAL INFECTIONS:**
- Look for: water-soaked lesions, soft rot, ooze, yellowing halos
- Assess: progression pattern, tissue breakdown, systemic spread

**VIRAL DISEASES:**
- Check for: mosaic patterns, mottling, distortion, stunting, ring spots
- Evaluate: symmetry of symptoms, plant vigor, growth abnormalities

## PATHOGEN IDENTIFICATION:
If disease is present:
- **Primary pathogen**: Most likely causal organism
- **Disease name**: Specific condition if identifiable
- **Pathogen lifecycle**: How it spreads and develops
- **Host susceptibility**: Why this plant is affected

## DIAGNOSTIC REASONING:
Explain your thought process:
- **Key diagnostic features**: What led to your conclusion
- **Distinguishing characteristics**: How you differentiated from other diseases
- **Confidence level**: How certain you are of the diagnosis

## MANAGEMENT STRATEGY:
Provide detailed recommendations:
- **Treatment timing**: When to act
- **Control methods**: Chemical, biological, cultural approaches
- **Resistance management**: Preventing further problems

If no disease is evident, explain what healthy characteristics you observe.""",
                "focus": "disease identification and pathology"
            },
            
            "nutrient_focused": {
                "prompt": """You are a plant nutrition specialist. Conduct a detailed nutritional assessment:

## NUTRITIONAL EVALUATION:
Systematically examine for deficiency symptoms:

**MACRONUTRIENT STATUS:**
- **Nitrogen**: Examine leaf color, growth vigor, older vs newer leaves
- **Phosphorus**: Check for purple/red discoloration, poor root development
- **Potassium**: Look for leaf edge burn, brown spots, weak stems

**MICRONUTRIENT ANALYSIS:**
- **Iron**: Assess interveinal chlorosis patterns
- **Magnesium**: Check for yellowing between veins
- **Calcium**: Look for tip burn, poor cell wall development

## SYMPTOM INTERPRETATION:
For each observed symptom:
- **Location on plant**: Which leaves/parts are affected
- **Progression pattern**: How symptoms develop over time
- **Severity assessment**: Mild, moderate, or severe deficiency
- **Mobile vs immobile nutrients**: Where symptoms appear first

## DIFFERENTIAL DIAGNOSIS:
Consider:
- **Primary deficiency**: Most likely nutrient shortage
- **Secondary factors**: pH, soil conditions, uptake issues
- **Toxicity symptoms**: Signs of nutrient excess
- **Interaction effects**: How nutrients affect each other

## CORRECTIVE MEASURES:
Provide specific recommendations:
- **Fertilizer selection**: What type and analysis needed
- **Application timing**: When and how often to apply
- **Soil management**: pH adjustment, organic matter
- **Long-term strategy**: Sustainable nutrition program

Explain your reasoning and provide confidence levels for your assessments.""",
                "focus": "nutritional analysis"
            },
            
            "environmental_focused": {
                "prompt": """You are a plant stress physiologist. Analyze environmental stress indicators:

## ENVIRONMENTAL STRESS ASSESSMENT:
Examine systematically for stress symptoms:

**WATER STRESS:**
- **Drought stress**: Wilting, leaf curl, reduced growth
- **Overwatering**: Root rot, yellowing, edema, fungal issues

**TEMPERATURE STRESS:**
- **Heat stress**: Scorching, wilting, reduced vigor
- **Cold damage**: Frost damage, chilling injury, growth cessation

**LIGHT CONDITIONS:**
- **Light stress**: Sun scald, bleaching, reduced photosynthesis
- **Shade stress**: Etiolation, weak growth, color changes

**PHYSICAL STRESS:**
- **Wind damage**: Torn leaves, broken branches, desiccation
- **Mechanical injury**: Cuts, bruises, compression damage

## STRESS DIAGNOSIS:
For each type of stress:
- **Symptom description**: Detailed visual characteristics
- **Distribution pattern**: Which parts of plant are affected
- **Timing factors**: When stress likely occurred
- **Severity level**: Extent of damage or stress response

## PHYSIOLOGICAL ANALYSIS:
Explain the plant's response:
- **Adaptive mechanisms**: How plant tries to cope
- **Damage progression**: How stress symptoms develop
- **Recovery potential**: Can the plant recover

## ENVIRONMENTAL MANAGEMENT:
Provide specific recommendations:
- **Immediate relief**: Emergency interventions
- **Environmental modification**: Changes to growing conditions
- **Protection strategies**: Preventing future stress
- **Recovery support**: Helping plant regain health

Be specific about environmental conditions and management practices.""",
                "focus": "environmental stress factors"
            }
        }
    
    def _get_device(self):
        """Determine the best available device for model execution"""
        if torch.backends.mps.is_available():
            logger.info("Using MPS (Apple Silicon) acceleration")
            return torch.device("mps")
        elif torch.cuda.is_available():
            logger.info("Using CUDA acceleration")
            return torch.device("cuda")
        else:
            logger.info("Using CPU")
            return torch.device("cpu")
    
    def _load_model(self):
        """Load the SmolVLM model and processor"""
        try:
            logger.info(f"Loading SmolVLM model '{self.model_name}' on {self.device}...")
            
            # Load processor with caching
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                cache_dir=None,  # Use default cache
                local_files_only=False  # Allow downloading if needed
            )
            
            # Load model with device-specific optimizations and caching
            if self.device.type == "cuda":
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.bfloat16,
                    _attn_implementation="flash_attention_2",
                    device_map="auto",
                    cache_dir=None,
                    local_files_only=False
                )
            elif self.device.type == "mps":
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    _attn_implementation="eager",
                    low_cpu_mem_usage=True,
                    cache_dir=None,
                    local_files_only=False
                ).to(self.device)
            else:
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    _attn_implementation="eager",
                    cache_dir=None,
                    local_files_only=False
                ).to(self.device)
            
            logger.info("SmolVLM Plant Doctor loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise RuntimeError(f"Failed to load SmolVLM model: {str(e)}")
    
    def diagnose_plant(self, image, analysis_type="general_diagnosis", plant_context="", 
                      detail_level="comprehensive"):
        """
        Diagnose plant health issues
        
        Args:
            image: PIL Image object
            analysis_type: Type of analysis ("general_diagnosis", "disease_focused", etc.)
            plant_context: Additional context (plant type, growing conditions, etc.)
            detail_level: "basic", "comprehensive", or "expert"
        
        Returns:
            Complete plant health analysis
        """
        try:
            logger.info(f"Analyzing plant health with {analysis_type} focus")
            
            # Input validation
            if image is None:
                return {"error": "No image provided"}
            
            if not isinstance(image, Image.Image):
                return {"error": "Invalid image format. Please upload a valid image file."}
            
            # Prepare image
            try:
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Resize large images for optimal processing
                max_size = 1024
                if max(image.size) > max_size:
                    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
            except Exception as e:
                logger.error(f"Image processing error: {e}")
                return {"error": "Could not process the uploaded image."}
            
            # Build analysis prompt
            prompt = self._build_analysis_prompt(analysis_type, plant_context, detail_level)
            logger.info(f"Analysis prompt created: {len(prompt)} characters")
            
            # Create prompt format for SmolVLM - Fixed format
            formatted_prompt = f"<|im_start|>user\n<image>\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            # Process inputs
            inputs = self._process_inputs_robust(formatted_prompt, image)
            if isinstance(inputs, str):  # Error message
                return {"error": inputs}
            
            # Generate analysis with SmolVLM - Enhanced parameters for detailed responses
            logger.info("Starting plant health analysis...")
            try:
                with torch.no_grad():
                    generated_ids = self.model.generate(
                        **inputs,
                        max_new_tokens=500,      # Increased for detailed analysis
                        min_new_tokens=100,     # Ensure minimum length
                        temperature=0.7,        # Higher for more varied responses
                        top_p=0.95,            # Slightly higher for creativity
                        top_k=50,              # Add top-k sampling
                        do_sample=True,
                        pad_token_id=self.processor.tokenizer.eos_token_id,
                        eos_token_id=self.processor.tokenizer.eos_token_id,
                        repetition_penalty=1.1,
                        no_repeat_ngram_size=3,  # Prevent repetitive phrases
                        early_stopping=False,    # Don't stop early
                        use_cache=True
                    )
                logger.info("Plant analysis completed")
            except Exception as e:
                logger.error(f"Generation error: {e}")
                return {"error": "Plant analysis failed. Please try again."}
            
            # Decode and extract analysis
            try:
                generated_texts = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
                full_text = generated_texts[0]
                
                logger.info(f"Full generated text length: {len(full_text)}")
                logger.info(f"Generated text preview: {full_text[:200]}...")
                
                # Extract the analysis from the generated text
                raw_analysis = self._extract_analysis(full_text)
                
                logger.info(f"Extracted analysis length: {len(raw_analysis)}")
                logger.info(f"Extracted analysis: {raw_analysis}")
                
                # If analysis is too short, try alternative extraction or return error
                if len(raw_analysis.strip()) < 50:
                    logger.warning("Analysis too short, attempting alternative extraction")
                    raw_analysis = self._extract_analysis_alternative(full_text)
                    
                    if len(raw_analysis.strip()) < 50:
                        logger.error("Still too short after alternative extraction")
                        return {"error": "Model generated insufficient analysis. Please try again with a different image."}
                
                # Process with plant health analyzer
                processed_results = self.plant_analyzer.process_analysis(
                    raw_analysis, 
                    analysis_type, 
                    plant_context
                )
                
                logger.info(f"Successfully completed plant diagnosis")
                return processed_results
                
            except Exception as e:
                logger.error(f"Analysis processing error: {e}")
                logger.error(traceback.format_exc())
                return {"error": "Could not process the plant analysis."}
                
        except Exception as e:
            logger.error(f"Unexpected error in plant diagnosis: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Sorry, there was an error analyzing your plant. Please try again."}
    
    def _build_analysis_prompt(self, analysis_type, plant_context, detail_level):
        """Build the analysis prompt based on type and context"""
        
        # Get base prompt for analysis type
        prompt_info = self.analysis_prompts.get(analysis_type, self.analysis_prompts["general_diagnosis"])
        base_prompt = prompt_info["prompt"]
        
        # Add plant context if provided
        context_addition = ""
        if plant_context.strip():
            context_addition = f"\n\n**PLANT CONTEXT:**\n{plant_context.strip()}\n\nConsider this context in your analysis."
        
        # Adjust detail level with explicit instructions
        detail_instruction = ""
        if detail_level == "basic":
            detail_instruction = "\n\n**RESPONSE REQUIREMENTS:**\nProvide a concise but complete analysis (at least 200 words). Focus on the most important observations and recommendations."
        elif detail_level == "expert":
            detail_instruction = "\n\n**RESPONSE REQUIREMENTS:**\nProvide a detailed technical analysis suitable for agricultural professionals (at least 400 words). Include scientific terminology and specific diagnostic criteria."
        else:  # comprehensive
            detail_instruction = "\n\n**RESPONSE REQUIREMENTS:**\nProvide a thorough analysis (at least 300 words). Be detailed but accessible to plant enthusiasts."
        
        # Add explicit formatting instructions
        format_instruction = "\n\n**FORMATTING:**\n- Use clear headings and sections\n- Provide specific observations\n- Explain your reasoning\n- Give actionable recommendations\n- Write in paragraph form, not bullet points\n- Be thorough and professional"
        
        # Combine all parts
        full_prompt = base_prompt + context_addition + detail_instruction + format_instruction
        
        # Add final instruction to encourage detailed response
        full_prompt += "\n\nIMPORTANT: Provide a comprehensive analysis with detailed explanations. Do not give one-word answers or brief responses."
        
        return full_prompt
    
    def _process_inputs_robust(self, prompt, image):
        """Robust input processing with multiple fallback methods"""
        
        processing_methods = [
            lambda: self.processor(text=prompt, images=image, return_tensors="pt"),
            lambda: self.processor(text=prompt, images=[image], return_tensors="pt"),
            lambda: self.processor(prompt, [image], return_tensors="pt"),
            lambda: self.processor(prompt, image, return_tensors="pt"),
        ]
        
        for i, method in enumerate(processing_methods, 1):
            try:
                logger.info(f"Trying processor method {i}")
                inputs = method()
                inputs = inputs.to(self.device)
                logger.info(f"Method {i} successful")
                return inputs
            except Exception as e:
                logger.warning(f"Method {i} failed: {e}")
                continue
        
        return "Error: Could not process the image. Please try with a different image."
    
    def _extract_analysis(self, full_text):
        """Extract the plant analysis from generated text"""
        logger.info(f"Extracting analysis from text of length: {len(full_text)}")
        
        # Try different extraction patterns
        extraction_patterns = [
            r"<\|im_start\|>assistant\n(.+?)(?:<\|im_end\|>|$)",
            r"assistant\n(.+?)(?:<\|im_end\|>|$)",
            r"<\|im_start\|>assistant(.+?)(?:<\|im_end\|>|$)",
            r"assistant(.+?)(?:<\|im_end\|>|$)"
        ]
        
        for pattern in extraction_patterns:
            match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
            if match:
                analysis = match.group(1).strip()
                if len(analysis) > 50:  # Only return if substantial content
                    logger.info(f"Extracted analysis using pattern: {pattern}")
                    return self._clean_analysis(analysis)
        
        # Fallback extraction - look for the assistant section
        if "assistant" in full_text.lower():
            parts = full_text.split("assistant", 1)
            if len(parts) > 1:
                analysis = parts[1].strip()
                # Remove any starting newlines or formatting
                analysis = re.sub(r'^[\n\s]*', '', analysis)
                if len(analysis) > 50:
                    return self._clean_analysis(analysis)
        
        # Final fallback - return cleaned full text if it's reasonable length
        cleaned = self._clean_analysis(full_text)
        if 100 < len(cleaned) < 3000:
            return cleaned
        
        return full_text.strip() if full_text.strip() else "No analysis generated."
    
    def _extract_analysis_alternative(self, full_text):
        """Alternative extraction method for stubborn cases"""
        logger.info("Trying alternative extraction method")
        
        # Look for content after common patterns
        patterns_to_try = [
            r"Answer:\s*(.+)",
            r"Analysis:\s*(.+)",
            r"Response:\s*(.+)",
            r"Diagnosis:\s*(.+)",
            r"(?:assistant|response)[:]*\s*(.+)"
        ]
        
        for pattern in patterns_to_try:
            match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
            if match:
                analysis = match.group(1).strip()
                if len(analysis) > 30:
                    logger.info(f"Alternative extraction successful with pattern: {pattern}")
                    return self._clean_analysis(analysis)
        
        # If still nothing, return the last substantial part
        sentences = full_text.split('.')
        if len(sentences) > 1:
            # Take the longest sentence or group of sentences
            longest_part = max(sentences, key=len)
            if len(longest_part.strip()) > 30:
                return self._clean_analysis(longest_part.strip() + '.')
        
        return full_text.strip()
    
    def _clean_analysis(self, analysis):
        """Clean and format the analysis text"""
        if not analysis:
            return "No analysis generated."
        
        # Remove unwanted tokens
        unwanted = ["<|im_end|>", "<|im_start|>", "assistant:", "user:", "<image>", "<|", "|>"]
        for token in unwanted:
            analysis = analysis.replace(token, "")
        
        # Clean whitespace and formatting
        analysis = re.sub(r'\s+', ' ', analysis)  # Replace multiple whitespace with single space
        analysis = re.sub(r'<[^>]*>', '', analysis)  # Remove HTML-like tags
        analysis = re.sub(r'[<>|]+\w*[<>|]*', '', analysis)  # Remove token artifacts
        
        # Ensure proper formatting
        analysis = analysis.strip()
        if analysis and not analysis.endswith(('.', '!', '?')):
            analysis += '.'
        
        # Remove very short responses
        if len(analysis.strip()) < 20:
            return "Analysis too brief. Please try again with a different image."
        
        return analysis
    
    def get_analysis_types(self):
        """Get available analysis types"""
        return list(self.analysis_prompts.keys())
    
    def clear_cache(self):
        """Clear GPU/MPS cache"""
        try:
            if self.device.type == "cuda":
                torch.cuda.empty_cache()
            elif self.device.type == "mps":
                torch.mps.empty_cache()
        except Exception as e:
            logger.warning(f"Could not clear cache: {e}")

# Singleton pattern
plant_doctor = None

def get_plant_doctor():
    global plant_doctor
    if plant_doctor is None:
        plant_doctor = SmolVLMPlantDoctor()
    return plant_doctor

def clear_model_cache():
    global plant_doctor
    if plant_doctor is not None:
        plant_doctor.clear_cache()
        del plant_doctor.model
        del plant_doctor.processor
        plant_doctor = None