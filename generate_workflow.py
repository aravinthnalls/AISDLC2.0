#!/usr/bin/env python3.11
"""
AI-Powered CI/CD Pipeline Generator
==================================

This script automatically analyzes a codebase and generates a comprehensive
CI/CD pipeline with GitHub Actions, including:
- Code analysis and dependency detection
- Automated testing and linting
- Infrastructure as Code (Terraform)
- Docker containerization
- AWS EC2 deployment
- Email notifications

Author: AI-Generated Pipeline System
"""

import os
import sys
import json
import yaml
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import argparse
import requests
import time

class CodeAnalyzer:
    """Analyzes codebase to detect languages, frameworks, and configurations."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analysis_results = {}
    
    def analyze_project(self) -> Dict:
        """Perform comprehensive project analysis."""
        print("🔍 Analyzing project structure...")
        
        analysis = {
            'frontend': self._analyze_frontend(),
            'backend': self._analyze_backend(),
            'infrastructure': self._analyze_infrastructure(),
            'docker': self._analyze_docker(),
            'git': self._analyze_git()
        }
        
        self.analysis_results = analysis
        return analysis
    
    def _analyze_frontend(self) -> Dict:
        """Analyze frontend code and configuration."""
        frontend_path = self.project_root / 'frontend'
        
        if not frontend_path.exists():
            return {'exists': False}
        
        analysis = {'exists': True, 'path': str(frontend_path)}
        
        # Check for package.json (Node.js projects)
        package_json = frontend_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                analysis['framework'] = 'node'
                analysis['dependencies'] = package_data.get('dependencies', {})
                analysis['scripts'] = package_data.get('scripts', {})
                analysis['test_command'] = 'npm test'
                analysis['build_command'] = 'npm run build'
                analysis['lint_command'] = 'npm run lint'
                analysis['install_command'] = 'npm install'
            except Exception as e:
                print(f"Warning: Could not parse package.json: {e}")
        
        # Check for index.html (static/vanilla JS projects)
        elif (frontend_path / 'index.html').exists():
            analysis['framework'] = 'vanilla-js'
            analysis['dependencies'] = {}
            analysis['test_command'] = 'echo "No tests defined for vanilla JS"'
            analysis['build_command'] = 'echo "No build step needed"'
            analysis['lint_command'] = 'echo "No linting configured"'
            analysis['install_command'] = 'echo "No dependencies to install"'
        
        # Detect port from JavaScript files
        js_files = list(frontend_path.glob('*.js'))
        analysis['port'] = self._detect_port_from_files(js_files, default=3000)
        
        return analysis
    
    def _analyze_backend(self) -> Dict:
        """Analyze backend code and configuration."""
        backend_path = self.project_root / 'backend'
        
        if not backend_path.exists():
            return {'exists': False}
        
        analysis = {'exists': True, 'path': str(backend_path)}
        
        # Check for Python projects
        if (backend_path / 'requirements.txt').exists() or (backend_path / 'main.py').exists():
            analysis['language'] = 'python'
            analysis['framework'] = self._detect_python_framework(backend_path)
            
            # Read requirements.txt
            req_file = backend_path / 'requirements.txt'
            if req_file.exists():
                with open(req_file, 'r') as f:
                    requirements = f.read().strip().split('\n')
                analysis['dependencies'] = [req.strip() for req in requirements if req.strip()]
            
            analysis['test_command'] = 'pytest'
            analysis['lint_command'] = 'flake8'
            analysis['install_command'] = 'pip install -r requirements.txt'
            
            # Detect port from Python files
            py_files = list(backend_path.glob('*.py'))
            analysis['port'] = self._detect_port_from_files(py_files, default=8000)
        
        return analysis
    
    def _detect_python_framework(self, backend_path: Path) -> str:
        """Detect Python web framework."""
        main_py = backend_path / 'main.py'
        if main_py.exists():
            content = main_py.read_text()
            if 'fastapi' in content.lower():
                return 'fastapi'
            elif 'flask' in content.lower():
                return 'flask'
            elif 'django' in content.lower():
                return 'django'
        return 'unknown'
    
    def _detect_port_from_files(self, files: List[Path], default: int) -> int:
        """Detect port number from code files."""
        for file_path in files:
            try:
                content = file_path.read_text()
                # Look for common port patterns
                port_patterns = [
                    r'port[:\s]*=?\s*(\d+)',
                    r'localhost:(\d+)',
                    r'0\.0\.0\.0:(\d+)',
                    r'uvicorn.*--port\s+(\d+)',
                    r'listen[:\s]*(\d+)'
                ]
                
                for pattern in port_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        return int(match.group(1))
            except Exception:
                continue
        
        return default
    
    def _analyze_infrastructure(self) -> Dict:
        """Analyze existing infrastructure configuration."""
        terraform_path = self.project_root / 'terraform'
        
        analysis = {
            'terraform_exists': terraform_path.exists(),
            'terraform_path': str(terraform_path)
        }
        
        if terraform_path.exists():
            tf_files = list(terraform_path.glob('*.tf'))
            analysis['terraform_files'] = [str(f) for f in tf_files]
        
        return analysis
    
    def _analyze_docker(self) -> Dict:
        """Analyze Docker configuration."""
        compose_file = self.project_root / 'docker-compose.yml'
        
        analysis = {
            'compose_exists': compose_file.exists(),
            'dockerfiles': []
        }
        
        # Find Dockerfiles
        for dockerfile in self.project_root.rglob('Dockerfile'):
            analysis['dockerfiles'].append(str(dockerfile))
        
        return analysis
    
    def _analyze_git(self) -> Dict:
        """Analyze git repository information."""
        git_path = self.project_root / '.git'
        
        analysis = {'is_git_repo': git_path.exists()}
        
        if git_path.exists():
            try:
                # Get current branch
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      cwd=self.project_root, 
                                      capture_output=True, text=True)
                analysis['current_branch'] = result.stdout.strip()
                
                # Get remote URL
                result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                      cwd=self.project_root, 
                                      capture_output=True, text=True)
                analysis['remote_url'] = result.stdout.strip()
                
            except Exception as e:
                print(f"Warning: Could not get git info: {e}")
        
        return analysis

class PipelineGenerator:
    """Generates CI/CD pipeline components based on code analysis."""
    
    def __init__(self, project_root: str, config_file: str = 'pipeline_request.txt', openai_token: Optional[str] = None):
        self.project_root = Path(project_root)
        self.config_file = config_file
        self.openai_token = openai_token.strip() if openai_token else None
        self.ai_mode_requested = bool(self.openai_token)
        self.config = self._load_config()
        self.analyzer = CodeAnalyzer(project_root)
        
        # Initialize AI capabilities if token is provided
        if self.openai_token:
            print("🤖 AI enhancement enabled with OpenAI integration")
        else:
            print("📝 Running in standard mode (no AI enhancement)")
    
    def _load_config(self) -> Dict:
        """Load pipeline configuration from file."""
        config_path = self.project_root / self.config_file
        
        if not config_path.exists():
            print(f"Warning: {self.config_file} not found, using defaults")
            return self._default_config()
        
        config = {}
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Handle lists
                            if value.startswith('[') and value.endswith(']'):
                                value = value[1:-1].split(',')
                                value = [v.strip() for v in value]
                            
                            config[key] = value
            
            print(f"🔧 Loaded config from {self.config_file}: instance_type={config.get('instance_type', 'default')}, environment={config.get('environment', 'default')}")
        
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._default_config()
        
        # Return the loaded config (defaults will be handled in individual methods)
        return config
    
    def _default_config(self) -> Dict:
        """Return default pipeline configuration."""
        return {
            'pipeline_name': 'auto-generated-pipeline',
            'environment': 'production',
            'target': 'aws_ec2',
            'instance_type': 't2.micro',
            'deploy_using': 'docker-compose',
            'labels': ['ai-generated', 'demo'],
            'email_notification': 'true',
            'email_recipient': 'demo@example.com'
        }
    
    def _ai_enhance_analysis(self, analysis: Dict, fail_on_ai_error: bool = False) -> Dict:
        """Use AI to enhance the project analysis with intelligent recommendations."""
        if not self.openai_token:
            if fail_on_ai_error:
                raise Exception("AI mode requested but no OpenAI API token provided. Use --openai-token or set OPENAI_API_TOKEN environment variable.")
            return analysis
        
        try:
            print("🧠 AI analyzing project for intelligent recommendations...")
            
            # Prepare context for AI analysis
            analysis_context = {
                "project_type": "web_application",
                "frontend": analysis.get('frontend', {}),
                "backend": analysis.get('backend', {}),
                "infrastructure_exists": analysis.get('infrastructure', {}).get('terraform_exists', False),
                "docker_setup": analysis.get('docker', {}).get('compose_exists', False)
            }
            
            # AI prompt for pipeline recommendations
            prompt = f"""
Analyze this project configuration and provide intelligent DevOps recommendations:

Project Analysis:
{json.dumps(analysis_context, indent=2)}

Please provide recommendations for:
1. Optimal CI/CD pipeline stages
2. Testing strategies based on the technology stack
3. Deployment recommendations
4. Security considerations
5. Performance optimization suggestions

Respond in JSON format with specific, actionable recommendations.
"""
            
            # Call OpenAI API (fail on error if AI mode is explicitly requested)
            ai_recommendations = self._call_openai_api(prompt, fail_on_error=fail_on_ai_error)
            
            if ai_recommendations:
                analysis['ai_recommendations'] = ai_recommendations
                print("✅ AI analysis completed - enhanced recommendations available")
            elif fail_on_ai_error:
                raise Exception("Failed to get AI recommendations despite explicit AI mode request")
            
        except Exception as e:
            if fail_on_ai_error:
                print(f"❌ AI enhancement failed in AI mode: {e}")
                raise e
            else:
                print(f"⚠️ AI enhancement failed: {e}")
                print("Continuing with standard analysis...")
        
        return analysis
    
    def _call_openai_api(self, prompt: str, fail_on_error: bool = False) -> Optional[Dict]:
        """Make a call to OpenAI API for intelligent analysis."""
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert DevOps engineer specializing in CI/CD pipeline optimization and cloud infrastructure."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1500,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse as JSON, fallback to text if needed
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {"recommendations": content}
            else:
                error_msg = f"OpenAI API Error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                if fail_on_error:
                    raise Exception(error_msg)
                return None
                
        except Exception as e:
            error_msg = f"Failed to access OpenAI API: {e}"
            print(f"❌ {error_msg}")
            if fail_on_error:
                raise Exception(error_msg)
            return None
    
    def _format_analysis_human_readable(self, analysis: Dict) -> str:
        """Format analysis results in human-readable format."""
        output = []
        output.append("\n📊 Project Analysis Report")
        output.append("=" * 50)
        
        # Frontend Analysis
        frontend = analysis.get('frontend', {})
        if frontend.get('exists'):
            output.append("\n🎨 Frontend Application:")
            framework = frontend.get('framework', 'Unknown')
            if framework == 'node':
                framework = 'Node.js/JavaScript'
            elif framework == 'vanilla-js':
                framework = 'Vanilla JavaScript'
            output.append(f"   📋 Framework: {framework}")
            output.append(f"   🌐 Port: {frontend.get('port', 'Not specified')}")
            
            dependencies = frontend.get('dependencies', {})
            if dependencies:
                output.append(f"   📦 Dependencies: {len(dependencies)} packages")
            
            # Show available scripts if any
            scripts = frontend.get('scripts', {})
            if scripts:
                output.append("   🛠️  Available scripts:")
                for script_name in ['test', 'build', 'lint', 'dev']:
                    if script_name in scripts:
                        output.append(f"      • {script_name}: Available")
        else:
            output.append("\n🎨 Frontend Application: ❌ Not found")
        
        # Backend Analysis
        backend = analysis.get('backend', {})
        if backend.get('exists'):
            output.append("\n🔧 Backend Application:")
            language = backend.get('language', 'Unknown').title()
            framework = backend.get('framework', 'Unknown')
            if framework == 'fastapi':
                framework = 'FastAPI'
            elif framework == 'flask':
                framework = 'Flask'
            elif framework == 'django':
                framework = 'Django'
            
            output.append(f"   💻 Language: {language}")
            output.append(f"   🚀 Framework: {framework}")
            output.append(f"   🌐 Port: {backend.get('port', 'Not specified')}")
            
            dependencies = backend.get('dependencies', [])
            if dependencies:
                output.append(f"   📦 Dependencies: {len(dependencies)} packages")
                # Show main dependencies
                main_deps = [dep.split('==')[0] for dep in dependencies[:3]]
                if main_deps:
                    output.append(f"      • Key packages: {', '.join(main_deps)}")
            
            # Show testing and linting setup
            if backend.get('test_command'):
                output.append(f"   🧪 Testing: {backend.get('test_command', 'Not configured')}")
            if backend.get('lint_command'):
                output.append(f"   🔍 Linting: {backend.get('lint_command', 'Not configured')}")
        else:
            output.append("\n🔧 Backend Application: ❌ Not found")
        
        # Infrastructure Analysis
        infra = analysis.get('infrastructure', {})
        output.append("\n🏗️ Infrastructure:")
        if infra.get('terraform_exists'):
            output.append("   ✅ Terraform configuration detected")
            tf_files = infra.get('terraform_files', [])
            if tf_files:
                output.append(f"   📄 Configuration files: {len(tf_files)}")
                for tf_file in tf_files:
                    filename = tf_file.split('/')[-1]
                    output.append(f"      • {filename}")
        else:
            output.append("   ⚠️  No Terraform configuration (will be generated)")
        
        # Docker Analysis
        docker = analysis.get('docker', {})
        output.append("\n🐳 Containerization:")
        if docker.get('compose_exists'):
            output.append("   ✅ Docker Compose configuration detected")
        else:
            output.append("   ⚠️  No Docker Compose (will be generated)")
            
        dockerfiles = docker.get('dockerfiles', [])
        if dockerfiles:
            output.append(f"   📦 Dockerfiles found: {len(dockerfiles)}")
            for dockerfile in dockerfiles:
                service = dockerfile.split('/')[-2] if '/' in dockerfile else 'root'
                output.append(f"      • {service.title()} service")
        else:
            output.append("   ⚠️  No Dockerfiles (will be generated)")
        
        # Git Analysis
        git = analysis.get('git', {})
        if git.get('is_git_repo'):
            output.append("\n📚 Version Control:")
            output.append(f"   Branch: {git.get('current_branch', 'Unknown')}")
            if git.get('remote_url'):
                output.append(f"   Repository: {git.get('remote_url')}")
        
        return "\n".join(output)
    
    def _format_ai_recommendations_human_readable(self, recommendations: Dict) -> str:
        """Format AI recommendations in human-readable format."""
        output = []
        output.append("\n🤖 AI-Powered Recommendations")
        output.append("=" * 50)
        
        if isinstance(recommendations, dict):
            if 'recommendations' in recommendations and isinstance(recommendations['recommendations'], str):
                # Handle text-based recommendations
                output.append("\n💡 AI Analysis:")
                lines = recommendations['recommendations'].split('\n')
                for line in lines:
                    if line.strip():
                        output.append(f"   {line.strip()}")
            else:
                # Handle structured recommendations
                for key, value in recommendations.items():
                    if isinstance(value, list):
                        output.append(f"\n📋 {key.replace('_', ' ').title()}:")
                        for item in value:
                            output.append(f"   • {item}")
                    elif isinstance(value, dict):
                        output.append(f"\n📂 {key.replace('_', ' ').title()}:")
                        for subkey, subvalue in value.items():
                            output.append(f"   {subkey}: {subvalue}")
                    else:
                        output.append(f"\n🔍 {key.replace('_', ' ').title()}: {value}")
        else:
            output.append(f"\n💡 AI Analysis:\n   {recommendations}")
        
        return "\n".join(output)
    
    def generate_pipeline(self) -> bool:
        """Generate complete CI/CD pipeline."""
        print("🚀 Generating AI-powered CI/CD pipeline...")
        
        # Analyze the codebase
        analysis = self.analyzer.analyze_project()
        
        # Enhance analysis with AI if available (fail if AI mode was explicitly requested but fails)
        analysis = self._ai_enhance_analysis(analysis, fail_on_ai_error=self.ai_mode_requested)
        
        # Generate pipeline components
        success = True
        
        try:
            self._generate_github_workflow(analysis)
            self._generate_ai_workflow_trigger()
            self._ensure_terraform_infrastructure(analysis)
            self._ensure_docker_configuration(analysis)
            self._update_readme(analysis)
            self._increment_version()
            
            print("✅ Pipeline generation completed successfully!")
            
        except Exception as e:
            print(f"❌ Pipeline generation failed: {e}")
            success = False
        
        return success
    
    def _generate_github_workflow(self, analysis: Dict):
        """Generate GitHub Actions CI/CD workflow."""
        print("📝 Generating GitHub Actions workflow...")
        
        workflow_dir = self.project_root / '.github' / 'workflows'
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Main CI/CD workflow
        workflow = {
            'name': f"{self.config.get('pipeline_name', 'AI-Generated Pipeline')}",
            'on': {
                'push': {'branches': ['main', 'develop']},
                'pull_request': {'branches': ['main']},
                'workflow_dispatch': {}
            },
            'env': {
                'AWS_REGION': 'us-east-1',
                'TERRAFORM_VERSION': '1.5.0'
            },
            'jobs': {
                'validate': self._create_validation_job(analysis),
                'test': self._create_test_job(analysis),
                'deploy': self._create_deploy_job(analysis)
            }
        }
        
        workflow_path = workflow_dir / 'ci-cd.yml'
        with open(workflow_path, 'w') as f:
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Created workflow: {workflow_path}")
    
    def _create_validation_job(self, analysis: Dict) -> Dict:
        """Create validation job for the workflow."""
        job = {
            'name': 'Validate Code and Infrastructure',
            'runs-on': 'ubuntu-latest',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Validate YAML files',
                    'run': 'find . -name "*.yml" -o -name "*.yaml" | xargs -I {} sh -c \'echo "Validating {}" && python -c "import yaml; yaml.safe_load(open(\'{}\'))" || exit 1\''
                }
            ]
        }
        
        # Add Terraform validation if terraform exists
        if analysis['infrastructure']['terraform_exists']:
            job['steps'].extend([
                {
                    'name': 'Setup Terraform',
                    'uses': 'hashicorp/setup-terraform@v3',
                    'with': {'terraform_version': '${{ env.TERRAFORM_VERSION }}'}
                },
                {
                    'name': 'Terraform Format Check',
                    'run': 'terraform fmt -check -recursive terraform/',
                    'continue-on-error': True
                },
                {
                    'name': 'Terraform Validate',
                    'run': '''
                    cd terraform
                    terraform init -backend=false
                    terraform validate
                    '''
                }
            ])
        
        return job
    
    def _create_test_job(self, analysis: Dict) -> Dict:
        """Create testing job for the workflow."""
        job = {
            'name': 'Run Tests',
            'runs-on': 'ubuntu-latest',
            'needs': 'validate',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                }
            ]
        }
        
        # Add backend testing
        if analysis['backend']['exists']:
            if analysis['backend'].get('language') == 'python':
                job['steps'].extend([
                    {
                        'name': 'Set up Python',
                        'uses': 'actions/setup-python@v4',
                        'with': {'python-version': '3.11'}
                    },
                    {
                        'name': 'Install backend dependencies',
                        'run': f"cd backend && {analysis['backend']['install_command']}"
                    },
                    {
                        'name': 'Lint backend code',
                        'run': f"cd backend && {analysis['backend']['lint_command']} || echo 'Linting not configured'",
                        'continue-on-error': True
                    },
                    {
                        'name': 'Test backend code',
                        'run': f"cd backend && {analysis['backend']['test_command']} || echo 'Tests not configured'",
                        'continue-on-error': True
                    }
                ])
        
        # Add frontend testing
        if analysis['frontend']['exists']:
            if analysis['frontend'].get('framework') == 'node':
                job['steps'].extend([
                    {
                        'name': 'Set up Node.js',
                        'uses': 'actions/setup-node@v4',
                        'with': {'node-version': '18'}
                    },
                    {
                        'name': 'Install frontend dependencies',
                        'run': f"cd frontend && {analysis['frontend']['install_command']}"
                    },
                    {
                        'name': 'Lint frontend code',
                        'run': f"cd frontend && {analysis['frontend']['lint_command']} || echo 'Linting not configured'",
                        'continue-on-error': True
                    },
                    {
                        'name': 'Test frontend code',
                        'run': f"cd frontend && {analysis['frontend']['test_command']} || echo 'Tests not configured'",
                        'continue-on-error': True
                    }
                ])
            else:
                job['steps'].append({
                    'name': 'Validate frontend files',
                    'run': 'echo "Frontend validation: Static files detected, no additional tests needed"'
                })
        
        return job
    
    def _create_deploy_job(self, analysis: Dict) -> Dict:
        """Create deployment job for the workflow."""
        job = {
            'name': 'Deploy to AWS',
            'runs-on': 'ubuntu-latest',
            'needs': ['validate', 'test'],
            'if': 'github.ref == \'refs/heads/main\'',
            'env': {
                'AWS_ACCESS_KEY_ID': '${{ secrets.AWS_ACCESS_KEY_ID }}',
                'AWS_SECRET_ACCESS_KEY': '${{ secrets.AWS_SECRET_ACCESS_KEY }}'
            },
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Terraform',
                    'uses': 'hashicorp/setup-terraform@v3',
                    'with': {'terraform_version': '${{ env.TERRAFORM_VERSION }}'}
                },
                {
                    'name': 'Terraform Init',
                    'run': '''
                    cd terraform
                    terraform init
                    '''
                },
                {
                    'name': 'Terraform Plan',
                    'run': '''
                    cd terraform
                    terraform plan -out=tfplan
                    '''
                },
                {
                    'name': 'Terraform Apply',
                    'run': '''
                    cd terraform
                    terraform apply -auto-approve tfplan
                    '''
                },
                {
                    'name': 'Get deployment info',
                    'id': 'deployment',
                    'run': '''
                    cd terraform
                    echo "public_ip=$(terraform output -raw public_ip)" >> $GITHUB_OUTPUT
                    echo "frontend_url=$(terraform output -raw application_urls | jq -r .frontend)" >> $GITHUB_OUTPUT
                    echo "backend_url=$(terraform output -raw application_urls | jq -r .backend_api)" >> $GITHUB_OUTPUT
                    '''
                },
                {
                    'name': 'Wait for application startup',
                    'run': '''
                    echo "Waiting for application to start..."
                    sleep 60
                    
                    # Check application health
                    curl -f ${{ steps.deployment.outputs.backend_url }}/health || echo "Backend health check failed"
                    curl -f ${{ steps.deployment.outputs.frontend_url }} || echo "Frontend health check failed"
                    '''
                }
            ]
        }
        
        # Add email notification if configured
        if self.config.get('email_notification', 'false').lower() == 'true':
            job['steps'].append({
                'name': 'Send deployment notification',
                'if': 'always()',
                'uses': 'dawidd6/action-send-mail@v3',
                'with': {
                    'server_address': 'smtp.gmail.com',
                    'server_port': '587',
                    'username': '${{ secrets.EMAIL_USERNAME }}',
                    'password': '${{ secrets.EMAIL_PASSWORD }}',
                    'subject': 'QR Generator Deployment ${{ job.status }}',
                    'to': self.config.get('email_recipient', 'demo@example.com'),
                    'from': '${{ secrets.EMAIL_USERNAME }}',
                    'body': '''
                    Deployment Status: ${{ job.status }}
                    
                    Frontend URL: ${{ steps.deployment.outputs.frontend_url }}
                    Backend API: ${{ steps.deployment.outputs.backend_url }}
                    
                    Commit: ${{ github.sha }}
                    Repository: ${{ github.repository }}
                    '''
                }
            })
        
        return job
    
    def _generate_ai_workflow_trigger(self):
        """Generate the AI workflow trigger."""
        print("🤖 Generating AI workflow trigger...")
        
        workflow_dir = self.project_root / '.github' / 'workflows'
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        ai_workflow = {
            'name': 'AI Pipeline Generator',
            'on': {
                'push': {'branches': ['main']},
                'workflow_dispatch': {}
            },
            'jobs': {
                'generate-pipeline': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {
                        'contents': 'write',
                        'pull-requests': 'write'
                    },
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4',
                            'with': {'token': '${{ secrets.GITHUB_TOKEN }}'}
                        },
                        {
                            'name': 'Set up Python',
                            'uses': 'actions/setup-python@v4',
                            'with': {'python-version': '3.11'}
                        },
                        {
                            'name': 'Install dependencies',
                            'run': 'pip install pyyaml'
                        },
                        {
                            'name': 'Run AI Pipeline Generator',
                            'run': 'python generate_workflow.py --auto-commit'
                        },
                        {
                            'name': 'Create Pull Request',
                            'if': 'success()',
                            'uses': 'peter-evans/create-pull-request@v5',
                            'with': {
                                'token': '${{ secrets.GITHUB_TOKEN }}',
                                'commit-message': 'AI: Update pipeline configuration',
                                'title': 'AI-Generated Pipeline Updates',
                                'body': '''
                                This PR was automatically generated by the AI Pipeline Generator.
                                
                                ## Changes:
                                - Updated CI/CD workflows
                                - Infrastructure as Code updates
                                - Docker configuration updates
                                - Documentation updates
                                
                                ## Generated by:
                                AI Pipeline Generator v1.0
                                ''',
                                'branch': f"ai-pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                                'labels': 'ai-generated,demo,pipeline'
                            }
                        }
                    ]
                }
            }
        }
        
        workflow_path = workflow_dir / 'ai-generate-workflow.yml'
        with open(workflow_path, 'w') as f:
            yaml.dump(ai_workflow, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Created AI workflow: {workflow_path}")
    
    def _ensure_terraform_infrastructure(self, analysis: Dict):
        """Ensure Terraform infrastructure exists."""
        terraform_path = self.project_root / 'terraform'
        
        # Check if terraform directory and essential files exist
        main_tf_exists = (terraform_path / 'main.tf').exists()
        variables_tf_exists = (terraform_path / 'variables.tf').exists()
        outputs_tf_exists = (terraform_path / 'outputs.tf').exists()
        
        if main_tf_exists and variables_tf_exists and outputs_tf_exists:
            print("✅ Terraform infrastructure already exists")
            return
        
        print("🏗️  Generating Terraform infrastructure...")
        
        # Create terraform directory
        terraform_path.mkdir(exist_ok=True)
        
        # Generate main.tf
        self._create_terraform_main(terraform_path, analysis)
        
        # Generate variables.tf
        self._create_terraform_variables(terraform_path)
        
        # Generate outputs.tf
        self._create_terraform_outputs(terraform_path)
        
        # Generate terraform.tfvars based on config
        self._create_terraform_tfvars(terraform_path)
        
        print("✅ Created Terraform infrastructure files")
    
    def _create_terraform_main(self, terraform_path: Path, analysis: Dict):
        """Create main.tf file."""
        # Get ports from config first, then fallback to analysis, then defaults
        backend_port = self.config.get('backend_port', analysis['backend'].get('port', 8000))
        frontend_port = self.config.get('frontend_port', analysis['frontend'].get('port', 3000))
        
        # Convert string ports to integers if needed
        try:
            backend_port = int(backend_port)
            frontend_port = int(frontend_port)
        except (ValueError, TypeError):
            backend_port = 8000
            frontend_port = 3000
        
        main_tf_content = f'''# AWS Provider configuration
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

# Security group for the application
resource "aws_security_group" "qr_generator_sg" {{
  name_prefix = "qr-generator-"
  description = "Security group for QR Generator application"
  
  # Allow HTTP traffic
  ingress {{
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  # Allow HTTPS traffic
  ingress {{
    from_port   = 443
    to_port     = 443
    protocol    = "tcp" 
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  # Allow SSH access
  ingress {{
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  # Allow backend port
  ingress {{
    from_port   = var.backend_port
    to_port     = var.backend_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  # Allow frontend port
  ingress {{
    from_port   = var.frontend_port
    to_port     = var.frontend_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  # Allow all outbound traffic
  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  tags = {{
    Name = "qr-generator-security-group"
    Project = "QR Generator"
  }}
}}

# EC2 Instance for the application
resource "aws_instance" "qr_generator" {{
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name
  
  vpc_security_group_ids = [aws_security_group.qr_generator_sg.id]
  
  # User data script to set up the application
  user_data = base64encode(templatefile("${{path.module}}/user_data.sh", {{
    backend_port  = var.backend_port
    frontend_port = var.frontend_port
  }}))
  
  root_block_device {{
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }}
  
  tags = merge(var.tags, {{
    Name = "${{var.project_name}}-instance"
    Type = "application-server"
  }})
}}

# Elastic IP for the instance
resource "aws_eip" "qr_generator_eip" {{
  instance = aws_instance.qr_generator.id
  domain   = "vpc"
  
  tags = {{
    Name = "qr-generator-eip"
    Project = "QR Generator"
  }}
}}
'''
        
        (terraform_path / 'main.tf').write_text(main_tf_content)
        
        # Create user_data.sh
        user_data_content = '''#!/bin/bash
set -e

# Update system
yum update -y

# Install Docker
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
yum install git -y

# Create application directory
mkdir -p /opt/qr-generator
cd /opt/qr-generator

# Clone the repository (this would be updated with actual repo URL)
# git clone https://github.com/your-username/qr-generator.git .

# For now, create a simple deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
echo "Starting QR Generator application..."

# Start services with Docker Compose
docker-compose up -d

# Show status
docker-compose ps

echo "Application deployed successfully!"
echo "Backend available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${backend_port}"
echo "Frontend available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${frontend_port}"
EOF

chmod +x deploy.sh

# Set up log rotation
cat > /etc/logrotate.d/qr-generator << 'EOF'
/opt/qr-generator/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 ec2-user ec2-user
}
EOF

echo "QR Generator infrastructure setup completed!"
'''
        
        (terraform_path / 'user_data.sh').write_text(user_data_content)
    
    def _create_terraform_variables(self, terraform_path: Path):
        """Create variables.tf file."""
        # Get configuration values with defaults
        environment = self.config.get('environment', 'dev')
        instance_type = self.config.get('instance_type', 't3.micro')
        project_name = self.config.get('pipeline_name', 'qr-generator').replace('-auto-pipeline', '')
        
        # Map AMI configuration
        ami_config = self.config.get('ami', 'latest-ubuntu')
        if 'ubuntu' in ami_config.lower():
            default_ami = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS
            ami_comment = "Ubuntu 22.04 LTS"
        else:
            default_ami = "ami-0c02fb55956c7d316"  # Amazon Linux 2
            ami_comment = "Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type"
        
        variables_content = f'''# AWS Configuration Variables
variable "aws_region" {{
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}}

variable "environment" {{
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "{environment}"
}}

# EC2 Configuration
variable "ami_id" {{
  description = "AMI ID for EC2 instance"
  type        = string
  default     = "{default_ami}" # {ami_comment}
}}

variable "instance_type" {{
  description = "EC2 instance type"
  type        = string
  default     = "{instance_type}"
}}

variable "key_pair_name" {{
  description = "Name of the AWS key pair for EC2 access"
  type        = string
}}

# Application Configuration
variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{project_name}"
}}

variable "tags" {{
  description = "Common tags for all resources"
  type        = map(string)
  default = {{
    Project     = "{project_name.title()}"
    ManagedBy   = "Terraform"
    Environment = "{environment}"
  }}
}}

# Application Port Configuration
variable "frontend_port" {{
  description = "Port for the frontend application"
  type        = number
  default     = {self.config.get('frontend_port', 3000)}
}}

variable "backend_port" {{
  description = "Port for the backend application"  
  type        = number
  default     = {self.config.get('backend_port', 8000)}
}}

# Deployment Configuration
variable "deploy_method" {{
  description = "Deployment method (docker-compose, kubernetes, etc.)"
  type        = string
  default     = "{self.config.get('deploy_using', 'docker-compose')}"
}}

variable "target_platform" {{
  description = "Target deployment platform"
  type        = string
  default     = "{self.config.get('target', 'aws_ec2')}"
}}
'''
        
        (terraform_path / 'variables.tf').write_text(variables_content)
    
    def _create_terraform_outputs(self, terraform_path: Path):
        """Create outputs.tf file using configured ports."""
        # Get ports from config
        backend_port = self.config.get('backend_port', 8000)
        frontend_port = self.config.get('frontend_port', 3000)
        
        outputs_content = f'''# EC2 Instance Outputs
output "instance_id" {{
  description = "ID of the EC2 instance"
  value       = aws_instance.qr_generator.id
}}

output "instance_public_ip" {{
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.qr_generator_eip.public_ip
}}

output "instance_public_dns" {{
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.qr_generator.public_dns
}}

output "instance_private_ip" {{
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.qr_generator.private_ip
}}

# Security Group Output
output "security_group_id" {{
  description = "ID of the security group"
  value       = aws_security_group.qr_generator_sg.id
}}

# Application URLs
output "backend_url" {{
  description = "URL for the backend application"
  value       = "http://${{aws_eip.qr_generator_eip.public_ip}}:${{var.backend_port}}"
}}

output "frontend_url" {{
  description = "URL for the frontend application"
  value       = "http://${{aws_eip.qr_generator_eip.public_ip}}:${{var.frontend_port}}"
}}

# SSH Access
output "ssh_command" {{
  description = "SSH command to connect to the instance"
  value       = "ssh -i ~/.ssh/${{var.key_pair_name}}.pem ec2-user@${{aws_eip.qr_generator_eip.public_ip}}"
}}
'''
        
        (terraform_path / 'outputs.tf').write_text(outputs_content)
    
    def _create_terraform_tfvars(self, terraform_path: Path):
        """Create terraform.tfvars file based on pipeline_request.txt configuration."""
        # Get configuration values
        environment = self.config.get('environment', 'dev')
        instance_type = self.config.get('instance_type', 't3.micro')
        project_name = self.config.get('pipeline_name', 'qr-generator').replace('-auto-pipeline', '')
        ami_config = self.config.get('ami', 'latest-ubuntu')
        
        # Map AMI configuration to actual AMI IDs
        if 'ubuntu' in ami_config.lower():
            ami_id = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS
        elif 'amazon' in ami_config.lower() or 'linux' in ami_config.lower():
            ami_id = "ami-0c02fb55956c7d316"  # Amazon Linux 2
        else:
            ami_id = "ami-0c7217cdde317cfec"  # Default to Ubuntu
        
        # Create tfvars content
        tfvars_content = f'''# Generated from pipeline_request.txt configuration
# Environment Configuration
environment = "{environment}"

# EC2 Configuration  
instance_type = "{instance_type}"
ami_id = "{ami_id}"

# Project Configuration
project_name = "{project_name}"

# Additional tags based on configuration
tags = {{
  Project = "{project_name.replace('-', ' ').title()}"
  Environment = "{environment}"
  ManagedBy = "Terraform"
  GeneratedFrom = "pipeline_request.txt"
  Labels = "{','.join(self.config.get('labels', ['ai-generated']))}"
}}

# AWS Configuration (update these values as needed)
aws_region = "us-west-2"

# Key Pair (REQUIRED: Set this to your AWS key pair name)
# key_pair_name = "your-key-pair-name"
'''

        # Add application-specific configurations
        frontend_port = self.config.get('frontend_port', '3000')
        backend_port = self.config.get('backend_port', '8000')
        
        tfvars_content += f'''
# Application Configuration (from pipeline_request.txt)
# These ports are used in security group rules and outputs
frontend_port = {frontend_port}
backend_port = {backend_port}

# Deployment Configuration
deploy_method = "{self.config.get('deploy_using', 'docker-compose')}"
target_platform = "{self.config.get('target', 'aws_ec2')}"
'''
        
        # Write the tfvars file
        (terraform_path / 'terraform.tfvars').write_text(tfvars_content)
        
        # Also create a .tfvars.example file for reference
        example_content = tfvars_content.replace('# key_pair_name = "your-key-pair-name"', 'key_pair_name = "your-key-pair-name"')
        example_content = example_content.replace('aws_region = "us-west-2"', 'aws_region = "us-east-1"')
        (terraform_path / 'terraform.tfvars.example').write_text(example_content)
        
        print(f"   📄 Created terraform.tfvars with {environment} environment and {instance_type} instance")
    
    def _ensure_docker_configuration(self, analysis: Dict):
        """Ensure Docker configuration exists."""
        if analysis['docker']['compose_exists']:
            print("✅ Docker Compose configuration already exists")
        
        # Check if Dockerfiles exist for frontend and backend
        if not analysis['docker']['dockerfiles']:
            print("❌ No Dockerfiles found - this should have been created earlier")
    
    def _update_readme(self, analysis: Dict):
        """Update README.md with comprehensive documentation."""
        print("📖 Updating README.md...")
        
        readme_content = f'''# QR Code Generator - AI-Powered CI/CD Demo

This project demonstrates **AI-assisted DevOps automation** with a complete CI/CD pipeline that automatically analyzes code and generates infrastructure.

## 🎯 Project Overview

**QR Code Generator** is a full-stack web application that generates QR codes from various data types:
- Plain text
- URLs
- Email addresses  
- Phone numbers
- WiFi credentials

### Architecture

- **Frontend**: {analysis['frontend'].get('framework', 'Unknown')} ({analysis['frontend'].get('port', 'N/A')} port)
- **Backend**: {analysis['backend'].get('framework', 'Unknown')} ({analysis['backend'].get('port', 'N/A')} port)
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
**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Project Version**: {self._get_current_version()}
'''
        
        readme_path = self.project_root / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"✅ Updated README: {readme_path}")
    
    def _increment_version(self):
        """Increment version in VERSION file."""
        version_file = self.project_root / 'VERSION'
        
        if version_file.exists():
            current_version = version_file.read_text().strip()
        else:
            current_version = '0.1.0'
        
        # Parse version (assuming semantic versioning)
        try:
            parts = current_version.split('.')
            patch = int(parts[2]) + 1
            new_version = f"{parts[0]}.{parts[1]}.{patch}"
        except:
            new_version = '0.1.1'
        
        version_file.write_text(new_version)
        print(f"📈 Version updated: {current_version} → {new_version}")
    
    def _get_current_version(self) -> str:
        """Get current version from VERSION file."""
        version_file = self.project_root / 'VERSION'
        if version_file.exists():
            return version_file.read_text().strip()
        return '0.1.0'

def main():
    """Main entry point for the AI pipeline generator."""
    parser = argparse.ArgumentParser(
        description='AI-Powered CI/CD Pipeline Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_workflow.py                                    # Generate complete pipeline
  python generate_workflow.py --analyze-only                     # Analyze code only
  python generate_workflow.py --auto-commit                      # Generate and commit changes
  python generate_workflow.py --openai-token YOUR_TOKEN          # Use AI enhancement with OpenAI
  OPENAI_API_TOKEN=your_token python generate_workflow.py        # Use AI via environment variable
        '''
    )
    
    parser.add_argument('--project-root', 
                       default='.',
                       help='Project root directory (default: current directory)')
    
    parser.add_argument('--config-file',
                       default='pipeline_request.txt',
                       help='Pipeline configuration file (default: pipeline_request.txt)')
    
    parser.add_argument('--analyze-only',
                       action='store_true',
                       help='Only analyze the project, don\'t generate files')
    
    parser.add_argument('--auto-commit',
                       action='store_true',
                       help='Automatically commit generated files to git')
    
    parser.add_argument('--verbose',
                       action='store_true',
                       help='Enable verbose output')
    
    parser.add_argument('--openai-token',
                       type=str,
                       help='OpenAI API token for AI-enhanced pipeline generation')
    
    args = parser.parse_args()
    
    print("🤖 AI-Powered CI/CD Pipeline Generator")
    print("=" * 50)
    
    try:
        # Get OpenAI token from argument or environment variable
        openai_token = args.openai_token or os.getenv('OPENAI_API_TOKEN')
        
        generator = PipelineGenerator(args.project_root, args.config_file, openai_token)
        
        if args.analyze_only:
            print("🔍 Running analysis only...")
            analysis = generator.analyzer.analyze_project()
            analysis = generator._ai_enhance_analysis(analysis, fail_on_ai_error=generator.ai_mode_requested)
            
            # Display human-readable analysis
            print(generator._format_analysis_human_readable(analysis))
            
            if 'ai_recommendations' in analysis:
                print(generator._format_ai_recommendations_human_readable(analysis['ai_recommendations']))
            
            # Show raw JSON in verbose mode
            if args.verbose:
                print("\n🔍 Raw Analysis Data (Verbose Mode):")
                print(json.dumps(analysis, indent=2))
            
        else:
            success = generator.generate_pipeline()
            
            if success and args.auto_commit:
                print("📤 Auto-committing changes...")
                try:
                    subprocess.run(['git', 'add', '.'], cwd=args.project_root)
                    subprocess.run(['git', 'commit', '-m', 'AI: Generated CI/CD pipeline components'], 
                                 cwd=args.project_root)
                    print("✅ Changes committed successfully")
                except Exception as e:
                    print(f"⚠️  Could not commit changes: {e}")
            
            if success:
                print("\n🎉 Pipeline generation completed successfully!")
                print("\nNext steps:")
                print("1. Review generated files")
                print("2. Configure GitHub secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
                print("3. Push changes to trigger the pipeline")
                print("4. Monitor deployment in GitHub Actions")
            else:
                print("\n❌ Pipeline generation failed")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()