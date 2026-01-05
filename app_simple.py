from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_requirement():   
    try:
        print("Analyze endpoint called")
        data = request.get_json()
        print(f"Received data: {data}")
        
        requirement = data.get('requirement', '').strip()
        print(f"Requirement: {requirement}")
        
        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400
        
        # Simple test response
        result = {
            'coverage_analysis': {
                'present_elements': ['Business Goal', 'Actor'],
                'missing_elements': ['Security', 'Dependencies'],
                'overall_score': 75,
                'enterprise_readiness': 'Medium'
            }
        }
        
        print(f"Returning result: {result}")
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in analyze_requirement: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'groq_configured': bool(os.getenv('GROQ_API_KEY'))})

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)