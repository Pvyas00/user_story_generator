# Fallback data constants for when API calls fail

DEFAULT_COVERAGE_ANALYSIS = {
    'coverage_analysis': {
        'present_elements': [
            {
                'element': 'Business Goal',
                'status': 'present',
                'details': 'Basic goal mentioned',
                'content': 'System improvement'
            }
        ],
        'missing_elements': [
            {
                'element': 'Security',
                'status': 'missing',
                'details': 'No security considerations mentioned',
                'suggested_content': 'Authentication and authorization required',
                'editable': True
            },
            {
                'element': 'Dependencies',
                'status': 'missing', 
                'details': 'External dependencies not specified',
                'suggested_content': 'Database, APIs, third-party services',
                'editable': True
            }
        ],
        'overall_score': 60,
        'enterprise_readiness': 'Needs Enhancement',
        'editable_recommendations': [
            {
                'element': 'Security',
                'question': 'What security measures should be implemented?',
                'suggested_answer': 'User authentication, role-based access control, data encryption',
                'field_type': 'textarea'
            },
            {
                'element': 'Dependencies',
                'question': 'What external systems or services are required?',
                'suggested_answer': 'Database server, authentication service, notification system',
                'field_type': 'textarea'
            },
            {
                'element': 'Acceptance Criteria',
                'question': 'What are the specific success conditions?',
                'suggested_answer': 'Feature works correctly, performance meets requirements, user satisfaction',
                'field_type': 'textarea'
            }
        ]
    }
}

DEFAULT_STORY_DATA = {
    'business_goal': 'Improve system functionality and user experience',
    'actor': 'System User',
    'trigger': 'User action or system event',
    'preconditions': ['User must be authenticated', 'System must be available'],
    'functional_flow': [
        'User performs action', 
        'System processes request', 
        'System validates input',
        'System returns response'
    ],
    'validations': ['Input validation required', 'Business rule validation'],
    'acceptance_criteria': [
        'Feature works as expected',
        'Performance meets requirements',
        'Error handling works correctly'
    ],
    'security': ['Authentication required', 'Authorization controls'],
    'dependencies': ['Database connection', 'External APIs'],
    'risks': ['System downtime possible', 'Data integrity risks']
}