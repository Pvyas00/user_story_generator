import os
import json
from groq import Groq
from field_questions import REQUIRED_FIELDS
from brd_field_questions import BRD_REQUIRED_FIELDS
from frd_field_questions import FRD_REQUIRED_FIELDS
from cr_field_questions import CR_REQUIRED_FIELDS
from srd_field_questions import SRD_REQUIRED_FIELDS
from constants import DEFAULT_COVERAGE_ANALYSIS, DEFAULT_STORY_DATA

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.debug_mode = os.getenv('FLASK_ENV') == 'development'
        
        if self.debug_mode:
            print(f"DEBUG - API Key configured: {bool(self.api_key)}")
        
        if not self.api_key:
            if self.debug_mode:
                print("ERROR - GROQ_API_KEY not found in environment")
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        try:
            self.client = Groq(api_key=self.api_key)
            if self.debug_mode:
                print("DEBUG - Groq client initialized successfully")
        except Exception as e:
            if self.debug_mode:
                print(f"ERROR - Groq client initialization failed: {str(e)}")
            raise
        
        self.model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.temperature = float(os.getenv('GROQ_TEMPERATURE', '0.3'))
        self.max_tokens = int(os.getenv('GROQ_MAX_TOKENS', '3000'))
        
        if self.debug_mode:
            print(f"DEBUG - Model: {self.model}, Temp: {self.temperature}, Tokens: {self.max_tokens}")
    
    def _load_prompt(self, prompt_file):
        """Load prompt from file"""
        try:
            with open(f'prompts/{prompt_file}', 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    
    def _make_request(self, messages):
        """Make request to Groq API"""
        try:
            if self.debug_mode:
                print(f"DEBUG - Making API call with model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            
            if self.debug_mode:
                print(f"DEBUG - API Response received: {len(content)} characters")
            return content
        except Exception as e:
            if self.debug_mode:
                print(f"DEBUG - API Error: {str(e)}")
                print(f"DEBUG - Error Type: {type(e).__name__}")
            return None
    
    def analyze_requirement(self, requirement):
        """Analyze requirement and generate questions for missing fields"""
        prompt_template = self._load_prompt('analyze_requirement.txt')
        if not prompt_template:
            prompt_template = """You are a business analyst. Analyze the given requirement and determine which fields are present and which are missing.

Required fields: {fields}

Requirement: {requirement}

For each missing field, generate EXACTLY ONE question with:
- field: field name
- question: clear question to ask user
- recommended_answer: AI-suggested answer
- expected_answer_format: text/yes_no/list/number

Return ONLY valid JSON in this format:
{{
  "present_fields": [],
  "missing_questions": [
    {{
      "field": "",
      "question": "",
      "recommended_answer": "",
      "expected_answer_format": ""
    }}
  ]
}}"""
        
        prompt = prompt_template.format(
            fields=', '.join(REQUIRED_FIELDS),
            requirement=requirement
        )
        
        messages = [
            {"role": "system", "content": "You are a business analyst that returns only valid JSON responses."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._make_request(messages)
        if not response:
            return None
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return None
    
    def analyze_requirement_coverage(self, requirement):
        """Analyze requirement coverage against 10 enterprise elements"""
        try:
            prompt_template = self._load_prompt('analyze_requirement.txt')
            if not prompt_template:
                return DEFAULT_COVERAGE_ANALYSIS
            
            prompt = prompt_template.format(requirement=requirement)
            
            messages = [
                {"role": "system", "content": "You are an expert business analyst that analyzes requirements and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return DEFAULT_COVERAGE_ANALYSIS
            
            try:
                parsed_response = json.loads(response)
                print(f"DEBUG - Parsed successfully: {list(parsed_response.keys())}")
                return parsed_response
            except json.JSONDecodeError as e:
                if self.debug_mode:
                    print(f"DEBUG - JSON Parse failed: {str(e)}")
                    print(f"DEBUG - Raw response: {response[:500]}")
                return DEFAULT_COVERAGE_ANALYSIS
                
        except Exception:
            return DEFAULT_COVERAGE_ANALYSIS
    
    def generate_story(self, requirement, answers, coverage_analysis=None):
        """Generate complete user story from requirement and answers"""
        try:
            prompt_template = self._load_prompt('generate_story.txt')
            if not prompt_template:
                return DEFAULT_STORY_DATA
            
            answers_text = json.dumps(answers, indent=2) if answers else "None provided"
            coverage_text = json.dumps(coverage_analysis, indent=2) if coverage_analysis else "None provided"
            
            prompt = prompt_template.format(
                requirement=requirement,
                answers=answers_text,
                coverage_analysis=coverage_text
            )
            
            messages = [
                {"role": "system", "content": "You are a senior business analyst that creates detailed enterprise-grade user stories and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return DEFAULT_STORY_DATA
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return DEFAULT_STORY_DATA
                
        except Exception:
            return DEFAULT_STORY_DATA
    
    def analyze_brd_requirement_coverage(self, requirement):
        """Analyze requirement coverage against 15 BRD elements"""
        try:
            prompt_template = self._load_prompt('analyze_brd_requirement.txt')
            if not prompt_template:
                return self._get_default_brd_coverage_analysis()
            
            prompt = prompt_template.format(requirement=requirement)
            
            messages = [
                {"role": "system", "content": "You are an expert business analyst that analyzes business requirements and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_brd_coverage_analysis()
            
            try:
                parsed_response = json.loads(response)
                if self.debug_mode:
                    print(f"DEBUG - BRD Analysis parsed successfully: {list(parsed_response.keys())}")
                return parsed_response
            except json.JSONDecodeError as e:
                if self.debug_mode:
                    print(f"DEBUG - BRD JSON Parse failed: {str(e)}")
                    print(f"DEBUG - Raw response: {response[:500]}")
                return self._get_default_brd_coverage_analysis()
                
        except Exception:
            return self._get_default_brd_coverage_analysis()
    
    def generate_brd(self, requirement, answers, coverage_analysis=None):
        """Generate complete BRD from requirement and answers"""
        try:
            prompt_template = self._load_prompt('generate_brd.txt')
            if not prompt_template:
                return self._get_default_brd_data()
            
            answers_text = json.dumps(answers, indent=2) if answers else "None provided"
            coverage_text = json.dumps(coverage_analysis, indent=2) if coverage_analysis else "None provided"
            
            prompt = prompt_template.format(
                requirement=requirement,
                answers=answers_text,
                coverage_analysis=coverage_text
            )
            
            messages = [
                {"role": "system", "content": "You are a senior business analyst that creates detailed enterprise-grade Business Requirements Documents and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_brd_data()
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._get_default_brd_data()
                
        except Exception:
            return self._get_default_brd_data()
    
    def analyze_frd_requirement_coverage(self, requirement):
        """Analyze requirement coverage against 14 FRD elements"""
        try:
            prompt_template = self._load_prompt('analyze_frd_requirement.txt')
            if not prompt_template:
                return self._get_default_frd_coverage_analysis()
            
            prompt = prompt_template.format(requirement=requirement)
            
            messages = [
                {"role": "system", "content": "You are an expert technical analyst that analyzes functional requirements and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_frd_coverage_analysis()
            
            try:
                parsed_response = json.loads(response)
                if self.debug_mode:
                    print(f"DEBUG - FRD Analysis parsed successfully: {list(parsed_response.keys())}")
                return parsed_response
            except json.JSONDecodeError as e:
                if self.debug_mode:
                    print(f"DEBUG - FRD JSON Parse failed: {str(e)}")
                    print(f"DEBUG - Raw response: {response[:500]}")
                return self._get_default_frd_coverage_analysis()
                
        except Exception:
            return self._get_default_frd_coverage_analysis()
    
    def generate_frd(self, requirement, answers, coverage_analysis=None):
        """Generate complete FRD from requirement and answers"""
        try:
            prompt_template = self._load_prompt('generate_frd.txt')
            if not prompt_template:
                return self._get_default_frd_data()
            
            answers_text = json.dumps(answers, indent=2) if answers else "None provided"
            coverage_text = json.dumps(coverage_analysis, indent=2) if coverage_analysis else "None provided"
            
            prompt = prompt_template.format(
                requirement=requirement,
                answers=answers_text,
                coverage_analysis=coverage_text
            )
            
            messages = [
                {"role": "system", "content": "You are a senior technical analyst that creates detailed enterprise-grade Functional Requirements Documents and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_frd_data()
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._get_default_frd_data()
                
        except Exception:
            return self._get_default_frd_data()
    
    def analyze_srd_requirement_coverage(self, requirement):
        """Analyze requirement coverage against 12 SRD elements"""
        try:
            prompt_template = self._load_prompt('analyze_srd_requirement.txt')
            if not prompt_template:
                return self._get_default_srd_coverage_analysis()
            
            prompt = prompt_template.format(requirement=requirement)
            
            messages = [
                {"role": "system", "content": "You are an expert system architect that analyzes system requirements and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_srd_coverage_analysis()
            
            try:
                parsed_response = json.loads(response)
                if self.debug_mode:
                    print(f"DEBUG - SRD Analysis parsed successfully: {list(parsed_response.keys())}")
                return parsed_response
            except json.JSONDecodeError as e:
                if self.debug_mode:
                    print(f"DEBUG - SRD JSON Parse failed: {str(e)}")
                    print(f"DEBUG - Raw response: {response[:500]}")
                return self._get_default_srd_coverage_analysis()
                
        except Exception:
            return self._get_default_srd_coverage_analysis()
    
    def generate_srd(self, requirement, answers, coverage_analysis=None):
        """Generate complete SRD from requirement and answers"""
        try:
            prompt_template = self._load_prompt('generate_srd.txt')
            if not prompt_template:
                return self._get_default_srd_data()
            
            answers_text = json.dumps(answers, indent=2) if answers else "None provided"
            coverage_text = json.dumps(coverage_analysis, indent=2) if coverage_analysis else "None provided"
            
            prompt = prompt_template.format(
                requirement=requirement,
                answers=answers_text,
                coverage_analysis=coverage_text
            )
            
            messages = [
                {"role": "system", "content": "You are a senior system architect that creates detailed enterprise-grade System Requirements Documents and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_srd_data()
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._get_default_srd_data()
                
        except Exception:
            return self._get_default_srd_data()
    
    def analyze_cr_requirement_coverage(self, requirement):
        """Analyze requirement coverage against 15 CR elements"""
        try:
            prompt_template = self._load_prompt('analyze_cr_requirement.txt')
            if not prompt_template:
                return self._get_default_cr_coverage_analysis()
            
            prompt = prompt_template.format(requirement=requirement)
            
            messages = [
                {"role": "system", "content": "You are an expert change management analyst that analyzes change requests and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_cr_coverage_analysis()
            
            try:
                parsed_response = json.loads(response)
                if self.debug_mode:
                    print(f"DEBUG - CR Analysis parsed successfully: {list(parsed_response.keys())}")
                return parsed_response
            except json.JSONDecodeError as e:
                if self.debug_mode:
                    print(f"DEBUG - CR JSON Parse failed: {str(e)}")
                    print(f"DEBUG - Raw response: {response[:500]}")
                return self._get_default_cr_coverage_analysis()
                
        except Exception:
            return self._get_default_cr_coverage_analysis()
    
    def generate_cr(self, requirement, answers, coverage_analysis=None):
        """Generate complete CR from requirement and answers"""
        try:
            prompt_template = self._load_prompt('generate_cr.txt')
            if not prompt_template:
                return self._get_default_cr_data()
            
            answers_text = json.dumps(answers, indent=2) if answers else "None provided"
            coverage_text = json.dumps(coverage_analysis, indent=2) if coverage_analysis else "None provided"
            
            prompt = prompt_template.format(
                requirement=requirement,
                answers=answers_text,
                coverage_analysis=coverage_text
            )
            
            messages = [
                {"role": "system", "content": "You are a senior change management specialist that creates detailed enterprise-grade Change Request documents and returns only valid JSON responses."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._make_request(messages)
            if not response:
                return self._get_default_cr_data()
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._get_default_cr_data()
                
        except Exception:
            return self._get_default_cr_data()
    
    def _get_default_brd_coverage_analysis(self):
        """Get default BRD coverage analysis"""
        return {
            "coverage_analysis": {
                "present_elements": [],
                "missing_elements": [
                    {"element": field, "status": "missing", "details": f"No {field.lower()} information provided", "editable": True}
                    for field in BRD_REQUIRED_FIELDS
                ]
            },
            "overall_score": 0,
            "enterprise_readiness": "Needs Significant Enhancement",
            "critical_gaps": BRD_REQUIRED_FIELDS,
            "editable_recommendations": [
                {"element": field, "question": f"Please provide {field.lower()} details", "suggested_answer": "To be determined", "field_type": "textarea"}
                for field in BRD_REQUIRED_FIELDS
            ],
            "requirement_category": "Business Process",
            "project_name": "Business Requirements Project"
        }
    
    def _get_default_brd_data(self):
        """Get default BRD data structure"""
        return {
            "project_name": "Business Requirements Project",
            "executive_summary": {
                "background": "Project background to be defined",
                "problem_statement": "Problem statement to be defined",
                "business_need": "Business need to be defined",
                "solution": "Solution approach to be defined",
                "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"]
            },
            "business_objectives": [
                {"objective": "Objective 1", "kpi": "KPI 1"},
                {"objective": "Objective 2", "kpi": "KPI 2"}
            ],
            "scope": {
                "in_scope": ["Feature 1", "Feature 2"],
                "out_of_scope": ["Feature A", "Feature B"]
            },
            "stakeholders": [
                {"name": "Business Owner", "role": "Owner", "department": "Business", "responsibilities": "Decision making"}
            ],
            "current_state": {
                "description": "Current state description",
                "pain_points": ["Pain point 1", "Pain point 2"]
            },
            "future_state": {
                "description": "Future state description",
                "improvements": ["Improvement 1", "Improvement 2"]
            },
            "business_requirements": [
                {"br_id": "BR-001", "title": "Requirement 1", "description": "Description", "priority": "High", "source": "Business", "acceptance_criteria": "Criteria"}
            ],
            "business_rules": [
                {"rule_id": "BR-001", "description": "IF condition THEN action"}
            ],
            "assumptions": ["Assumption 1", "Assumption 2"],
            "dependencies": ["Dependency 1", "Dependency 2"],
            "risks": [
                {"risk_id": "R-001", "description": "Risk description", "impact": "Medium", "likelihood": "Low", "mitigation": "Mitigation strategy"}
            ],
            "glossary": [
                {"term": "Term 1", "definition": "Definition 1"}
            ]
        }
    
    def _get_default_frd_coverage_analysis(self):
        """Get default FRD coverage analysis"""
        return {
            "coverage_analysis": {
                "present_elements": [],
                "missing_elements": [
                    {"element": field, "status": "missing", "details": f"No {field.lower()} information provided", "editable": True}
                    for field in FRD_REQUIRED_FIELDS
                ]
            },
            "overall_score": 0,
            "enterprise_readiness": "Needs Significant Enhancement",
            "critical_gaps": FRD_REQUIRED_FIELDS,
            "editable_recommendations": [
                {"element": field, "question": f"Please provide {field.lower()} details", "suggested_answer": "To be determined", "field_type": "textarea"}
                for field in FRD_REQUIRED_FIELDS
            ],
            "requirement_category": "Technical Requirements",
            "system_complexity": "Medium"
        }
    
    def _get_default_frd_data(self):
        """Get default FRD data structure"""
        return {
            "system_overview": {
                "architecture": "System architecture to be defined",
                "components": ["Component 1", "Component 2"],
                "technology_stack": ["Technology 1", "Technology 2"],
                "design_principles": ["Principle 1", "Principle 2"]
            },
            "functional_requirements": [
                {"req_id": "FR-001", "title": "Functional Requirement 1", "description": "Description", "priority": "High", "acceptance_criteria": "Criteria"}
            ],
            "data_requirements": {
                "data_models": ["Model 1", "Model 2"],
                "storage_requirements": "Storage requirements to be defined",
                "data_flow": "Data flow to be defined",
                "data_integrity": "Data integrity requirements"
            },
            "interface_requirements": {
                "ui_specifications": "UI specifications to be defined",
                "api_specifications": "API specifications to be defined",
                "integration_interfaces": "Integration interfaces to be defined"
            },
            "integration_requirements": [
                {"system": "External System 1", "method": "REST API", "data_format": "JSON", "frequency": "Real-time"}
            ],
            "performance_requirements": {
                "response_time": "< 2 seconds",
                "throughput": "1000 requests/minute",
                "scalability": "Auto-scaling requirements",
                "availability": "99.9% uptime"
            },
            "security_requirements": [
                "Authentication and authorization",
                "Data encryption requirements"
            ],
            "validation_rules": [
                {"field": "Field 1", "rule": "Validation rule", "error_message": "Error message"}
            ],
            "error_handling": [
                {"error_type": "System Error", "handling_strategy": "Strategy", "user_message": "Message", "logging": "Logging requirements"}
            ],
            "reporting_requirements": [
                {"report_name": "Report 1", "description": "Description", "frequency": "Daily", "format": "Dashboard"}
            ],
            "testing_requirements": {
                "unit_testing": "Unit testing requirements",
                "integration_testing": "Integration testing requirements",
                "performance_testing": "Performance testing criteria",
                "security_testing": "Security testing requirements"
            },
            "deployment_requirements": {
                "environment": "Production environment specs",
                "deployment_strategy": "Deployment approach",
                "rollback_plan": "Rollback strategy",
                "infrastructure": "Infrastructure requirements"
            },
            "maintenance_requirements": {
                "monitoring": "System monitoring requirements",
                "backup_strategy": "Backup procedures",
                "update_procedures": "Update processes",
                "support_procedures": "Support procedures"
            },
            "technical_specifications": [
                {"component": "Component 1", "specification": "Technical specifications"}
            ]
        }
    
    def _get_default_srd_coverage_analysis(self):
        """Get default SRD coverage analysis"""
        return {
            "coverage_analysis": {
                "present_elements": [],
                "missing_elements": [
                    {"element": field, "status": "missing", "details": f"No {field.lower()} information provided", "editable": True}
                    for field in SRD_REQUIRED_FIELDS
                ]
            },
            "overall_score": 0,
            "enterprise_readiness": "Needs Significant Enhancement",
            "critical_gaps": SRD_REQUIRED_FIELDS,
            "editable_recommendations": [
                {"element": field, "question": f"Please provide {field.lower()} details", "suggested_answer": "To be determined", "field_type": "textarea"}
                for field in SRD_REQUIRED_FIELDS
            ],
            "requirement_category": "System Requirements",
            "system_complexity": "Medium"
        }
    
    def _get_default_srd_data(self):
        """Get default SRD data structure"""
        return {
            "system_architecture": {
                "overview": "System architecture to be defined",
                "components": ["Component 1", "Component 2"],
                "deployment_model": "Cloud deployment model",
                "architecture_patterns": ["Pattern 1", "Pattern 2"]
            },
            "hardware_requirements": {
                "servers": "Server specifications to be defined",
                "storage": "Storage requirements to be defined",
                "network_hardware": "Network hardware requirements",
                "backup_hardware": "Backup hardware specifications"
            },
            "software_requirements": {
                "operating_system": "OS requirements to be defined",
                "middleware": ["Middleware 1", "Middleware 2"],
                "runtime_environments": ["Runtime 1", "Runtime 2"],
                "third_party_software": ["Software 1", "Software 2"]
            },
            "network_requirements": {
                "bandwidth": "Network bandwidth requirements",
                "connectivity": "Network connectivity specifications",
                "protocols": ["Protocol 1", "Protocol 2"],
                "security": "Network security requirements"
            },
            "database_requirements": {
                "database_type": "Database system to be defined",
                "storage_capacity": "Database storage requirements",
                "performance": "Database performance specifications",
                "replication": "Database replication requirements"
            },
            "system_interfaces": [
                {"interface": "Interface 1", "type": "REST API", "protocol": "HTTPS", "data_format": "JSON"}
            ],
            "performance_specifications": {
                "response_time": "< 2 seconds",
                "throughput": "1000 requests/minute",
                "concurrent_users": "500 users",
                "availability": "99.9% uptime"
            },
            "security_architecture": {
                "authentication": "Authentication mechanisms",
                "authorization": "Access control requirements",
                "encryption": "Data encryption requirements",
                "network_security": "Network security measures"
            },
            "backup_recovery": {
                "backup_strategy": "Backup procedures to be defined",
                "recovery_procedures": "Recovery procedures",
                "disaster_recovery": "Disaster recovery planning",
                "data_retention": "Data retention policies"
            },
            "monitoring_logging": {
                "system_monitoring": "System monitoring requirements",
                "performance_monitoring": "Performance monitoring",
                "log_management": "Log management procedures",
                "reporting": "System reporting requirements"
            },
            "scalability_requirements": {
                "horizontal_scaling": "Horizontal scaling capabilities",
                "vertical_scaling": "Vertical scaling specifications",
                "load_balancing": "Load balancing requirements",
                "capacity_planning": "Capacity planning procedures"
            },
            "compliance_standards": [
                {"standard": "ISO 27001", "description": "Information security compliance"}
            ]
        }
    
    def _get_default_cr_coverage_analysis(self):
        """Get default CR coverage analysis"""
        return {
            "coverage_analysis": {
                "present_elements": [],
                "missing_elements": [
                    {"element": field, "status": "missing", "details": f"No {field.lower()} information provided", "editable": True}
                    for field in CR_REQUIRED_FIELDS
                ]
            },
            "overall_score": 0,
            "enterprise_readiness": "Needs Significant Enhancement",
            "critical_gaps": CR_REQUIRED_FIELDS,
            "editable_recommendations": [
                {"element": field, "question": f"Please provide {field.lower()} details", "suggested_answer": "To be determined", "field_type": "textarea"}
                for field in CR_REQUIRED_FIELDS
            ],
            "requirement_category": "Change Management",
            "change_complexity": "Medium"
        }
    
    def _get_default_cr_data(self):
        """Get default CR data structure"""
        return {
            "change_request_id": "CR-2024-001: Change Request Title",
            "business_justification": "Business justification to be defined",
            "requestor_information": "Requestor information to be provided",
            "impact_analysis": "Impact analysis to be conducted",
            "current_state": "Current state description to be provided",
            "proposed_changes": "Proposed changes to be detailed",
            "risk_assessment": [
                {"risk_id": "RISK-001", "description": "Risk description", "probability": "Medium", "impact": "Medium", "mitigation": "Mitigation strategy"}
            ],
            "cost_benefit_analysis": {
                "implementation_costs": "Implementation costs to be estimated",
                "operational_costs": "Operational cost changes to be analyzed",
                "expected_benefits": "Expected benefits to be quantified",
                "roi_analysis": "ROI calculation to be performed"
            },
            "implementation_timeline": [
                {"phase": "Phase 1: Analysis", "duration": "2 weeks", "deliverables": "Analysis deliverables", "dependencies": "Dependencies"}
            ],
            "stakeholder_impact": [
                {"stakeholder_group": "End Users", "impact_level": "Medium", "impact_description": "Impact description", "mitigation_actions": "Mitigation actions"}
            ],
            "testing_requirements": {
                "testing_strategy": "Testing strategy to be defined",
                "test_types": ["Unit Testing", "Integration Testing", "User Acceptance Testing"],
                "acceptance_criteria": "Acceptance criteria to be defined",
                "testing_timeline": "Testing timeline to be established"
            },
            "approval_workflow": [
                {"step": 1, "approver_role": "IT Manager", "approver_name": "TBD", "approval_criteria": "Technical approval"}
            ],
            "rollback_plan": {
                "rollback_triggers": "Rollback triggers to be defined",
                "rollback_steps": ["Step 1: Stop services", "Step 2: Restore backup", "Step 3: Verify system"],
                "data_recovery": "Data recovery procedures to be defined",
                "communication": "Rollback communication plan"
            },
            "success_metrics": [
                {"metric_name": "System Performance", "measurement_method": "Performance monitoring", "target_value": "< 2 seconds response time", "monitoring_frequency": "Continuous"}
            ],
            "supporting_documents": [
                "Technical Specification Document",
                "System Architecture Diagram",
                "Risk Assessment Report"
            ]
        }