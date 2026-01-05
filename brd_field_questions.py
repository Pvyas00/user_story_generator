BRD_REQUIRED_FIELDS = [
    "Project Name",
    "Executive Summary",
    "Business Objectives", 
    "Scope",
    "Stakeholders",
    "Current State",
    "Future State",
    "Business Requirements",
    "Business Rules",
    "Assumptions",
    "Dependencies",
    "Risks",
    "Glossary",
    "Approval Section",
    "Document Control"
]

BRD_FIELD_DESCRIPTIONS = {
    "Project Name": "What is the clear project identification and name?",
    "Executive Summary": "What is the project background, problem statement, business need, solution, and expected benefits?",
    "Business Objectives": "What are the specific business objectives with measurable KPIs?",
    "Scope": "What features/functions are in-scope and out-of-scope for this project?",
    "Stakeholders": "Who are the key stakeholders with their roles, departments, and responsibilities?",
    "Current State": "What is the current AS-IS process description and what are the pain points?",
    "Future State": "What is the desired TO-BE process and expected improvements?",
    "Business Requirements": "What are the detailed business requirements with priorities and acceptance criteria?",
    "Business Rules": "What are the business logic rules (IF-THEN-ELSE conditions)?",
    "Assumptions": "What assumptions are being made about the project context and environment?",
    "Dependencies": "What external systems, services, or resources are required?",
    "Risks": "What potential business and technical risks exist and how to mitigate them?",
    "Glossary": "What business and technical terms need definition for clarity?",
    "Approval Section": "Who needs to approve this BRD and what is the approval workflow?",
    "Document Control": "What is the version history and who are the reviewers?"
}

def get_brd_field_question(field_name):
    """Get the standard question for a BRD field"""
    return BRD_FIELD_DESCRIPTIONS.get(field_name, f"Please provide details about {field_name}")

def get_brd_recommended_answer(field_name, requirement_context=""):
    """Get AI-recommended answer based on BRD field and context"""
    recommendations = {
        "Project Name": "Business Process Enhancement Project",
        "Executive Summary": "Project aims to improve business efficiency and user experience through process optimization",
        "Business Objectives": "Increase operational efficiency by 25%, reduce processing time by 50%, improve user satisfaction",
        "Scope": "Core business processes, user interfaces, reporting capabilities",
        "Stakeholders": "Business owners, end users, IT support, compliance team",
        "Current State": "Manual processes with inefficiencies and user pain points",
        "Future State": "Automated, streamlined processes with improved user experience",
        "Business Requirements": "Functional requirements with clear acceptance criteria and priorities",
        "Business Rules": "Business logic governing process flows and decision points",
        "Assumptions": "System availability, user training, resource allocation assumptions",
        "Dependencies": "External systems, third-party services, infrastructure requirements",
        "Risks": "Technical risks, business continuity risks, resource risks with mitigation strategies",
        "Glossary": "Key business and technical terms with clear definitions",
        "Approval Section": "Business stakeholder approval workflow and sign-off process",
        "Document Control": "Version management and review process"
    }
    return recommendations.get(field_name, "To be determined based on business requirements")

def get_brd_expected_format(field_name):
    """Get expected answer format for a BRD field"""
    formats = {
        "Project Name": "text",
        "Executive Summary": "object",
        "Business Objectives": "list",
        "Scope": "object",
        "Stakeholders": "list",
        "Current State": "object",
        "Future State": "object",
        "Business Requirements": "list",
        "Business Rules": "list",
        "Assumptions": "list",
        "Dependencies": "list",
        "Risks": "list",
        "Glossary": "list",
        "Approval Section": "text",
        "Document Control": "text"
    }
    return formats.get(field_name, "text")