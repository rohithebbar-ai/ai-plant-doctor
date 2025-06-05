# gradio_app.py - AI Plant Doctor Simple Landing Page with SmolVLM Integration

import gradio as gr
import logging
from PIL import Image
import traceback
import time
from model_handler import get_plant_doctor
from utils import format_diagnosis_report

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Professional CSS with natural leaf background
CUSTOM_CSS = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Global Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, .gradio-container {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), 
                url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2071&q=80') center center;
    background-size: cover;
    background-attachment: fixed;
    min-height: 100vh;
    color: #2c3e2d;
}

/* Main container styles */
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.content-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 3rem 2rem;
    max-width: 700px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    animation: fadeInUp 1s ease-out;
    margin: 0 auto;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #27ae60;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.subtitle {
    font-size: 1.4rem;
    color: #34495e;
    font-weight: 500;
    margin-bottom: 1.5rem;
}

.description {
    font-size: 1.1rem;
    color: #7f8c8d;
    line-height: 1.7;
    margin-bottom: 2rem;
}

.upload-zone {
    border: 3px dashed #27ae60 !important;
    border-radius: 20px !important;
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.05), rgba(39, 174, 96, 0.1)) !important;
    padding: 4rem 2rem !important;
    margin: 1rem 0 !important;
    transition: all 0.4s ease !important;
    cursor: pointer !important;
}

.upload-zone:hover {
    border-color: #219a52 !important;
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.1), rgba(39, 174, 96, 0.2)) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(39, 174, 96, 0.2) !important;
}

.upload-text {
    color: #27ae60;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.upload-subtext {
    color: #7f8c8d;
    font-size: 1rem;
}

.analyze-btn {
    background: linear-gradient(135deg, #27ae60, #219a52) !important;
    color: white !important;
    border: none !important;
    padding: 1.2rem 3rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 50px !important;
    cursor: pointer !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-top: 2rem !important;
    width: 100% !important;
}

.analyze-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #219a52, #1e8449) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 35px rgba(39, 174, 96, 0.4) !important;
}

.analyze-btn:disabled {
    background: linear-gradient(135deg, #95a5a6, #7f8c8d) !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: 0 4px 15px rgba(149, 165, 166, 0.3) !important;
}

/* Loading styles */
.loading-spinner {
    width: 80px;
    height: 80px;
    border: 6px solid #f3f3f3;
    border-top: 6px solid #27ae60;
    border-radius: 50%;
    animation: spin 1.5s linear infinite;
    margin: 0 auto 2rem auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    font-size: 1.5rem;
    color: #27ae60;
    font-weight: 600;
    margin-bottom: 1rem;
}

.loading-subtext {
    font-size: 1rem;
    color: #7f8c8d;
    line-height: 1.6;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background-color: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
    margin: 1.5rem 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #27ae60, #219a52);
    border-radius: 4px;
    animation: progress 3s ease-in-out;
}

@keyframes progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
}

/* Results styles */
.results-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #27ae60;
    margin-bottom: 0.5rem;
}

.results-subtitle {
    font-size: 1.2rem;
    color: #7f8c8d;
    margin-bottom: 2rem;
}

.results-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 2rem;
    max-width: 1000px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    text-align: left;
    margin: 0 auto;
}

.diagnosis-content {
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid #e8f5e9;
    border-radius: 15px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.back-btn {
    background: linear-gradient(135deg, #3498db, #2980b9) !important;
    color: white !important;
    border: none !important;
    padding: 1rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 25px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin: 1rem 0 !important;
}

.back-btn:hover {
    background: linear-gradient(135deg, #2980b9, #21618c) !important;
    transform: translateY(-2px) !important;
}

/* Diagnosis specific styles */
.diagnosis-card {
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1px solid #e8f5e9 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin: 1rem 0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.3s ease !important;
}

.diagnosis-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12) !important;
}

.diagnosis-card h3 {
    color: #27ae60 !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
    border-bottom: 2px solid #e8f5e9 !important;
    padding-bottom: 0.5rem !important;
}

.diagnosis-card p, .diagnosis-card li {
    color: #2c3e2d !important;
    line-height: 1.6 !important;
    margin: 0.5rem 0 !important;
}

.diagnosis-card strong {
    color: #27ae60 !important;
    font-weight: 600 !important;
}

/* Treatment Cards */
.treatment-card {
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.05), rgba(39, 174, 96, 0.1)) !important;
    border: 1px solid rgba(39, 174, 96, 0.2) !important;
    border-radius: 10px !important;
    padding: 1.2rem !important;
    margin: 0.8rem 0 !important;
    border-left: 4px solid #27ae60 !important;
    transition: all 0.3s ease !important;
}

.treatment-card:hover {
    transform: translateX(5px) !important;
    box-shadow: 0 4px 15px rgba(39, 174, 96, 0.15) !important;
}

.treatment-card h4 {
    color: #1e8449 !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.8rem !important;
}

.treatment-card p, .treatment-card li {
    color: #2c3e2d !important;
    line-height: 1.5 !important;
}

/* Severity Indicators */
.severity-none, .severity-healthy {
    border-left: 6px solid #27ae60 !important;
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.05), rgba(39, 174, 96, 0.1)) !important;
}

.severity-mild {
    border-left: 6px solid #f39c12 !important;
    background: linear-gradient(135deg, rgba(243, 156, 18, 0.05), rgba(243, 156, 18, 0.1)) !important;
}

.severity-moderate {
    border-left: 6px solid #e67e22 !important;
    background: linear-gradient(135deg, rgba(230, 126, 34, 0.05), rgba(230, 126, 34, 0.1)) !important;
}

.severity-high {
    border-left: 6px solid #e74c3c !important;
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.05), rgba(231, 76, 60, 0.1)) !important;
}

/* Emergency Alert */
.emergency-alert {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.1), rgba(231, 76, 60, 0.15)) !important;
    border: 2px solid #e74c3c !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin: 1rem 0 !important;
    animation: pulse 2s infinite !important;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
    100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
}

.emergency-alert h3, .emergency-alert p, .emergency-alert li {
    color: #c0392b !important;
    font-weight: 600 !important;
}

/* Analysis configuration styles - Better visibility */
.config-container {
    margin: 2rem 0;
    max-width: 800px;
    width: 100%;
}

.config-card {
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(20px) !important;
    border: 2px solid rgba(39, 174, 96, 0.3) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2) !important;
    margin: 0 auto !important;
}

/* Enhanced form controls for better visibility */
.config-card .gradio-dropdown,
.config-card .gradio-textbox {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e0e0e0 !important;
    border-radius: 10px !important;
    font-size: 1rem !important;
    padding: 0.8rem !important;
}

.config-card .gradio-dropdown:focus,
.config-card .gradio-textbox:focus {
    border-color: #27ae60 !important;
    box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1) !important;
    outline: none !important;
}

.config-card label {
    color: #2c3e2d !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .title {
        font-size: 2.5rem;
    }
    
    .content-card, .results-card {
        padding: 2rem 1.5rem;
        margin: 1rem;
    }
    
    .upload-zone {
        padding: 3rem 1rem !important;
    }
}
"""

def get_landing_page():
    """Return HTML for landing page"""
    return """
    <div class="content-card">
        <div class="title">🌿 AI Plant Doctor</div>
        <div class="subtitle">Intelligent Plant Health Analysis</div>
        <div class="description">
            Upload a photo of your plant and let our advanced AI diagnose diseases, 
            identify nutrient deficiencies, and provide expert treatment recommendations.
        </div>
    </div>
    """

def get_upload_section():
    """Return HTML for upload section - No longer needed"""
    return ""

def get_loading_page():
    """Return HTML for loading page"""
    return """
    <div class="content-card">
        <div class="loading-spinner"></div>
        <div class="loading-text">🌱 Analyzing Your Plant</div>
        <div class="loading-subtext">
            Our AI is carefully examining your plant image...<br>
            This may take a few moments for the most accurate diagnosis.
        </div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
    """

def get_results_page(diagnosis_html):
    """Return HTML for results page"""
    return f"""
    <div class="results-card">
        <div class="results-title">📊 Diagnosis Complete</div>
        <div class="results-subtitle">Here's what our AI found about your plant</div>
        <div style="margin-top: 1rem;">
            {diagnosis_html}
        </div>
    </div>
    """

def diagnose_plant_health(image, analysis_type="general_diagnosis", plant_info="", detail_level="comprehensive"):
    """Main function to diagnose plant health issues using SmolVLM"""
    try:
        if image is None:
            return "❌ Please upload an image of your plant first.", "", ""
        
        logger.info(f"Starting plant diagnosis with {analysis_type} analysis")
        
        # Get the plant doctor instance
        plant_doctor = get_plant_doctor()
        
        # Perform diagnosis with SmolVLM
        results = plant_doctor.diagnose_plant(
            image=image,
            analysis_type=analysis_type,
            plant_context=plant_info,
            detail_level=detail_level
        )
        
        # Check for errors
        if "error" in results:
            error_msg = results["error"]
            logger.error(f"Plant diagnosis error: {error_msg}")
            return f"❌ Error: {error_msg}", "", ""
        
        # Format the results using your existing formatter
        diagnosis_report = format_diagnosis_report(results)
        raw_analysis = results.get("raw_analysis", "No detailed analysis available.")
        recommendations = results.get("recommendations", "No specific recommendations available.")
        
        logger.info("Plant diagnosis completed successfully")
        return diagnosis_report, raw_analysis, recommendations
        
    except Exception as e:
        error_msg = f"Unexpected error during diagnosis: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return f"❌ {error_msg}", "", ""

def create_plant_doctor_interface():
    """Create the simple landing page interface with SmolVLM integration"""
    
    with gr.Blocks(css=CUSTOM_CSS, title="🌱 AI Plant Doctor") as app:
        
        with gr.Column(elem_classes=["main-container"]):
            # Main display area
            main_display = gr.HTML(value=get_landing_page())
            
            # Single image upload section
            with gr.Row():
                image_input = gr.Image(
                    label="📷 Drop your plant image here or click to browse and select a file",
                    type="pil",
                    height=300,
                    elem_classes=["upload-zone"],
                    container=True,
                    visible=True,
                    sources=["upload"]  # Only allow file upload, no webcam
                )
            
            # Analysis configuration (initially hidden) - Better visibility
            with gr.Column(visible=False, elem_classes=["config-container"]) as config_section:
                with gr.Column(elem_classes=["config-card"]):
                    gr.HTML('<div style="text-align: center; margin-bottom: 1.5rem;"><h3 style="color: #27ae60; font-size: 1.4rem; margin: 0;">⚙️ Analysis Options</h3></div>')
                    
                    with gr.Row():
                        with gr.Column(scale=1):
                            analysis_type = gr.Dropdown(
                                choices=[
                                    ("🔍 General Health Check", "general_diagnosis"),
                                    ("🦠 Disease Detection", "disease_focused"), 
                                    ("🌱 Nutrient Analysis", "nutrient_focused"),
                                    ("🌡️ Environmental Stress", "environmental_focused")
                                ],
                                value="general_diagnosis",
                                label="Analysis Type"
                            )
                        
                        with gr.Column(scale=1):
                            detail_level = gr.Dropdown(
                                choices=[
                                    ("📋 Basic Analysis", "basic"),
                                    ("📊 Comprehensive Report", "comprehensive"),
                                    ("🔬 Expert Analysis", "expert")
                                ],
                                value="comprehensive",
                                label="Detail Level"
                            )
                    
                    plant_info = gr.Textbox(
                        label="Plant Context (Optional)",
                        placeholder="e.g., 'Tomato plant, grown outdoors, watered daily, symptoms appeared 3 days ago'",
                        lines=2
                    )
            
            # Analyze button
            analyze_btn = gr.Button(
                "🔬 Analyze My Plant",
                elem_classes=["analyze-btn"],
                interactive=False,
                visible=True
            )
            
            # Back button (initially hidden)
            back_btn = gr.Button(
                "🏠 Analyze Another Plant",
                elem_classes=["back-btn"],
                visible=False
            )
            
            # Hidden outputs for detailed analysis and recommendations - Centered
            with gr.Column(visible=False) as detailed_section:
                with gr.Row():
                    with gr.Column():
                        with gr.Accordion("🔬 Detailed AI Analysis", open=False):
                            raw_analysis_output = gr.Textbox(
                                label="Raw Analysis from SmolVLM",
                                lines=10,
                                max_lines=20,
                                show_copy_button=True,
                                placeholder="Detailed AI analysis will appear here..."
                            )
                    
                    with gr.Column():
                        with gr.Accordion("💊 Treatment Recommendations", open=False):
                            recommendations_output = gr.Markdown(
                                value="Treatment recommendations will appear here after analysis..."
                            )
        
        def enable_analyze_button(image):
            """Enable analyze button and show config when image is uploaded"""
            if image is not None:
                return (
                    gr.update(interactive=True),   # analyze_btn
                    gr.update(visible=True)        # config_section
                )
            else:
                return (
                    gr.update(interactive=False),  # analyze_btn
                    gr.update(visible=False)       # config_section
                )
        
        def start_analysis(image, analysis_type, plant_info, detail_level):
            """Show loading page and hide upload elements"""
            if image is None:
                return (
                    get_landing_page(),
                    gr.update(visible=True),   # image_input
                    gr.update(visible=False),  # config_section
                    gr.update(visible=True, interactive=False),   # analyze_btn
                    gr.update(visible=False),  # back_btn
                    gr.update(visible=False),  # detailed_section
                    "",  # raw_analysis_output
                    ""   # recommendations_output
                )
            
            return (
                get_loading_page(),
                gr.update(visible=False),  # image_input
                gr.update(visible=False),  # config_section
                gr.update(visible=False),  # analyze_btn
                gr.update(visible=False),  # back_btn
                gr.update(visible=False),  # detailed_section
                "",  # raw_analysis_output
                ""   # recommendations_output
            )
        
        def complete_analysis(image, analysis_type, plant_info, detail_level):
            """Show results page with actual SmolVLM analysis"""
            diagnosis_html, raw_analysis, recommendations = diagnose_plant_health(
                image, analysis_type, plant_info, detail_level
            )
            
            return (
                get_results_page(diagnosis_html),
                gr.update(visible=False),  # image_input
                gr.update(visible=False),  # config_section
                gr.update(visible=False),  # analyze_btn
                gr.update(visible=True),   # back_btn
                gr.update(visible=True),   # detailed_section
                raw_analysis,              # raw_analysis_output
                recommendations            # recommendations_output
            )
        
        def reset_to_landing():
            """Reset to landing page"""
            return (
                None,  # clear image
                get_landing_page(),
                gr.update(visible=True),   # image_input
                gr.update(visible=False),  # config_section
                gr.update(visible=True, interactive=False),   # analyze_btn
                gr.update(visible=False),  # back_btn
                gr.update(visible=False),  # detailed_section
                "",  # raw_analysis_output
                ""   # recommendations_output
            )
        
        # Event handlers
        image_input.change(
            fn=enable_analyze_button,
            inputs=[image_input],
            outputs=[analyze_btn, config_section]
        )
        
        # Event handlers - Fixed output counting
        image_input.change(
            fn=enable_analyze_button,
            inputs=[image_input],
            outputs=[analyze_btn, config_section]
        )
        
        analyze_btn.click(
            fn=start_analysis,
            inputs=[image_input, analysis_type, plant_info, detail_level],
            outputs=[main_display, image_input, config_section, analyze_btn, back_btn, detailed_section, raw_analysis_output, recommendations_output]
        ).then(
            fn=complete_analysis,
            inputs=[image_input, analysis_type, plant_info, detail_level],
            outputs=[main_display, image_input, config_section, analyze_btn, back_btn, detailed_section, raw_analysis_output, recommendations_output]
        )
        
        back_btn.click(
            fn=reset_to_landing,
            outputs=[image_input, main_display, image_input, config_section, analyze_btn, back_btn, detailed_section, raw_analysis_output, recommendations_output]
        )
    
    return app

def main():
    """Launch the AI Plant Doctor application"""
    try:
        logger.info("Starting AI Plant Doctor Landing Page with SmolVLM...")
        
        # Create the interface
        app = create_plant_doctor_interface()
        
        # Launch the app
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            favicon_path=None
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()