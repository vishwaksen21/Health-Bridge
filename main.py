# main.py
from src.ai_assistant import load_knowledge_base, generate_comprehensive_answer, format_answer_for_display
import json
import sys

def main():
    print("🏥 Welcome to Dual Recommendation Health Assistant!")
    print("   (Herbal Remedies + Pharmaceutical Medications)")
    print("=" * 65)
    
    # Load knowledge base once
    print("📚 Loading medical knowledge base...")
    knowledge = load_knowledge_base()
    print("✅ Knowledge base loaded!")
    print("💊 Pharmaceutical database available!\n")
    
    # Check for LLM availability
    import os
    has_llm_token = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT"))
    if has_llm_token:
        print("✅ AI LLM enabled (GitHub Models)\n")
        use_ai = True
    else:
        print("ℹ️  AI LLM not configured (Optional - system works without it)")
        print("   To enable AI insights:")
        print("   1. Get token: https://github.com/settings/tokens/new")
        print("   2. Run: export GITHUB_TOKEN='your_actual_token'")
        print("   3. Restart: python main.py\n")
        use_ai = False
    
    print("=" * 65 + "\n")
    print("💡 TIP: For best results, enter your symptoms WITHOUT spelling mistakes")
    print("   (e.g., 'asthma', 'fever', 'headache', not 'asthma', 'fevr', 'headeache')\n")
    print("=" * 65 + "\n")
    
    # Check if running in interactive or pipe mode
    is_interactive = sys.stdin.isatty()
    
    if not is_interactive:
        # Pipe mode: read from stdin
        for line in sys.stdin:
            user_input = line.strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                break
            if not user_input:
                continue
            
            print(f"🧍 Analyzing: {user_input}\n")
            response = generate_comprehensive_answer(
                user_input, 
                knowledge, 
                use_ai=use_ai,
                include_drugs=True  # Include drug recommendations
            )
            print(format_answer_for_display(response))
            print("=" * 65 + "\n")
    else:
        # Interactive mode
        while True:
            try:
                user_input = input("🧍 Enter your problem or symptoms (or 'quit' to exit): ").strip()
            except EOFError:
                break
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Thank you for using the Dual Recommendation Assistant!")
                break
            
            if not user_input:
                print("⚠️ Please enter your symptoms.\n")
                continue
            
            print("\n🔍 Analyzing your symptoms...\n")
            
            # Generate comprehensive answer with BOTH herbal and drug recommendations
            response = generate_comprehensive_answer(
                user_input, 
                knowledge, 
                use_ai=use_ai,
                include_drugs=True  # Get both herbal and pharmaceutical recommendations
            )
            
            # Display formatted answer
            print(format_answer_for_display(response))
            
            # Optional: Show JSON for debugging
            show_json = input("\n📊 Show detailed JSON response? (y/n): ").strip().lower()
            if show_json == 'y':
                print(json.dumps(response, indent=2))
            
            print("\n" + "=" * 65 + "\n")

if __name__ == "__main__":
    main()
