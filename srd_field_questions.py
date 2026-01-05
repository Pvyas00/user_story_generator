SRD_REQUIRED_FIELDS = [
    "System Architecture",
    "Hardware Requirements",
    "Software Requirements", 
    "Network Requirements",
    "Database Requirements",
    "System Interfaces",
    "Performance Specifications",
    "Security Architecture",
    "Backup & Recovery",
    "Monitoring & Logging",
    "Scalability Requirements",
    "Compliance & Standards"
]

SRD_FIELD_DESCRIPTIONS = {
    "System Architecture": "What is the overall system architecture and design?",
    "Hardware Requirements": "What hardware specifications and infrastructure are needed?",
    "Software Requirements": "What software components, OS, and dependencies are required?",
    "Network Requirements": "What network infrastructure and connectivity requirements are needed?",
    "Database Requirements": "What database systems and storage requirements are needed?",
    "System Interfaces": "What external system connections and interfaces are required?",
    "Performance Specifications": "What system performance and capacity planning requirements are needed?",
    "Security Architecture": "What system-level security design and protocols are required?",
    "Backup & Recovery": "What data backup and disaster recovery procedures are needed?",
    "Monitoring & Logging": "What system monitoring and logging requirements are needed?",
    "Scalability Requirements": "What system scaling and growth planning requirements are needed?",
    "Compliance & Standards": "What regulatory and industry standards compliance is required?"
}

def get_srd_field_question(field_name):
    """Get the standard question for an SRD field"""
    return SRD_FIELD_DESCRIPTIONS.get(field_name, f"Please provide details about {field_name}")

def get_srd_recommended_answer(field_name, requirement_context=""):
    """Get AI-recommended answer based on SRD field and context"""
    recommendations = {
        "System Architecture": "High-level system architecture with components and deployment model",
        "Hardware Requirements": "Server specifications, storage capacity, and infrastructure requirements",
        "Software Requirements": "Operating system, middleware, runtime environments, and software dependencies",
        "Network Requirements": "Network bandwidth, connectivity, protocols, and security requirements",
        "Database Requirements": "Database system type, storage capacity, performance, and replication",
        "System Interfaces": "External system connections, APIs, protocols, and data formats",
        "Performance Specifications": "Response time, throughput, concurrent users, and availability requirements",
        "Security Architecture": "Authentication, authorization, encryption, and network security measures",
        "Backup & Recovery": "Backup procedures, recovery strategies, and disaster recovery planning",
        "Monitoring & Logging": "System monitoring, performance monitoring, log management, and reporting",
        "Scalability Requirements": "Horizontal scaling, vertical scaling, load balancing, and capacity planning",
        "Compliance & Standards": "Regulatory compliance requirements and industry standards adherence"
    }
    return recommendations.get(field_name, "To be determined based on system requirements")

def get_srd_expected_format(field_name):
    """Get expected answer format for an SRD field"""
    formats = {
        "System Architecture": "object",
        "Hardware Requirements": "object",
        "Software Requirements": "object",
        "Network Requirements": "object",
        "Database Requirements": "object",
        "System Interfaces": "list",
        "Performance Specifications": "object",
        "Security Architecture": "object",
        "Backup & Recovery": "object",
        "Monitoring & Logging": "object",
        "Scalability Requirements": "object",
        "Compliance & Standards": "list"
    }
    return formats.get(field_name, "text")