# main.py
"""
Dual Recommendation Health Assistant - CLI Interface
Combines herbal remedies and pharmaceutical recommendations with optional AI insights.
"""

import json
import sys
import os
import time
from typing import Optional

# Try importing the AI assistant module with graceful error handling
try:
    from src.ai_assistant import (
        load_knowledge_base,
        generate_comprehensive_answer,
        format_answer_for_display
    )
    # QUICK WIN #4: Import safety checks module
    from src.safety_checks import (
        check_emergency_keywords,
        check_confidence_threshold,
        add_medical_disclaimer
    )
    AI_MODULE_OK = True
except ImportError as e:
    print(f"⚠️  WARNING: Could not import AI module: {e}")
    print("   Checking if src/__init__.py exists...")
    if not os.path.exists("src/__init__.py"):
        print("   ❌ src/__init__.py is missing. Creating it...")
        try:
            os.makedirs("src", exist_ok=True)
            with open("src/__init__.py", "w", encoding="utf-8") as f:
                f.write("# AI Assistant Module\n")
            print("   ✅ src/__init__.py created.")
        except Exception as ex:
            print(f"   ❌ Could not create src/__init__.py: {ex}")
    sys.exit(1)
except Exception as e:
    print(f"❌ FATAL: Unexpected error loading AI module: {e}")
    sys.exit(1)


def progress_spinner(duration: float = 1.5) -> None:
    """Display a simple progress spinner during analysis."""
    spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r   {spinner_chars[idx % len(spinner_chars)]} ")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write("\r   ✓ Complete!\n")


def check_ai_module() -> Optional[str]:
    """Check if src/__init__.py exists; return warning if missing."""
    if not os.path.exists("src/__init__.py"):
        return "⚠️  WARNING: src/__init__.py is missing. The module may not work properly."
    return None


def main():
    """Main CLI entry point."""
    try:
        # Display welcome banner
        print("\n🏥 Welcome to Dual Recommendation Health Assistant!")
        print("   (Herbal Remedies + Pharmaceutical Medications)")
        print("=" * 65)
        
        # Check for missing module file
        module_warning = check_ai_module()
        if module_warning:
            print(f"{module_warning}\n")
        
        # Load knowledge base with error handling
        print("📚 Loading medical knowledge base...")
        try:
            knowledge = load_knowledge_base()
            print("✅ Knowledge base loaded successfully!")
        except Exception as e:
            print(f"❌ ERROR loading knowledge base: {e}")
            print("   Attempting to continue with fallback data...")
            try:
                # Attempt fallback if load fails
                from src.ai_assistant import load_knowledge_base as fallback_load
                knowledge = fallback_load()
            except Exception as e2:
                print(f"❌ FATAL: Could not load any knowledge base: {e2}")
                sys.exit(1)
        
        print("💊 Pharmaceutical database available!")
        
        # Check for LLM availability
        has_llm_token = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT") or os.environ.get("OPENAI_API_KEY"))
        if has_llm_token:
            print("✅ AI LLM enabled (GitHub Models / OpenAI)\n")
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
            try:
                for line in sys.stdin:
                    user_input = line.strip()
                    if user_input.lower() in ["quit", "exit", "q"]:
                        break
                    if not user_input:
                        continue
                    
                    # QUICK WIN #4A: Emergency Detection - Check in pipe mode too
                    emergency_check = check_emergency_keywords(user_input)
                    if emergency_check['is_emergency']:
                        print(emergency_check['message'])
                        continue  # Skip to next input in pipe mode
                    
                    print(f"🧍 Analyzing: {user_input}")
                    progress_spinner(1.0)
                    
                    try:
                        response = generate_comprehensive_answer(
                            user_input, 
                            knowledge, 
                            use_ai=use_ai,
                            include_drugs=True
                        )
                        if use_ai and response.get("ai_insights"):
                            print("✅ AI insights generated successfully!\n")
                        print(format_answer_for_display(response))
                        
                        # QUICK WIN #4B: Low Confidence Warning
                        predicted_confidence = response.get('confidence', 1.0)
                        confidence_check = check_confidence_threshold(predicted_confidence)
                        if confidence_check['show_warning']:
                            print(confidence_check['message'])
                        
                        # Add medical disclaimer
                        print(add_medical_disclaimer())
                    except Exception as e:
                        print(f"❌ Error processing symptoms: {e}")
                        print("   Continuing with next input...\n")
                    
                    print("=" * 65 + "\n")
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Thank you for using the Dual Recommendation Assistant!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error in pipe mode: {e}")
                sys.exit(1)
        else:
            # Interactive mode
            try:
                while True:
                    try:
                        user_input = input("🧍 Enter your problem or symptoms (or 'quit' to exit): ").strip()
                    except EOFError:
                        print("\n👋 Thank you for using the Dual Recommendation Assistant!")
                        break
                    except KeyboardInterrupt:
                        print("\n\n👋 Interrupted. Thank you for using the Dual Recommendation Assistant!")
                        sys.exit(0)
                    
                    if not user_input:
                        print("⚠️  Please enter your symptoms.\n")
                        continue
                    
                    if user_input.lower() in ["quit", "exit", "q"]:
                        print("\n👋 Thank you for using the Dual Recommendation Assistant!")
                        break
                    
                    # QUICK WIN #4A: Emergency Detection - Check BEFORE processing
                    emergency_check = check_emergency_keywords(user_input)
                    if emergency_check['is_emergency']:
                        print(emergency_check['message'])
                        print("\n⚠️  Exiting application. Please call emergency services.\n")
                        sys.exit(1)
                    
                    print("\n🔍 Analyzing your symptoms...")
                    progress_spinner(1.5)
                    print()
                    
                    try:
                        # Generate comprehensive answer
                        response = generate_comprehensive_answer(
                            user_input, 
                            knowledge, 
                            use_ai=use_ai,
                            include_drugs=True
                        )
                        
                        if use_ai and response.get("ai_insights"):
                            print("✅ AI insights generated successfully!\n")
                        
                        # Display formatted answer
                        print(format_answer_for_display(response))
                        
                        # QUICK WIN #4B: Low Confidence Warning - Check AFTER prediction
                        predicted_confidence = response.get('confidence', 1.0)
                        confidence_check = check_confidence_threshold(predicted_confidence)
                        if confidence_check['show_warning']:
                            print(confidence_check['message'])
                        
                        # Add medical disclaimer
                        print(add_medical_disclaimer())
                        
                        # Optional: Show JSON for debugging
                        try:
                            show_json = input("\n📊 Show detailed JSON response? (y/n): ").strip().lower()
                            if show_json in ['y', 'yes']:
                                print(json.dumps(response, indent=2, ensure_ascii=False))
                        except KeyboardInterrupt:
                            pass
                        except Exception:
                            pass
                        
                        print("\n" + "=" * 65 + "\n")
                    
                    except Exception as e:
                        print(f"❌ Error processing symptoms: {e}")
                        print("   Please try again with a different symptom description.\n")
                        print("=" * 65 + "\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Thank you for using the Dual Recommendation Assistant!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()