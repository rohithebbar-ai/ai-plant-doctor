# model_handler.py - Final AI Plant Doctor with Quantized SmolVLM and Test Support

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, BitsAndBytesConfig
from PIL import Image
import logging
import traceback
import re
import os

from plant_health_analyzer import PlantHealthAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmolVLMPlantDoctor:
    def __init__(self, model_name="leon-se/SmolVLM-Instruct-W4A16-G128", use_quantization=False):
        """AI Plant Doctor using quantized SmolVLM optimized for deployment"""
        self.device = self._get_device()
        self.model_name = model_name
        self.use_quantization = use_quantization
        self.model = None
        self.processor = None
        self._test_mode = False
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
                "prompt": """You are a plant nutrition specialist. Conduct a detailed Nutritional assessment:

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
- **Mobile vs immobile Nutrients**: Where symptoms appear first

## DIFFERENTIAL DIAGNOSIS:
Consider:
- **Primary deficiency**: Most likely Nutrient shortage
- **Secondary factors**: pH, soil conditions, uptake issues
- **Toxicity symptoms**: Signs of Nutrient excess
- **Interaction effects**: How Nutrients affect each other

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
        if torch.cuda.is_available():
            logger.info("Using CUDA acceleration")
            return torch.device("cuda")
        else:
            # Force CPU instead of MPS for better stability with vision models
            logger.info("Using CPU for better model compatibility")
            return torch.device("cpu")
    
    def _load_model(self):
        """Load the pre-quantized SmolVLM model for optimal deployment performance"""
        try:
            logger.info(f"Loading SmolVLM model '{self.model_name}' on {self.device}...")
            
            # Load processor with caching
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                local_files_only=False
            )
            
            # Since leon-se/SmolVLM-Instruct-W4A16-G128 is already quantized,
            # we don't need runtime quantization - just load directly
            if self.device.type == "cuda":
                logger.info("Loading model for CUDA...")
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                    local_files_only=False,
                    torch_dtype=torch.float16  # Optimal for pre-quantized model
                )
            elif self.device.type == "mps":
                logger.info("Loading pre-quantized model for MPS...")
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                    local_files_only=False
                ).to(self.device)
            else:
                logger.info("Loading pre-quantized model for CPU...")
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                    local_files_only=False
                ).to(self.device)
            
            logger.info("Pre-quantized SmolVLM Plant Doctor loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading pre-quantized model: {e}")
            # Fallback to original model if pre-quantized fails
            logger.info("Falling back to original model...")
            self.model_name = "HuggingFaceTB/SmolVLM-Instruct"
            self._load_original_model()
    
    def _load_original_model(self):
        """Fallback method to load original model with runtime quantization"""
        try:
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                local_files_only=False
            )
            
            if self.device.type == "cuda" and self.use_quantization:
                logger.info("Applying runtime quantization...")
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                    cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                    local_files_only=False,
                    torch_dtype=torch.float16
                )
            else:
                self.model = AutoModelForVision2Seq.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    cache_dir=os.environ.get("TRANSFORMERS_CACHE", None),
                    local_files_only=False
                ).to(self.device)
                
            logger.info("Original model loaded as fallback")
        except Exception as e:
            logger.error(f"Failed to load fallback model: {e}")
            raise RuntimeError(f"Failed to load any SmolVLM model: {str(e)}")
    
    def diagnose_plant(self, image, analysis_type="general_diagnosis", plant_context="", 
                      detail_level="comprehensive"):
        """
        Diagnose plant health issues - Optimized for deployment with test support
        
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
            
            # Prepare image - Smart resizing (only if needed)
            try:
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Only resize if image is larger than optimal size
                max_size = 512
                width, height = image.size
                logger.info(f"Original image size: {width}x{height}")
                
                # Only resize if either dimension is larger than max_size
                if width > max_size or height > max_size:
                    # Calculate aspect ratio preserving resize
                    if width > height:
                        new_width = max_size
                        new_height = int((height * max_size) / width)
                    else:
                        new_height = max_size
                        new_width = int((width * max_size) / height)
                    
                    # Resize maintaining aspect ratio
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    logger.info(f"Resized image to: {new_width}x{new_height}")
                else:
                    logger.info(f"Image size OK, no resizing needed")
                
                logger.info(f"Final image size: {image.size}")
                    
            except Exception as e:
                logger.error(f"Image processing error: {e}")
                return {"error": "Could not process the uploaded image."}
            
            # Build analysis prompt
            prompt = self._build_analysis_prompt(analysis_type, plant_context, detail_level)
            logger.info(f"Analysis prompt created: {len(prompt)} characters")
            
            # Create prompt format for SmolVLM
            formatted_prompt = f"<|im_start|>user\n<image>\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            # Process inputs
            inputs = self._process_inputs_robust(formatted_prompt, image)
            if isinstance(inputs, str):  # Error message
                return {"error": inputs}
            
            # Generate analysis with optimized parameters for deployment
            logger.info("Starting plant health analysis...")
            try:
                with torch.no_grad():
                    # Check if we're in test mode to avoid actual model generation
                    if self._test_mode:
                        # Return a mock response for testing
                        logger.info("Test mode detected - returning mock response")
                        mock_response = "This is a comprehensive plant health analysis. The plant shows healthy green foliage with no visible signs of disease or nutrient deficiency. The leaves appear vibrant and well-formed, indicating proper care and growing conditions. Continue current care practices including regular watering and appropriate light exposure."
                        
                        processed_results = self.plant_analyzer.process_analysis(
                            mock_response, 
                            analysis_type, 
                            plant_context
                        )
                        return processed_results
                    
                    # Only proceed with actual generation if not in test mode
                    generated_ids = self.model.generate(
                        **inputs,
                        max_new_tokens=600,      # Balanced for speed and detail
                        min_new_tokens=100,
                        temperature=0.7,
                        top_p=0.9,
                        do_sample=True,
                        pad_token_id=self.processor.tokenizer.eos_token_id,
                        eos_token_id=self.processor.tokenizer.eos_token_id,
                        repetition_penalty=1.1,
                        use_cache=True
                    )
                logger.info("Plant analysis completed")
            except Exception as e:
                logger.error(f"Generation error: {e}")
                # In test mode, don't return an error for generation failures
                if self._test_mode:
                    logger.info("Test mode - returning mock response instead of error")
                    mock_response = "Mock plant analysis for testing purposes. The plant appears to be in good condition with no major issues detected."
                    processed_results = self.plant_analyzer.process_analysis(
                        mock_response, 
                        analysis_type, 
                        plant_context
                    )
                    return processed_results
                return {"error": "Plant analysis failed. Please try again."}
            
            # Decode and extract analysis
            try:
                generated_texts = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
                full_text = generated_texts[0]
                
                logger.info(f"Generated text length: {len(full_text)}")
                logger.info(f"Generated text preview: {full_text[:200]}...")
                
                # Extract the analysis
                raw_analysis = self._extract_analysis_fixed(full_text, formatted_prompt)
                
                logger.info(f"Extracted analysis length: {len(raw_analysis)}")
                logger.info(f"Extracted analysis preview: {raw_analysis[:200]}...")
                
                # Fallback for short responses
                if len(raw_analysis.strip()) < 50:
                    logger.warning("Analysis too short, using fallback with available content")
                    raw_analysis = f"Plant analysis: {full_text.strip()}" if full_text.strip() else "Unable to generate detailed analysis"
                
                # Process with plant health analyzer
                processed_results = self.plant_analyzer.process_analysis(
                    raw_analysis, 
                    analysis_type, 
                    plant_context
                )
                
                logger.info("Plant diagnosis completed successfully")
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
        """Build the analysis prompt based on type and context with proper detail level handling"""
        
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
    
    def _extract_analysis_fixed(self, full_text, original_prompt):
        """Fixed extraction method that handles various response formats"""
        logger.info(f"Extracting analysis from text of length: {len(full_text)}")
        
        # Remove the original prompt from the generated text to get only the response
        if original_prompt in full_text:
            response_part = full_text.replace(original_prompt, "").strip()
        else:
            # Try to find where the assistant response starts
            assistant_markers = [
                "<|im_start|>assistant",
                "assistant",
                "<|im_start|>assistant\n"
            ]
            
            response_part = full_text
            for marker in assistant_markers:
                if marker in full_text:
                    parts = full_text.split(marker, 1)
                    if len(parts) > 1:
                        response_part = parts[1]
                        break
        
        # Clean up the response
        response_part = self._clean_analysis_fixed(response_part)
        
        # If we still have a very short response, try alternative methods
        if len(response_part.strip()) < 50:
            logger.warning("Short response detected, trying alternative extraction")
            
            # Split by common delimiters and take the longest part
            potential_responses = []
            
            # Try splitting by various patterns
            for separator in ['\n\n', '. ', '?\n', '!\n']:
                parts = full_text.split(separator)
                for part in parts:
                    cleaned_part = self._clean_analysis_fixed(part)
                    if len(cleaned_part.strip()) > 30:
                        potential_responses.append(cleaned_part)
            
            if potential_responses:
                # Return the longest substantial response
                response_part = max(potential_responses, key=len)
        
        # Final validation
        if len(response_part.strip()) < 20:
            logger.warning("Still very short response, using full text as fallback")
            response_part = self._clean_analysis_fixed(full_text)
        
        logger.info(f"Final extracted analysis length: {len(response_part)}")
        return response_part.strip() if response_part.strip() else "Analysis could not be extracted properly."
    
    def _clean_analysis_fixed(self, analysis):
        """Improved cleaning method for analysis text"""
        if not analysis:
            return "No analysis generated."
        
        # Remove unwanted tokens and patterns
        unwanted_patterns = [
            r'<\|im_end\|>',
            r'<\|im_start\|>',
            r'<\|[^|]*\|>',  # Any token-like patterns
            r'assistant:?\s*',
            r'user:?\s*',
            r'<image>',
            r'^[\s\n]*',  # Leading whitespace/newlines
            r'[\s\n]*$',  # Trailing whitespace/newlines
        ]
        
        cleaned = analysis
        for pattern in unwanted_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        # Ensure proper sentence ending
        if cleaned and not cleaned.endswith(('.', '!', '?', ':')):
            cleaned += '.'
        
        return cleaned
    
    def _extract_analysis(self, full_text):
        """Legacy extraction method for backward compatibility"""
        return self._extract_analysis_fixed(full_text, "")
    
    def _extract_analysis_alternative(self, full_text):
        """Alternative extraction method for stubborn cases"""
        return self._extract_analysis_fixed(full_text, "")
    
    def _clean_analysis(self, analysis):
        """Legacy cleaning method for backward compatibility"""
        return self._clean_analysis_fixed(analysis)
    
    def get_analysis_types(self):
        """Get available analysis types"""
        return list(self.analysis_prompts.keys())
    
    def set_test_mode(self, test_mode=True):
        """Enable test mode to avoid actual model inference during testing"""
        self._test_mode = test_mode
        logger.info(f"Test mode {'enabled' if test_mode else 'disabled'}")
    
    def clear_cache(self):
        """Clear GPU/MPS cache"""
        try:
            if self.device.type == "cuda":
                torch.cuda.empty_cache()
            elif self.device.type == "mps":
                torch.mps.empty_cache()
        except Exception as e:
            logger.warning(f"Could not clear cache: {e}")

# Singleton pattern for deployment
plant_doctor = None

def get_plant_doctor(model_name=None, for_testing=False):
    global plant_doctor
    if plant_doctor is None:
        # Use original model by default due to MPS compatibility issues
        if for_testing:
            # Use original model name for tests
            default_model = "HuggingFaceTB/SmolVLM-Instruct"
        else:
            # Use original model for production due to MPS issues with quantized model
            default_model = "HuggingFaceTB/SmolVLM-Instruct"
        
        final_model_name = model_name or default_model
        
        plant_doctor = SmolVLMPlantDoctor(
            model_name=final_model_name,
            use_quantization=False  # Disable quantization for MPS compatibility
        )
        
        # Enable test mode if this is for testing
        if for_testing:
            plant_doctor.set_test_mode(True)
            
    return plant_doctor

def clear_model_cache():
    global plant_doctor
    if plant_doctor is not None:
        plant_doctor.clear_cache()
        del plant_doctor.model
        del plant_doctor.processor
        plant_doctor = None