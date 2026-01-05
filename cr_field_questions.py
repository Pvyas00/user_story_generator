"""
CR (Change Request) Field Questions and Definitions
Comprehensive change management documentation with 15 essential sections
"""

CR_REQUIRED_FIELDS = [
    'change_request_id',
    'business_justification', 
    'requestor_information',
    'impact_analysis',
    'current_state',
    'proposed_changes',
    'risk_assessment',
    'cost_benefit_analysis',
    'implementation_timeline',
    'stakeholder_impact',
    'testing_requirements',
    'approval_workflow',
    'rollback_plan',
    'success_metrics',
    'supporting_documents'
]

CR_FIELD_QUESTIONS = {
    'change_request_id': {
        'question': 'What is the unique identifier and title for this change request?',
        'description': 'Provide a unique CR ID and descriptive title for tracking purposes',
        'example': 'CR-2024-001: User Authentication System Enhancement'
    },
    
    'business_justification': {
        'question': 'What is the business justification for this change?',
        'description': 'Explain why this change is necessary and how it aligns with business objectives',
        'example': 'Improve user security and reduce support tickets by 30%'
    },
    
    'requestor_information': {
        'question': 'Who is requesting this change and what are their contact details?',
        'description': 'Provide requestor name, department, role, and contact information',
        'example': 'John Smith, IT Security Manager, john.smith@company.com'
    },
    
    'impact_analysis': {
        'question': 'What is the detailed impact analysis of this change?',
        'description': 'Analyze impact on systems, processes, users, and business operations',
        'example': 'High impact on user login process, medium impact on database performance'
    },
    
    'current_state': {
        'question': 'What is the current state of the system/process being changed?',
        'description': 'Describe the existing system, process, or functionality in detail',
        'example': 'Current system uses basic username/password authentication'
    },
    
    'proposed_changes': {
        'question': 'What are the specific changes being proposed?',
        'description': 'Detail the exact modifications, additions, or removals being requested',
        'example': 'Implement multi-factor authentication with SMS and email verification'
    },
    
    'risk_assessment': {
        'question': 'What are the risks associated with this change and their mitigation strategies?',
        'description': 'Identify potential risks, their probability, impact, and mitigation plans',
        'example': 'Risk: User adoption issues. Mitigation: Comprehensive training program'
    },
    
    'cost_benefit_analysis': {
        'question': 'What is the cost-benefit analysis for this change?',
        'description': 'Provide detailed cost estimates and expected benefits/ROI',
        'example': 'Implementation cost: $50K, Expected savings: $200K annually'
    },
    
    'implementation_timeline': {
        'question': 'What is the proposed implementation timeline and key milestones?',
        'description': 'Provide detailed project timeline with phases, milestones, and dependencies',
        'example': 'Phase 1: Analysis (2 weeks), Phase 2: Development (6 weeks), Phase 3: Testing (2 weeks)'
    },
    
    'stakeholder_impact': {
        'question': 'How will this change impact different stakeholders?',
        'description': 'Analyze impact on end users, IT teams, management, and external parties',
        'example': 'End users: Additional login step, IT team: New system to maintain'
    },
    
    'testing_requirements': {
        'question': 'What are the testing requirements and acceptance criteria?',
        'description': 'Define testing strategy, test cases, and success criteria',
        'example': 'Unit testing, integration testing, user acceptance testing, security testing'
    },
    
    'approval_workflow': {
        'question': 'What is the approval workflow and who are the approvers?',
        'description': 'Define the approval process, required approvers, and escalation path',
        'example': 'IT Manager → Security Officer → CTO → Final Approval'
    },
    
    'rollback_plan': {
        'question': 'What is the rollback plan if the change needs to be reversed?',
        'description': 'Provide detailed steps to revert changes if issues occur',
        'example': 'Database backup restoration, configuration rollback, user notification'
    },
    
    'success_metrics': {
        'question': 'How will the success of this change be measured?',
        'description': 'Define KPIs, metrics, and success criteria to evaluate change effectiveness',
        'example': 'Reduce security incidents by 50%, improve user satisfaction score to 4.5/5'
    },
    
    'supporting_documents': {
        'question': 'What supporting documents and references are available?',
        'description': 'List any technical specifications, diagrams, or reference materials',
        'example': 'System architecture diagram, security policy document, vendor specifications'
    }
}

def get_cr_field_question(field_name):
    """Get question details for a specific CR field"""
    return CR_FIELD_QUESTIONS.get(field_name, {
        'question': f'Please provide details for {field_name.replace("_", " ").title()}',
        'description': f'Describe the {field_name.replace("_", " ")} requirements',
        'example': 'Please provide relevant information'
    })

def get_all_cr_questions():
    """Get all CR field questions"""
    return CR_FIELD_QUESTIONS

def get_cr_required_fields():
    """Get list of required CR fields"""
    return CR_REQUIRED_FIELDS