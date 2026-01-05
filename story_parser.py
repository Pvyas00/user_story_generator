import json

class StoryParser:
    def __init__(self):
        self.required_fields = [
            'business_goal', 'actor', 'trigger', 'preconditions', 'functional_flow',
            'validations', 'acceptance_criteria', 'security', 'dependencies', 'risks'
        ]
    
    def parse_story(self, story_data):
        """Parse and validate story data from LLM response"""
        if isinstance(story_data, str):
            try:
                story_data = json.loads(story_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format in story data")
        
        if not isinstance(story_data, dict):
            raise ValueError("Story data must be a dictionary")
        
        # Validate and clean story data
        parsed_story = {}
        
        for field in self.required_fields:
            value = story_data.get(field, '')
            
            if field in ['preconditions', 'functional_flow', 'validations', 
                        'acceptance_criteria', 'security', 'dependencies', 'risks']:
                # Ensure arrays
                if isinstance(value, str):
                    parsed_story[field] = [value] if value.strip() else []
                elif isinstance(value, list):
                    parsed_story[field] = [str(item).strip() for item in value if str(item).strip()]
                else:
                    parsed_story[field] = []
            else:
                # String fields
                parsed_story[field] = str(value).strip() if value else ''
        
        # Validate required fields have content
        if not parsed_story.get('business_goal'):
            parsed_story['business_goal'] = 'Improve system functionality and user experience'
        
        if not parsed_story.get('actor'):
            parsed_story['actor'] = 'System User'
        
        return parsed_story
    
    def validate_story(self, story_data):
        """Validate story completeness"""
        errors = []
        
        if not story_data.get('business_goal'):
            errors.append('Business goal is required')
        
        if not story_data.get('actor'):
            errors.append('Actor is required')
        
        if not story_data.get('functional_flow'):
            errors.append('Functional flow is required')
        
        return errors
    
    def format_story_for_display(self, story_data):
        """Format story data for UI display"""
        formatted = {}
        
        # Format string fields
        for field in ['business_goal', 'actor', 'trigger']:
            formatted[field] = story_data.get(field, '')
        
        # Format array fields
        array_fields = [
            'preconditions', 'functional_flow', 'validations',
            'acceptance_criteria', 'security', 'dependencies', 'risks'
        ]
        
        for field in array_fields:
            items = story_data.get(field, [])
            if isinstance(items, list):
                formatted[field] = items
            else:
                formatted[field] = [str(items)] if items else []
        
        return formatted