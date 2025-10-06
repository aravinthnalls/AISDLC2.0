#!/usr/bin/env python3.11
"""
Demo script to showcase AI-enhanced workflow generation
"""

import os
import sys
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="AI-Enhanced Workflow Generator Demo")
    parser.add_argument("--openai-token", help="OpenAI API token for AI enhancement")
    args = parser.parse_args()
    
    print("🤖 AI-Enhanced Workflow Generator Demo")
    print("=" * 50)
    
    # Check if token was provided via command line
    provided_token = args.openai_token
    
    print("\n📋 Available modes:")
    print("1. Standard Mode (no AI)")
    print("2. AI-Enhanced Mode (requires OpenAI API token)")
    
    # Auto-select AI mode if token is provided
    if provided_token:
        print(f"\n🤖 Token provided - automatically selecting AI-Enhanced Mode")
        mode = "2"
    else:
        mode = input("\nSelect mode (1 or 2): ").strip()
    
    # Ask what to run
    print("\n📋 What would you like to do?")
    print("1. Analyze project only")
    print("2. Generate complete pipeline")
    
    action = input("Select action (1 or 2): ").strip()
    analyze_only = action == "1"
    
    if mode == "1":
        print(f"\n🔍 Running in Standard Mode {'(analysis only)' if analyze_only else '(full generation)'}...")
        cmd = f"python3.11 generate_workflow.py --verbose{' --analyze-only' if analyze_only else ''}"
        os.system(cmd)
    
    elif mode == "2":
        token = provided_token
        
        # Only ask for token if not provided via command line
        if not token:
            token = input("Enter your OpenAI API token (or press Enter to skip): ").strip()
        else:
            print(f"✅ Using provided OpenAI API token")
            
        if token:
            print(f"\n🧠 Running with AI Enhancement {'(analysis only)' if analyze_only else '(full generation)'}...")
            cmd = f"python3.11 generate_workflow.py --verbose --openai-token '{token}'{' --analyze-only' if analyze_only else ''}"
            os.system(cmd)
        else:
            print(f"⚠️ No token provided, running in standard mode {'(analysis only)' if analyze_only else '(full generation)'}...")
            cmd = f"python3.11 generate_workflow.py --verbose{' --analyze-only' if analyze_only else ''}"
            os.system(cmd)
    
    else:
        print("❌ Invalid selection")
        return
    
    print("\n✅ Demo completed!")
    print("\nTo use AI enhancement in your own projects:")
    print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Run: python generate_workflow.py --openai-token YOUR_TOKEN")
    print("3. Or set environment variable: export OPENAI_API_TOKEN=your_token")
    print("4. Or use this demo: python demo_ai_enhancement.py --openai-token YOUR_TOKEN")

if __name__ == "__main__":
    main()