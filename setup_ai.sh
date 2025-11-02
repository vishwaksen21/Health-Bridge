#!/bin/bash
# Quick setup script for OpenAI API integration

echo "=================================="
echo "🤖 AI Integration Setup"
echo "=================================="
echo ""

# Check if OPENAI_API_KEY is already set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "No OpenAI API key detected."
    echo ""
    echo "To enable real AI responses, you need an OpenAI API key."
    echo ""
    echo "📋 Steps to get your API key:"
    echo "1. Go to: https://platform.openai.com/api/keys"
    echo "2. Sign up or log in to your OpenAI account"
    echo "3. Click 'Create new secret key'"
    echo "4. Copy the key (starts with 'sk_')"
    echo ""
    echo "❓ Do you have an OpenAI API key? (y/n)"
    read -r response
    
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo ""
        echo "Enter your OpenAI API key (starts with 'sk_'):"
        read -r api_key
        
        if [[ $api_key == sk_* ]]; then
            # Add to shell profile
            echo ""
            echo "Adding to your shell profile..."
            
            # Determine which shell profile to update
            if [ -f ~/.zshrc ]; then
                echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.zshrc
                echo "✅ Added to ~/.zshrc"
            elif [ -f ~/.bash_profile ]; then
                echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bash_profile
                echo "✅ Added to ~/.bash_profile"
            elif [ -f ~/.bashrc ]; then
                echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bashrc
                echo "✅ Added to ~/.bashrc"
            fi
            
            # Set for current session
            export OPENAI_API_KEY="$api_key"
            
            echo ""
            echo "🎉 API key configured!"
            echo ""
            echo "To use the new configuration:"
            echo "1. Restart your terminal or run: source ~/.zshrc"
            echo "2. Run: python main.py"
            echo ""
            echo "You'll now get real AI-generated health insights! 🚀"
        else
            echo "❌ Invalid API key format. Key should start with 'sk_'"
        fi
    else
        echo ""
        echo "No problem! The system works with local heuristic responses."
        echo "You can set up an API key anytime."
    fi
else
    echo "✅ OpenAI API key already configured!"
    echo "Key: ${OPENAI_API_KEY:0:20}...${OPENAI_API_KEY: -5}"
    echo ""
    echo "🚀 Real AI is ready! Run: python main.py"
fi

echo ""
echo "=================================="
echo "Alternative Options:"
echo "=================================="
echo ""
echo "1. GitHub Models (Free for GitHub users):"
echo "   - Set GITHUB_TOKEN environment variable"
echo ""
echo "2. Azure OpenAI (Enterprise):"
echo "   - Set AZURE_ENDPOINT and AZURE_API_KEY"
echo ""
echo "For more details, see: AI_INTEGRATION_SETUP.md"
