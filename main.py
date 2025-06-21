from reflection_agent import ReflectionAgent
import os
from datetime import datetime

print("=== Reflection-Agent ===\n")

api_url = "http://127.0.0.1:1234/v1/"
model_name = "gemma-3-12b-it-qat"

agent = ReflectionAgent(api_url, model_name)
state_files = [f for f in os.listdir('.') if f.startswith('reflexion_state_') and f.endswith('.pkl')]

def generate_report(input):
    results = agent.process_reflection(input)
                
    print("\nGenerate final report...")
    report = agent.generate_report(input, results)
    
    filename = f"reflexion_analyse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nAnalysis completed! Report saved as: {filename}")

def main():
    if state_files:
        print("🔍 Incomplete analyses found:")
        for i, f in enumerate(state_files, 1):
            print(f"  {i}. {f}")
        
        choice = input(f"\nContinue analysis? (y/n)").strip().lower()
        
        if choice=='y':
            agent.state_file = state_files[-1]
            workbench = agent.load_state()
            if workbench:
                print(f"🔄 Continue analysis...")
                generate_report(workbench['user_input'])
                return
            else:
                print(f"Workbench corrupted, restarting...")

    # Start new analysis
    print("\nPlease enter your request or problem:")
    user_input = input().strip()

    language = agent.call_llm(f"Please return the language of the following text as a whole word:\n\"{user_input}\"")
    agent.language = language

    if not user_input:
        print("No input received. Exit...")
        return

    print("\nStart analysis...\n")

    try:
        results = agent.process_reflection(user_input)
        
        print("\nGenerating final report...")
        report = agent.generate_report(user_input, results)
        
        filename = f"reflexion_analyse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        if os.path.exists(agent.state_file):
            os.remove(agent.state_file)
            print("✓ Temporary status file deleted")
        
        print(f"\nAnalysis completed! Report saved as: {filename}")
        
    except KeyboardInterrupt:
        print(f"\n⏸ Analysis interrupted. Workbench has been saved.")
        print("Restart the script to continue.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Workbench has been saved. Try a restart.")

main()