from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
import json
import tempfile
from llm_client import GroqClient
from story_parser import StoryParser
from story_exporter_enhanced import EnhancedStoryExporter
from field_questions import REQUIRED_FIELDS

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

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
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Clean requirement text to avoid encoding issues
        requirement = requirement.encode('ascii', 'ignore').decode('ascii')
        
        # Analyze requirement coverage using LLM
        coverage_analysis = groq_client.analyze_requirement_coverage(requirement)
        
        print(f"Debug - Requirement: {requirement}")
        print(f"Debug - Coverage Analysis: {coverage_analysis}")
        
        if not coverage_analysis:
            return jsonify({'error': 'Failed to analyze requirement coverage'}), 500
        
        # Ensure proper structure for frontend
        if 'coverage_analysis' not in coverage_analysis:
            # If response is direct coverage data, wrap it properly
            result = {
                'coverage_analysis': coverage_analysis
            }
        else:
            # If response already has coverage_analysis wrapper
            result = coverage_analysis
        
        print(f"Debug - Final Result: {result}")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in analyze_requirement: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        requirement = data.get('requirement', '').strip()
        answers = data.get('answers', {})
        coverage_analysis = data.get('coverage_analysis', {})
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Generate user story using LLM with coverage analysis
        story_data = groq_client.generate_story(requirement, answers, coverage_analysis)
        
        if not story_data:
            return jsonify({'error': 'Failed to generate user story'}), 500
        
        # Parse and validate story
        parsed_story = story_parser.parse_story(story_data)
        
        return jsonify(parsed_story)
    
    except Exception as e:
        return jsonify({'error': f'Story generation failed: {str(e)}'}), 500

@app.route('/export/<format_type>', methods=['POST'])
def export_story(format_type):
    try:
        data = request.get_json()
        story_data = data.get('story_data')
        coverage_data = data.get('coverage_data')
        
        if not story_data:
            return jsonify({'error': 'Story data is required'}), 400
        
        if format_type not in ['word', 'pdf', 'png']:
            return jsonify({'error': 'Invalid export format'}), 400
        
        # Generate export file with enhanced features
        file_path = story_exporter.export_story(story_data, format_type, coverage_data)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Export failed'}), 500
        
        # Determine MIME type
        mime_types = {
            'word': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'png': 'image/png'
        }
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"user_story.{format_type if format_type != 'word' else 'docx'}",
            mimetype=mime_types[format_type]
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'groq_configured': bool(os.getenv('GROQ_API_KEY'))})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)