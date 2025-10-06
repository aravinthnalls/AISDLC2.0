#!/usr/bin/env python3.11
"""
Test script to verify the QR Generator demo setup
"""

import subprocess
import sys
import json
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, cwd=Path.cwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_files_exist():
    """Test that all required files exist."""
    print("🔍 Checking required files...")
    
    required_files = [
        'VERSION',
        'pipeline_request.txt',
        'docker-compose.yml',
        'generate_workflow.py',
        'frontend/Dockerfile',
        'backend/Dockerfile',
        'terraform/main.tf',
        'terraform/variables.tf',
        '.github/workflows/ci-cd.yml',
        '.github/workflows/ai-generate-workflow.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    print("  🎉 All required files exist!")
    return True

def test_docker_compose_syntax():
    """Test Docker Compose file syntax."""
    print("\n🐳 Testing Docker Compose syntax...")
    
    success, stdout, stderr = run_command("docker-compose config")
    if success:
        print("  ✅ docker-compose.yml syntax is valid")
        return True
    else:
        print(f"  ❌ docker-compose.yml syntax error: {stderr}")
        return False

def test_terraform_syntax():
    """Test Terraform file syntax."""
    print("\n🏗️  Testing Terraform syntax...")
    
    # Change to terraform directory and test
    success, stdout, stderr = run_command("cd terraform && terraform fmt -check")
    if success:
        print("  ✅ Terraform files are properly formatted")
    else:
        print("  ⚠️  Terraform formatting issues (non-critical)")
    
    # Test validation (requires init first)
    success, stdout, stderr = run_command("cd terraform && terraform init -backend=false")
    if not success:
        print(f"  ❌ Terraform init failed: {stderr}")
        return False
    
    success, stdout, stderr = run_command("cd terraform && terraform validate")
    if success:
        print("  ✅ Terraform configuration is valid")
        return True
    else:
        print(f"  ❌ Terraform validation failed: {stderr}")
        return False

def test_ai_generator():
    """Test the AI generator script."""
    print("\n🤖 Testing AI Generator...")
    
    # Test standard mode
    success, stdout, stderr = run_command("python3.11 generate_workflow.py --analyze-only")
    if success:
        print("  ✅ Standard mode analysis completed successfully")
    else:
        print(f"  ❌ Standard mode failed: {stderr}")
        return False
    
    # Test AI mode with mock token (should fail gracefully)
    success, stdout, stderr = run_command("python3.11 generate_workflow.py --analyze-only --openai-token 'mock-token'")
    if success or "AI enhancement enabled" in stdout:
        print("  ✅ AI enhancement mode tested successfully (graceful fallback)")
        return True
    else:
        print(f"  ❌ AI enhancement mode failed: {stderr}")
        return False

def test_backend_syntax():
    """Test backend Python syntax."""
    print("\n🐍 Testing backend Python syntax...")
    
    success, stdout, stderr = run_command("cd backend && python3.11 -m py_compile main.py")
    if success:
        print("  ✅ Backend Python syntax is valid")
        return True
    else:
        print(f"  ❌ Backend Python syntax error: {stderr}")
        return False

def main():
    """Run all tests."""
    print("🧪 QR Generator Demo - Verification Tests")
    print("=" * 50)
    
    tests = [
        test_files_exist,
        test_docker_compose_syntax,
        test_terraform_syntax,
        test_ai_generator,
        test_backend_syntax
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"  ⚠️  Test failed but continuing...")
        except Exception as e:
            print(f"  ❌ Test error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your QR Generator demo is ready!")
        print("\n📋 Next Steps:")
        print("1. Configure AWS credentials: aws configure")
        print("2. Set up GitHub secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
        print("3. Test locally: docker-compose up -d")
        print("4. Deploy to AWS: cd terraform && terraform apply")
        print("5. Push to GitHub to trigger CI/CD pipeline")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())