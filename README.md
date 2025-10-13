# QR Code Generator - AI-Powered CI/CD Demo

This project demonstrates **AI-assisted DevOps automation** with a complete CI/CD pipeline that automatically analyzes code and generates infrastructure.

## 🎯 Project Overview

**QR Code Generator** is a full-stack web application that generates QR codes from various data types:
- Plain text
- URLs
- Email addresses  
- Phone numbers
- WiFi credentials

### Architecture

- **Frontend**: node (8000 port)
- **Backend**: fastapi (8000 port)
- **Infrastructure**: AWS EC2 with Terraform
- **Deployment**: Docker Compose
- **CI/CD**: GitHub Actions with AI-generated workflows

## 🚀 Quick Start

### Prerequisites

- AWS Account with CLI configured
- Docker and Docker Compose
- Terraform >= 1.5.0
- Python 3.11+
- Git

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AISDLC2.0
   ```

2. **Run locally with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### AWS Deployment

1. **Configure AWS credentials**:
   ```bash
   aws configure
   ```

2. **Set up Terraform variables**:
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your preferences
   ```

3. **Deploy to AWS**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Get deployment URLs**:
   ```bash
   terraform output application_urls
   ```

## 🤖 AI Pipeline Generator

The `generate_workflow.py` script automatically:

### Code Analysis
- Detects programming languages and frameworks
- Identifies dependencies and test commands
- Analyzes port configurations
- Suggests optimal CI/CD strategies

### Infrastructure Generation
- Creates Terraform configurations for AWS EC2
- Generates Docker and Docker Compose files
- Sets up security groups and networking
- Configures auto-scaling and monitoring

### Pipeline Automation  
- Generates GitHub Actions workflows
- Sets up automated testing and linting
- Configures deployment strategies
- Implements rollback mechanisms

### Usage

```bash
# Run the AI generator
python generate_workflow.py

# Run with auto-commit (for CI/CD)
python generate_workflow.py --auto-commit

# Analyze only (no file generation)
python generate_workflow.py --analyze-only
```

## 📁 Project Structure

```
.
├── README.md                          # This file
├── VERSION                            # Version tracking
├── pipeline_request.txt              # AI pipeline configuration
├── generate_workflow.py              # AI pipeline generator
├── docker-compose.yml               # Local development setup
├── frontend/                        # Frontend application
│   ├── index.html                  # Main HTML file
│   ├── script.js                   # JavaScript logic
│   ├── style.css                   # Styling
│   ├── Dockerfile                  # Frontend container
│   └── nginx.conf                  # Nginx configuration
├── backend/                         # Backend API
│   ├── main.py                     # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend container
│   └── api/                        # API modules
├── terraform/                       # Infrastructure as Code
│   ├── main.tf                     # Main Terraform configuration
│   ├── variables.tf                # Variable definitions
│   ├── user_data.sh               # EC2 initialization script
│   └── terraform.tfvars.example   # Example configuration
└── .github/workflows/              # CI/CD pipelines
    ├── ci-cd.yml                   # Main deployment workflow
    └── ai-generate-workflow.yml    # AI generator trigger
```

## 🔄 CI/CD Workflow

The AI-generated pipeline includes:

### 1. **Validation Stage**
- YAML syntax validation
- Terraform formatting and validation  
- Code linting and security scanning

### 2. **Testing Stage**
- Backend API testing with pytest
- Frontend testing (if configured)
- Integration testing
- Security vulnerability scanning

### 3. **Deployment Stage**
- Terraform infrastructure provisioning
- Docker image building and pushing
- AWS EC2 deployment via user data script
- Health checks and monitoring setup

### 4. **Notification Stage**
- Email notifications on success/failure
- Slack/Teams integration (configurable)
- Deployment status reporting

## ⚙️ Configuration

### Pipeline Configuration (`pipeline_request.txt`)

```yaml
pipeline_name: qr-generator-auto-pipeline
environment: production
target: aws_ec2
instance_type: t2.micro
deploy_using: docker-compose
labels: [ai-generated, demo]
email_notification: true
email_recipient: your-email@example.com
```

### GitHub Secrets Required

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `EMAIL_USERNAME`: SMTP username (optional)
- `EMAIL_PASSWORD`: SMTP password (optional)

## 🛡️ Security Features

- EC2 security groups with minimal required ports
- Encrypted EBS volumes
- IAM roles with least privilege
- Container security scanning
- Secrets management via GitHub Secrets

## 📊 Monitoring & Logging

- CloudWatch monitoring for EC2 instances
- Application health checks
- Docker container logs
- Terraform state management
- Automated backup and recovery

## 🧹 Cleanup

To destroy the AWS infrastructure:

```bash
cd terraform
terraform destroy
```

To stop local development:

```bash
docker-compose down -v
```

## 🔧 Troubleshooting

### Common Issues

1. **AWS Permissions**: Ensure your AWS user has EC2, VPC, and IAM permissions
2. **Terraform State**: Use remote state storage for team collaboration
3. **Docker Build**: Check Dockerfile syntax and dependency availability
4. **Port Conflicts**: Ensure ports 3000, 8000, 80 are available

### Debug Commands

```bash
# Check application logs
docker-compose logs -f

# SSH into EC2 instance
ssh -i qr-generator-private-key.pem ubuntu@<instance-ip>

# Check Terraform state
terraform show

# Validate Terraform configuration
terraform validate
```

## 🤝 Contributing

This is a demo project showcasing AI-assisted DevOps. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **Terraform**: Infrastructure as Code
- **GitHub Actions**: CI/CD automation
- **AWS**: Cloud infrastructure
- **Docker**: Containerization platform

---

**Generated by**: AI-Powered Pipeline Generator v1.0
**Last Updated**: 2025-10-08 17:46:11
**Project Version**: 0.1.28

# AI-Powered CI/CD Architecture Diagram

## 🏗️ System Architecture Overview

```mermaid
graph TB
    %% Developer Workflow
    DEV[👨‍💻 Developer] --> GIT[📚 Git Repository]
    
    %% AI Pipeline Generator
    subgraph "🤖 AI Pipeline Generation"
        PIPELINE[generate_workflow.py]
        OPENAI[🧠 OpenAI API]
        CONFIG[📋 pipeline_request.txt]
        
        PIPELINE --> OPENAI
        CONFIG --> PIPELINE
    end
    
    %% Code Analysis
    subgraph "🔍 Code Analysis Engine"
        ANALYZER[CodeAnalyzer]
        FRONTEND_SCAN[Frontend Scanner]
        BACKEND_SCAN[Backend Scanner]
        INFRA_SCAN[Infrastructure Scanner]
        DOCKER_SCAN[Docker Scanner]
        
        ANALYZER --> FRONTEND_SCAN
        ANALYZER --> BACKEND_SCAN
        ANALYZER --> INFRA_SCAN
        ANALYZER --> DOCKER_SCAN
    end
    
    %% Generated Components
    subgraph "📁 Generated DevOps Components"
        TERRAFORM[🏗️ Terraform IaC]
        GITHUB_ACTIONS[⚙️ GitHub Actions]
        DOCKER_COMPOSE[🐳 Docker Compose]
        README[📖 Documentation]
    end
    
    %% CI/CD Pipeline
    subgraph "🚀 GitHub Actions Workflow"
        VALIDATE[✅ Validation Job]
        TEST[🧪 Test Job]
        DEPLOY[🚀 Deploy Job]
        NOTIFY[📧 Notification]
        
        VALIDATE --> TEST
        TEST --> DEPLOY
        DEPLOY --> NOTIFY
    end
    
    %% AWS Infrastructure
    subgraph "☁️ AWS Cloud Infrastructure"
        EC2[🖥️ EC2 Instance]
        SG[🛡️ Security Group]
        EIP[🌐 Elastic IP]
        EBS[💾 EBS Volume]
        
        EC2 --> SG
        EC2 --> EIP
        EC2 --> EBS
    end
    
    %% Application Stack
    subgraph "📱 QR Generator Application"
        NGINX[🌐 Nginx Proxy]
        FRONTEND_APP[🎨 Frontend\n(Vanilla JS)]
        BACKEND_APP[🔧 Backend\n(FastAPI)]
        
        NGINX --> FRONTEND_APP
        NGINX --> BACKEND_APP
    end
    
    %% Connections
    GIT --> PIPELINE
    PIPELINE --> ANALYZER
    ANALYZER --> TERRAFORM
    ANALYZER --> GITHUB_ACTIONS
    ANALYZER --> DOCKER_COMPOSE
    ANALYZER --> README
    
    GIT --> GITHUB_ACTIONS
    GITHUB_ACTIONS --> VALIDATE
    TERRAFORM --> EC2
    EC2 --> NGINX
    
    style DEV fill:#e1f5fe
    style PIPELINE fill:#f3e5f5
    style OPENAI fill:#fff3e0
    style EC2 fill:#e8f5e8
    style GITHUB_ACTIONS fill:#fff8e1
```

## 🔄 Detailed Workflow Architecture

```mermaid
sequenceDiagram
    participant Dev as 👨‍💻 Developer
    participant Git as 📚 Git Repository
    participant AI as 🤖 AI Generator
    participant OpenAI as 🧠 OpenAI API
    participant GHA as ⚙️ GitHub Actions
    participant AWS as ☁️ AWS Infrastructure
    participant App as 📱 Application

    Dev->>Git: Push code changes
    Git->>AI: Trigger AI generator
    AI->>AI: Analyze codebase
    AI->>OpenAI: Get AI recommendations
    OpenAI-->>AI: Return intelligent suggestions
    AI->>Git: Generate pipeline components
    
    Git->>GHA: Trigger CI/CD workflow
    GHA->>GHA: Validate code & config
    GHA->>GHA: Run tests
    GHA->>AWS: Deploy infrastructure
    AWS->>AWS: Provision EC2 + networking
    AWS->>App: Deploy application
    App-->>Dev: Application ready
    GHA->>Dev: Send notification
```

## 🎯 Component Architecture Details

### 1. AI Pipeline Generator Core

```mermaid
graph LR
    subgraph "🤖 PipelineGenerator Class"
        INIT[__init__] --> LOAD_CONFIG[_load_config]
        LOAD_CONFIG --> ANALYZER[CodeAnalyzer]
        ANALYZER --> AI_ENHANCE[_ai_enhance_analysis]
        AI_ENHANCE --> GENERATE[generate_pipeline]
        
        GENERATE --> GEN_WORKFLOW[_generate_github_workflow]
        GENERATE --> GEN_TERRAFORM[_ensure_terraform_infrastructure]
        GENERATE --> GEN_DOCKER[_ensure_docker_configuration]
        GENERATE --> UPDATE_README[_update_readme]
        GENERATE --> INCREMENT_VERSION[_increment_version]
    end
    
    style GENERATE fill:#e8f5e8
    style AI_ENHANCE fill:#fff3e0
```

### 2. Code Analysis Engine

```mermaid
graph TB
    subgraph "🔍 CodeAnalyzer"
        PROJECT[analyze_project]
        
        PROJECT --> FRONTEND[_analyze_frontend]
        PROJECT --> BACKEND[_analyze_backend]
        PROJECT --> INFRA[_analyze_infrastructure]
        PROJECT --> DOCKER[_analyze_docker]
        PROJECT --> GIT[_analyze_git]
        
        FRONTEND --> DETECT_FRAMEWORK[Detect Framework]
        FRONTEND --> DETECT_PORT[Detect Ports]
        FRONTEND --> ANALYZE_DEPS[Analyze Dependencies]
        
        BACKEND --> PYTHON_FRAMEWORK[Python Framework Detection]
        BACKEND --> PORT_DETECTION[Port Detection]
        BACKEND --> REQUIREMENTS[Requirements Analysis]
    end
    
    style PROJECT fill:#e1f5fe
```

### 3. Infrastructure Generation

```mermaid
graph TB
    subgraph "🏗️ Terraform Infrastructure"
        MAIN_TF[main.tf]
        VARIABLES_TF[variables.tf]
        OUTPUTS_TF[outputs.tf]
        TFVARS[terraform.tfvars]
        USER_DATA[user_data.sh]
        
        MAIN_TF --> EC2_CONFIG[EC2 Instance Config]
        MAIN_TF --> SECURITY_GROUP[Security Group Rules]
        MAIN_TF --> ELASTIC_IP[Elastic IP Assignment]
        
        VARIABLES_TF --> PORT_CONFIG[Port Configuration]
        VARIABLES_TF --> INSTANCE_CONFIG[Instance Type Config]
        VARIABLES_TF --> ENVIRONMENT_CONFIG[Environment Settings]
        
        OUTPUTS_TF --> URLS[Application URLs]
        OUTPUTS_TF --> SSH_INFO[SSH Connection Info]
        OUTPUTS_TF --> INSTANCE_INFO[Instance Details]
    end
    
    style MAIN_TF fill:#e8f5e8
    style TFVARS fill:#fff8e1
```

### 4. CI/CD Pipeline Structure

```mermaid
graph TB
    subgraph "⚙️ GitHub Actions Workflows"
        MAIN_WORKFLOW[ci-cd.yml]
        AI_WORKFLOW[ai-generate-workflow.yml]
        
        MAIN_WORKFLOW --> VALIDATE_JOB[Validation Job]
        MAIN_WORKFLOW --> TEST_JOB[Test Job]
        MAIN_WORKFLOW --> DEPLOY_JOB[Deploy Job]
        
        VALIDATE_JOB --> YAML_VALIDATE[YAML Validation]
        VALIDATE_JOB --> TERRAFORM_VALIDATE[Terraform Validation]
        
        TEST_JOB --> BACKEND_TEST[Backend Testing]
        TEST_JOB --> FRONTEND_TEST[Frontend Testing]
        TEST_JOB --> LINT_CHECK[Code Linting]
        
        DEPLOY_JOB --> TERRAFORM_PLAN[Terraform Plan]
        DEPLOY_JOB --> TERRAFORM_APPLY[Terraform Apply]
        DEPLOY_JOB --> HEALTH_CHECK[Health Checks]
        DEPLOY_JOB --> EMAIL_NOTIFY[Email Notification]
        
        AI_WORKFLOW --> AUTO_GENERATE[Auto Pipeline Generation]
        AI_WORKFLOW --> CREATE_PR[Create Pull Request]
    end
    
    style MAIN_WORKFLOW fill:#fff8e1
    style AI_WORKFLOW fill:#f3e5f5
```

## 🔧 Technology Stack Architecture

```mermaid
graph TB
    subgraph "💻 Development Stack"
        PYTHON[Python 3.11]
        JAVASCRIPT[JavaScript/HTML/CSS]
        YAML_CONFIG[YAML Configuration]
        BASH[Bash Scripts]
    end
    
    subgraph "🤖 AI & Analysis"
        OPENAI_API[OpenAI GPT-3.5-turbo]
        CODE_ANALYSIS[Code Pattern Recognition]
        INTELLIGENT_RECOMMENDATIONS[Smart Recommendations]
    end
    
    subgraph "🏗️ Infrastructure as Code"
        TERRAFORM_CORE[Terraform >= 1.5.0]
        AWS_PROVIDER[AWS Provider]
        TEMPLATE_FILES[Template Files]
    end
    
    subgraph "🐳 Containerization"
        DOCKER[Docker Engine]
        DOCKER_COMPOSE[Docker Compose]
        NGINX_PROXY[Nginx Reverse Proxy]
    end
    
    subgraph "☁️ AWS Services"
        EC2_SERVICE[EC2 Instances]
        VPC_NETWORKING[VPC Networking]
        SECURITY_GROUPS[Security Groups]
        ELASTIC_IPS[Elastic IPs]
        EBS_STORAGE[EBS Storage]
    end
    
    subgraph "🚀 CI/CD Platform"
        GITHUB_ACTIONS_CORE[GitHub Actions]
        WORKFLOW_TRIGGERS[Workflow Triggers]
        SECRET_MANAGEMENT[Secrets Management]
        NOTIFICATION_SYSTEM[Notification System]
    end
    
    %% Connections
    PYTHON --> OPENAI_API
    TERRAFORM_CORE --> AWS_PROVIDER
    DOCKER_COMPOSE --> NGINX_PROXY
    GITHUB_ACTIONS_CORE --> TERRAFORM_CORE
    TERRAFORM_CORE --> EC2_SERVICE
    
    style OPENAI_API fill:#fff3e0
    style TERRAFORM_CORE fill:#e8f5e8
    style GITHUB_ACTIONS_CORE fill:#fff8e1
    style EC2_SERVICE fill:#f3e5f5
```

## 📊 Data Flow Architecture

```mermaid
graph LR
    subgraph "📥 Input Sources"
        PIPELINE_REQUEST[pipeline_request.txt]
        CODEBASE[Existing Codebase]
        OPENAI_TOKEN[OpenAI API Token]
        GITHUB_SECRETS[GitHub Secrets]
    end
    
    subgraph "🔄 Processing Engine"
        CONFIG_PARSER[Configuration Parser]
        CODE_ANALYZER[Code Analyzer]
        AI_ENHANCER[AI Enhancement Engine]
        TEMPLATE_ENGINE[Template Generator]
    end
    
    subgraph "📤 Generated Outputs"
        TERRAFORM_FILES[Terraform Files]
        GITHUB_WORKFLOWS[GitHub Workflows]
        DOCKER_CONFIGS[Docker Configurations]
        DOCUMENTATION[Documentation]
        VERSION_FILE[Version Tracking]
    end
    
    subgraph "🚀 Deployment Artifacts"
        AWS_INFRASTRUCTURE[AWS Infrastructure]
        CONTAINERIZED_APPS[Containerized Applications]
        MONITORING_SETUP[Monitoring & Logging]
        NOTIFICATION_CONFIG[Notification Setup]
    end
    
    %% Data Flow
    PIPELINE_REQUEST --> CONFIG_PARSER
    CODEBASE --> CODE_ANALYZER
    OPENAI_TOKEN --> AI_ENHANCER
    
    CONFIG_PARSER --> TEMPLATE_ENGINE
    CODE_ANALYZER --> AI_ENHANCER
    AI_ENHANCER --> TEMPLATE_ENGINE
    
    TEMPLATE_ENGINE --> TERRAFORM_FILES
    TEMPLATE_ENGINE --> GITHUB_WORKFLOWS
    TEMPLATE_ENGINE --> DOCKER_CONFIGS
    TEMPLATE_ENGINE --> DOCUMENTATION
    TEMPLATE_ENGINE --> VERSION_FILE
    
    TERRAFORM_FILES --> AWS_INFRASTRUCTURE
    DOCKER_CONFIGS --> CONTAINERIZED_APPS
    GITHUB_WORKFLOWS --> MONITORING_SETUP
    GITHUB_SECRETS --> NOTIFICATION_CONFIG
    
    style AI_ENHANCER fill:#fff3e0
    style TEMPLATE_ENGINE fill:#e8f5e8
    style AWS_INFRASTRUCTURE fill:#f3e5f5
```

## 🔐 Security Architecture

```mermaid
graph TB
    subgraph "🛡️ Security Layers"
        GITHUB_SECRETS[GitHub Secrets Management]
        AWS_IAM[AWS IAM Roles & Policies]
        SECURITY_GROUPS[EC2 Security Groups]
        ENCRYPTED_STORAGE[Encrypted EBS Volumes]
        
        GITHUB_SECRETS --> API_KEYS[API Keys Protection]
        GITHUB_SECRETS --> AWS_CREDENTIALS[AWS Credentials]
        
        AWS_IAM --> LEAST_PRIVILEGE[Least Privilege Access]
        AWS_IAM --> SERVICE_ROLES[Service-Specific Roles]
        
        SECURITY_GROUPS --> PORT_RESTRICTIONS[Port-based Access Control]
        SECURITY_GROUPS --> IP_WHITELISTING[IP Address Restrictions]
        
        ENCRYPTED_STORAGE --> DATA_PROTECTION[Data at Rest Protection]
        ENCRYPTED_STORAGE --> VOLUME_ENCRYPTION[Volume-level Encryption]
    end
    
    style GITHUB_SECRETS fill:#ffebee
    style AWS_IAM fill:#e8f5e8
    style SECURITY_GROUPS fill:#fff3e0
    style ENCRYPTED_STORAGE fill:#f3e5f5
```

This architecture diagram shows how the AI-powered CI/CD pipeline generator creates a comprehensive DevOps automation system that can intelligently analyze codebases, generate infrastructure, and deploy applications with minimal human intervention.

**Key Architectural Benefits:**
- 🤖 **AI-Driven**: Intelligent code analysis and recommendations
- 🔄 **Fully Automated**: End-to-end pipeline generation
- 🏗️ **Infrastructure as Code**: Reproducible and version-controlled infrastructure
- 🚀 **Cloud-Native**: Designed for modern cloud deployment
- 🔐 **Security-First**: Built-in security best practices
- 📊 **Observable**: Comprehensive monitoring and logging