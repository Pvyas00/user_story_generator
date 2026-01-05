REQUIRED_FIELDS = [
    "Business Goal",
    "Actor", 
    "Trigger",
    "Preconditions",
    "Functional Flow",
    "Validations",
    "Acceptance Criteria",
    "Security",
    "Dependencies",
    "Risks"
]

FIELD_DESCRIPTIONS = {
    "Business Goal": "Why this feature exists, what business value it provides?",
    "Actor": "Who will use this feature (specific user types, roles)?",
    "Trigger": "What event or condition initiates this user story?",
    "Preconditions": "What must be true before this story can be executed?",
    "Functional Flow": "What are the step-by-step processes involved?",
    "Validations": "What data/input checks and validations are needed?",
    "Acceptance Criteria": "What specific conditions must be met for this story to be considered complete?",
    "Security": "What authentication, authorization, or security measures are required?",
    "Dependencies": "What external systems, services, or resources are required?",
    "Risks": "What potential issues might occur and how to mitigate them?"
}

def get_field_question(field_name):
    """Get the standard question for a field"""
    return FIELD_DESCRIPTIONS.get(field_name, f"Please provide details about {field_name}")

def get_recommended_answer(field_name, requirement_context=""):
    """Get AI-recommended answer based on field and context"""
    recommendations = {
        "Business Goal": "Improve user experience and business efficiency",
        "Actor": "End users, administrators, or system operators",
        "Trigger": "User action or system event",
        "Preconditions": "User must be authenticated and have required permissions",
        "Functional Flow": "Step-by-step process from initiation to completion",
        "Validations": "Input validation, business rule checks, data integrity",
        "Acceptance Criteria": "Given-When-Then scenarios covering main and edge cases",
        "Security": "User authentication required, role-based access control",
        "Dependencies": "Database, third-party APIs, file systems",
        "Risks": "System downtime, data loss, security breaches - mitigation strategies needed"
    }
    return recommendations.get(field_name, "To be determined based on requirements")

def get_expected_format(field_name):
    """Get expected answer format for a field"""
    formats = {
        "Business Goal": "text",
        "Actor": "text",
        "Trigger": "text",
        "Preconditions": "list",
        "Functional Flow": "list",
        "Validations": "list",
        "Acceptance Criteria": "list",
        "Security": "text",
        "Dependencies": "list",
        "Risks": "list"
    }
    return formats.get(field_name, "text")