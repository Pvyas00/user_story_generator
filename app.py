from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
import json
import tempfile
import base64
from werkzeug.utils import secure_filename
from llm_client import GroqClient
from story_parser import StoryParser
from story_exporter_enhanced import EnhancedStoryExporter
from field_questions import REQUIRED_FIELDS
from brd_field_questions import BRD_REQUIRED_FIELDS
from frd_field_questions import FRD_REQUIRED_FIELDS
from cr_field_questions import CR_REQUIRED_FIELDS
from srd_field_questions import SRD_REQUIRED_FIELDS

import secrets

load_dotenv()

app = Flask(__name__)
# Generate secure secret key if not provided
default_secret = secrets.token_hex(32) if os.getenv('FLASK_ENV') == 'development' else None
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default_secret)

# File upload configuration
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx'}

# Initialize components
groq_client = GroqClient()
story_parser = StoryParser()
story_exporter = EnhancedStoryExporter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_requirement():   
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Analyze requirement coverage using LLM
        coverage_analysis = groq_client.analyze_requirement_coverage(requirement)
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            result = coverage_analysis
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Generate user story using LLM with coverage analysis
        story_data = groq_client.generate_story(requirement, answers, coverage_analysis)
        
        if not story_data:
            return jsonify({'error': 'Failed to generate user story'}), 500
        
        # Parse and validate story
        if story_parser:
            parsed_story = story_parser.parse_story(story_data)
        else:
            parsed_story = story_data
        
        return jsonify(parsed_story)
    
    except Exception as e:
        app.logger.error(f"Story generation error: {str(e)}")
        return jsonify({'error': f'Story generation failed: {str(e)}'}), 500

@app.route('/export/<format_type>', methods=['POST'])
def export_story(format_type):
    try:
        data = request.get_json()
        story_data = data.get('story_data')
        coverage_data = data.get('coverage_data')
        section_images = data.get('section_images', {})
        
        if not story_data:
            return jsonify({'error': 'Story data is required'}), 400
        
        if format_type not in ['word', 'pdf']:
            return jsonify({'error': 'Invalid export format'}), 400
        
        # Generate export file with enhanced features
        file_path = story_exporter.export_story(story_data, format_type, coverage_data, section_images)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Export failed'}), 500
        
        # Determine MIME type
        mime_types = {
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf'
        }
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"user_story.{format_type if format_type != 'word' else 'docx'}",
            mimetype=mime_types[format_type]
        )
    
    except Exception as e:
        app.logger.error(f"Export error: {str(e)}")
        print(f"Error in export_story: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/analyze_brd', methods=['POST'])
def analyze_brd_requirement():   
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Analyze BRD requirement coverage using LLM
        coverage_analysis = groq_client.analyze_brd_requirement_coverage(requirement)
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze BRD requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            result = coverage_analysis
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"BRD Analysis error: {str(e)}")
        return jsonify({'error': f'BRD Analysis failed: {str(e)}'}), 500

@app.route('/generate_brd', methods=['POST'])
def generate_brd():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Generate BRD using LLM with coverage analysis
        brd_data = groq_client.generate_brd(requirement, answers, coverage_analysis)
        
        if not brd_data:
            return jsonify({'error': 'Failed to generate BRD'}), 500
        
        return jsonify(brd_data)
    
    except Exception as e:
        app.logger.error(f"BRD generation error: {str(e)}")
        return jsonify({'error': f'BRD generation failed: {str(e)}'}), 500

@app.route('/export_brd/<format_type>', methods=['POST'])
def export_brd(format_type):
    try:
        data = request.get_json()
        brd_data = data.get('brd_data')
        coverage_data = data.get('coverage_data')
        section_images = data.get('section_images', {})
        
        if not brd_data:
            return jsonify({'error': 'BRD data is required'}), 400
        
        if format_type not in ['word', 'pdf']:
            return jsonify({'error': 'Invalid export format'}), 400
        
        # Generate BRD export file with enhanced features
        file_path = story_exporter.export_brd(brd_data, format_type, coverage_data, section_images)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'BRD Export failed'}), 500
        
        # Determine MIME type
        mime_types = {
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf'
        }
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"business_requirements_document.{format_type if format_type != 'word' else 'docx'}",
            mimetype=mime_types[format_type]
        )
    
    except Exception as e:
        app.logger.error(f"BRD Export error: {str(e)}")
        print(f"Error in export_brd: {str(e)}")
        return jsonify({'error': f'BRD Export failed: {str(e)}'}), 500

@app.route('/analyze_frd', methods=['POST'])
def analyze_frd_requirement():   
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Analyze FRD requirement coverage using LLM
        coverage_analysis = groq_client.analyze_frd_requirement_coverage(requirement)
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze FRD requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            result = coverage_analysis
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"FRD Analysis error: {str(e)}")
        return jsonify({'error': f'FRD Analysis failed: {str(e)}'}), 500

@app.route('/generate_frd', methods=['POST'])
def generate_frd():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Generate FRD using LLM with coverage analysis
        frd_data = groq_client.generate_frd(requirement, answers, coverage_analysis)
        
        if not frd_data:
            return jsonify({'error': 'Failed to generate FRD'}), 500
        
        return jsonify(frd_data)
    
    except Exception as e:
        app.logger.error(f"FRD generation error: {str(e)}")
        return jsonify({'error': f'FRD generation failed: {str(e)}'}), 500

@app.route('/export_frd/<format_type>', methods=['POST'])
def export_frd(format_type):
    try:
        data = request.get_json()
        frd_data = data.get('frd_data')
        coverage_data = data.get('coverage_data')
        section_images = data.get('section_images', {})
        
        if not frd_data:
            return jsonify({'error': 'FRD data is required'}), 400
        
        if format_type not in ['word', 'pdf']:
            return jsonify({'error': 'Invalid export format'}), 400
        
        # Generate FRD export file with enhanced features
        file_path = story_exporter.export_frd(frd_data, format_type, coverage_data, section_images)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'FRD Export failed'}), 500
        
        # Determine MIME type
        mime_types = {
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf'
        }
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"functional_requirements_document.{format_type if format_type != 'word' else 'docx'}",
            mimetype=mime_types[format_type]
        )
    
    except Exception as e:
        app.logger.error(f"FRD Export error: {str(e)}")
        print(f"Error in export_frd: {str(e)}")
        return jsonify({'error': f'FRD Export failed: {str(e)}'}), 500

@app.route('/analyze_srd', methods=['POST'])
def analyze_srd_requirement():   
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Analyze SRD requirement coverage using LLM
        coverage_analysis = groq_client.analyze_srd_requirement_coverage(requirement)
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze SRD requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            result = coverage_analysis
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"SRD Analysis error: {str(e)}")
        return jsonify({'error': f'SRD Analysis failed: {str(e)}'}), 500

@app.route('/generate_srd', methods=['POST'])
def generate_srd():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Generate SRD using LLM with coverage analysis
        srd_data = groq_client.generate_srd(requirement, answers, coverage_analysis)
        
        if not srd_data:
            return jsonify({'error': 'Failed to generate SRD'}), 500
        
        return jsonify(srd_data)
    
    except Exception as e:
        app.logger.error(f"SRD generation error: {str(e)}")
        return jsonify({'error': f'SRD generation failed: {str(e)}'}), 500

@app.route('/analyze_cr', methods=['POST'])
def analyze_cr_requirement():   
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        attachments = data.get('attachments', [])
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Process attachments if any
        attachment_context = ""
        if attachments:
            attachment_context = f"\n\nAttached files context:\n"
            for att in attachments:
                attachment_context += f"- {att['name']} ({att['type']})\n"
                if att.get('content') and att['type'].startswith('image/'):
                    attachment_context += f"  [Image content available for analysis]\n"
        
        # Combine requirement with attachment context
        enhanced_requirement = requirement + attachment_context
        
        # Analyze CR requirement coverage using LLM
        coverage_analysis = groq_client.analyze_cr_requirement_coverage(enhanced_requirement)
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze CR requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            result = coverage_analysis
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"CR Analysis error: {str(e)}")
        return jsonify({'error': f'CR Analysis failed: {str(e)}'}), 500

@app.route('/generate_cr', methods=['POST'])
def generate_cr():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Check if groq_client is available
        if not groq_client:
            return jsonify({'error': 'GroqClient not initialized'}), 500
        
        # Generate CR using LLM with coverage analysis
        cr_data = groq_client.generate_cr(requirement, answers, coverage_analysis)
        
        if not cr_data:
            return jsonify({'error': 'Failed to generate CR'}), 500
        
        return jsonify(cr_data)
    
    except Exception as e:
        app.logger.error(f"CR generation error: {str(e)}")
        return jsonify({'error': f'CR generation failed: {str(e)}'}), 500

@app.route('/export_srd/<format_type>', methods=['POST'])
def export_srd(format_type):
    try:
        data = request.get_json()
        srd_data = data.get('srd_data')
        coverage_data = data.get('coverage_data')
        section_images = data.get('section_images', {})
        
        if not srd_data:
            return jsonify({'error': 'SRD data is required'}), 400
        
        if format_type not in ['word', 'pdf']:
            return jsonify({'error': 'Invalid export format'}), 400
        
        # Generate SRD export file with enhanced features
        file_path = story_exporter.export_srd(srd_data, format_type, coverage_data, section_images)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'SRD Export failed'}), 500
        
        # Determine MIME type
        mime_types = {
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf'
        }
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"system_requirements_document.{format_type if format_type != 'word' else 'docx'}",
            mimetype=mime_types[format_type]
        )
    
    except Exception as e:
        app.logger.error(f"SRD Export error: {str(e)}")
        print(f"Error in export_srd: {str(e)}")
        return jsonify({'error': f'SRD Export failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'groq_configured': bool(os.getenv('GROQ_API_KEY'))})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    if debug_mode:
        print("Starting Flask app...")
        print(f"GROQ_API_KEY configured: {bool(os.getenv('GROQ_API_KEY'))}")
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_attachment(base64_content):
    """Process base64 image content for AI analysis"""
    try:
        # Remove data URL prefix if present
        if base64_content.startswith('data:'):
            base64_content = base64_content.split(',')[1]
        
        # For now, just return a description that the image is available
        # In future, this could be enhanced with actual image analysis
        return "[Image attachment available for visual context analysis]"
    except Exception as e:
        return f"[Error processing image: {str(e)}]"