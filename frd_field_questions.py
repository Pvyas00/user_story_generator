FRD_REQUIRED_FIELDS = [
    "System Overview",
    "Functional Requirements",
    "Data Requirements", 
    "Interface Requirements",
    "Integration Requirements",
    "Performance Requirements",
    "Security Requirements",
    "Validation Rules",
    "Error Handling",
    "Reporting Requirements",
    "Testing Requirements",
    "Deployment Requirements",
    "Maintenance Requirements",
    "Technical Specifications"
]

FRD_FIELD_DESCRIPTIONS = {
    "System Overview": "What is the system architecture and high-level design?",
    "Functional Requirements": "What are the detailed functional specifications and requirements?",
    "Data Requirements": "What data models, schemas, and storage requirements are needed?",
    "Interface Requirements": "What are the UI/API specifications and interface requirements?",
    "Integration Requirements": "What external system connections and integrations are needed?",
    "Performance Requirements": "What are the system performance criteria and benchmarks?",
    "Security Requirements": "What technical security measures and protocols are required?",
    "Validation Rules": "What data validation and business rules need to be implemented?",
    "Error Handling": "What exception handling strategies and error management approaches are needed?",
    "Reporting Requirements": "What reporting and analytics capabilities are required?",
    "Testing Requirements": "What testing strategies, criteria, and procedures are needed?",
    "Deployment Requirements": "What deployment and infrastructure requirements are needed?",
    "Maintenance Requirements": "What ongoing maintenance procedures and support are required?",
    "Technical Specifications": "What are the detailed technical specifications and implementation details?"
}

def get_frd_field_question(field_name):
    """Get the standard question for an FRD field"""
    return FRD_FIELD_DESCRIPTIONS.get(field_name, f"Please provide details about {field_name}")

def get_frd_recommended_answer(field_name, requirement_context=""):
    """Get AI-recommended answer based on FRD field and context"""
    recommendations = {
        "System Overview": "High-level system architecture with key components and technology stack",
        "Functional Requirements": "Detailed functional specifications with priorities and acceptance criteria",
        "Data Requirements": "Data models, database schemas, and storage requirements",
        "Interface Requirements": "User interface specifications and API endpoint definitions",
        "Integration Requirements": "External system connections, data formats, and integration methods",
        "Performance Requirements": "Response time, throughput, scalability, and performance benchmarks",
        "Security Requirements": "Authentication, authorization, encryption, and security protocols",
        "Validation Rules": "Input validation, data integrity checks, and business rule implementations",
        "Error Handling": "Exception handling strategies, error logging, and recovery procedures",
        "Reporting Requirements": "Report specifications, analytics capabilities, and data visualization needs",
        "Testing Requirements": "Unit testing, integration testing, and performance testing strategies",
        "Deployment Requirements": "Environment specifications, deployment procedures, and infrastructure needs",
        "Maintenance Requirements": "Monitoring, backup strategies, and ongoing maintenance procedures",
        "Technical Specifications": "Detailed technical implementation specifications and standards"
    }
    return recommendations.get(field_name, "To be determined based on technical requirements")

def get_frd_expected_format(field_name):
    """Get expected answer format for an FRD field"""
    formats = {
        "System Overview": "object",
        "Functional Requirements": "list",
        "Data Requirements": "object",
        "Interface Requirements": "object",
        "Integration Requirements": "list",
        "Performance Requirements": "object",
        "Security Requirements": "list",
        "Validation Rules": "list",
        "Error Handling": "list",
        "Reporting Requirements": "list",
        "Testing Requirements": "object",
        "Deployment Requirements": "object",
        "Maintenance Requirements": "object",
        "Technical Specifications": "list"
    }
    return formats.get(field_name, "text")