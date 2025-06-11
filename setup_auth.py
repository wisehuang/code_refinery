#!/usr/bin/env python3
"""
Authentication Setup Script for Code Refinery

This script helps you set up authentication for the Code Refinery API.
"""

import os
import secrets
import string

def generate_secure_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def setup_auth():
    """Setup authentication configuration"""
    print("🔐 Code Refinery Authentication Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_path = "backend/.env"
    env_example_path = "backend/env.example"
    
    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            print(f"📋 Copying {env_example_path} to {env_path}")
            with open(env_example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
        else:
            print(f"❌ {env_example_path} not found. Creating new .env file.")
            with open(env_path, 'w') as f:
                f.write("# LLM API Keys\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("ANTHROPIC_API_KEY=your_anthropic_api_key_here\n")
                f.write("GOOGLE_API_KEY=your_google_api_key_here\n\n")
                f.write("# Authentication Settings\n")
                f.write("AUTH_ENABLED=true\n")
                f.write("API_TOKEN=your_secret_api_token_here\n")
    
    # Read current .env file
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    print("\n🔧 Authentication Configuration Options:")
    print("1. Generate a new secure API token")
    print("2. Set a custom API token")
    print("3. Disable authentication (development only)")
    print("4. Exit without changes")
    
    choice = input("\nSelect an option (1-4): ").strip()
    
    if choice == "1":
        # Generate secure token
        new_token = f"sk-refinery-{generate_secure_token(24)}"
        print(f"\n🔑 Generated secure token: {new_token}")
        
        # Update .env file
        lines = env_content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('API_TOKEN='):
                updated_lines.append(f'API_TOKEN={new_token}')
            elif line.startswith('AUTH_ENABLED='):
                updated_lines.append('AUTH_ENABLED=true')
            else:
                updated_lines.append(line)
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print(f"✅ Updated {env_path} with new token")
        print(f"\n📝 Next steps:")
        print(f"1. Add this to your frontend .env.local file:")
        print(f"   NEXT_PUBLIC_API_TOKEN={new_token}")
        print(f"2. Restart your backend server")
        print(f"3. Restart your frontend development server")
        
    elif choice == "2":
        # Custom token
        custom_token = input("\n🔑 Enter your custom API token: ").strip()
        
        if not custom_token:
            print("❌ Token cannot be empty")
            return
        
        # Update .env file
        lines = env_content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('API_TOKEN='):
                updated_lines.append(f'API_TOKEN={custom_token}')
            elif line.startswith('AUTH_ENABLED='):
                updated_lines.append('AUTH_ENABLED=true')
            else:
                updated_lines.append(line)
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print(f"✅ Updated {env_path} with custom token")
        print(f"\n📝 Next steps:")
        print(f"1. Add this to your frontend .env.local file:")
        print(f"   NEXT_PUBLIC_API_TOKEN={custom_token}")
        print(f"2. Restart your backend server")
        print(f"3. Restart your frontend development server")
        
    elif choice == "3":
        # Disable authentication
        lines = env_content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('AUTH_ENABLED='):
                updated_lines.append('AUTH_ENABLED=false')
            else:
                updated_lines.append(line)
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print(f"✅ Disabled authentication in {env_path}")
        print(f"⚠️  Warning: This should only be used for development!")
        print(f"\n📝 Next steps:")
        print(f"1. Remove NEXT_PUBLIC_API_TOKEN from your frontend .env.local file (if it exists)")
        print(f"2. Restart your backend server")
        print(f"3. Restart your frontend development server")
        
    elif choice == "4":
        print("👋 Exiting without changes")
        return
    
    else:
        print("❌ Invalid choice")
        return

def main():
    """Main function"""
    try:
        setup_auth()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")

if __name__ == "__main__":
    main() 