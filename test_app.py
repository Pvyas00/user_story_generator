from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return "App is working!"

@app.route('/test')
def test():
    return jsonify({'status': 'working', 'message': 'Test endpoint successful'})

@app.route('/analyze', methods=['POST'])
def analyze_requirement():
    try:
        data = request.get_json()
        requirement = data.get('requirement', '').strip()
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Simple test response
        result = {
            'coverage_analysis': {
                'missing_fields': [],
                'coverage_score': 85,
                'suggestions': ['Test suggestion']
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)