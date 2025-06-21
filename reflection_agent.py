#!/usr/bin/env python3
import requests
import re
import os
import pickle
from datetime import datetime
from typing import Dict, Any, Optional
from prompts import prompts

step_prints = [
"Step 1: Free reflection...",
"Step 2: Extracting the core problem...",
"Step 3: Generating clarification questions...",
"Step 4: Creating priority profile...",
"Step 5: Aspect exploration...",
"Step 6: Extracting arguments...",
"Step 7: Categorizing arguments...",
"Step 8: Identifying stakeholders...",
"Step 9: Analyzing time horizons...",
"Step 10: Uncovering basic assumptions...",
"Step 11: Final analysis...",
"Step 12: Brainstorming options...",
"Step 13: Evaluating options...",
"Step 14: Final recommendation..."
]

step_workbench_keys = [
'free_reflection',
'core_problem',
'user_answers',
'priority_profile',
'aspect_exploration',
'raw_arguments',
'categorized_arguments',
'stakeholders',
'time_horizons',
'assumptions',
'final_analysis',
'options',
'rated_options',
'recommendations'
]

step_input_keys = [
['user_input'],
['free_reflection'],
['core_problem'],
['user_answers'],
['free_reflection','user_input'],
['aspect_exploration','user_input'],
['raw_arguments'],
['user_input','aspect_exploration'],
['categorized_arguments'],
['free_reflection','user_input','user_answers'],
['categorized_arguments','priority_profile'],
['final_analysis','assumptions','aspect_exploration'],
['options','priority_profile'],
['final_analysis','rated_options','time_horizons']
]

class ReflectionAgent:
    def __init__(self, api_url, model_name, api_key=None):
        self.api_url = api_url.rstrip('/')
        self.model_name = model_name
        self.headers = {'Content-Type': 'application/json'}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
        
        # State management
        self.state_file = None
        self.current_step = 1
        self.max_retries = 3
        self.base_timeout = 300
        self.language = 'english'
        
        self.prompts = prompts

    def save_state(self, state: Dict[str, Any]):
        """Saves the current workbench to a file"""
        with open(self.state_file, 'wb') as f:
            pickle.dump(state, f)
        print(f"✓ State saved (step {self.current_step})")

    def load_state(self) -> Optional[Dict[str, Any]]:
        """Loads the saved workbench, if available"""
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"⚠ Warning: Could not load state: {e}")
        return None

    def call_llm(self, prompt: str) -> str:
        """Calls the LLM with retry logic and customizable timeouts"""
        for attempt in range(self.max_retries):
            try:
                timeout = self.base_timeout * (2 ** attempt)
                
                if attempt > 0:
                    enhanced_prompt = f"{prompt}\n\nWichtig: Bitte beschränke deine Antwort auf maximal 500 Wörter."
                else:
                    enhanced_prompt = prompt
                
                payload = {
                    "model": self.model_name,
                    "messages": [{"role": "system","content":f"You always and only answer in {self.language}"},
                                 {"role": "user", "content": enhanced_prompt}],
                    "temperature": 0.37,
                    "max_tokens": 4096
                }
                
                print(f"  → LLM call (attempt {attempt + 1}/{self.max_retries}, Timeout: {timeout}s)")
                
                response = requests.post(
                    f"{self.api_url}/chat/completions", 
                    headers=self.headers, 
                    json=payload, 
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
                
            except requests.exceptions.Timeout:
                print(f"  ⚠ Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    print(f"Trying again")
                else:
                    raise Exception(f"LLM call failed after {self.max_retries} attempts (timeout)")
                    
            except requests.exceptions.RequestException as e:
                print(f"  ⚠ Request error during attempt {attempt + 1}: {e}")
                if not attempt < self.max_retries - 1:
                    raise Exception(f"LLM call failed after {self.max_retries} attempts (timeout)")

    def extract_section(self, text, marker):
        pattern = f"### {marker} ###(.*?)(?=### |$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else text.strip()

    def get_user_answers(self, questions):
        print("\n" + "="*50)
        print("PLEASE ANSWER THE FOLLOWING QUESTIONS:")
        print("="*50)
        print(questions)
        print("\n" + "="*50)
        
        answers = []
        question_lines = [line.strip() for line in questions.split('\n') 
                         if line.strip() and any(char.isdigit() for char in line[:5])]
        
        for i, question in enumerate(question_lines, 1):
            print(f"\nQuestion {i}: {question}")
            answer = input("Answer: ").strip()
            answers.append(f"{i}. {answer}")
        
        return "\n".join(answers)

    def process_reflection(self, user_input: str) -> Dict[str, Any]:
        """Main processing logic with state management"""
        
        self.state_file = f"reflexion_workbench.pkl"
        
        # Attempts to load previous state
        workbench = self.load_state()
        if workbench:
            print(f"🔄 Continuing analysis at step {workbench['current_step']}...")
            self.current_step = workbench['current_step']
        else:
            print("🆕 Start new analysis...")
            workbench = {
                'user_input': user_input,
                'current_step': 1,
                'language':self.language
                }
            
        try:
            for step in range(max(1,self.current_step),15):
                print(step_prints[step-1])
                if step!=3:
                    workbench[step_workbench_keys[step-1]] = self.call_llm(
                        self.prompts[step]
                        .format(*[workbench[k] for k in step_input_keys[step-1]]))
                if step==3 and not 'user_answers' in workbench:
                    questions = self.call_llm(self.prompts[3].format(workbench['core_problem']))
                    workbench['user_answers'] = self.get_user_answers(questions)
                self.current_step = step+1
                workbench.update({'current_step': self.current_step})
                self.save_state(workbench)
        
        except Exception as e:
            print(f"\n❌ Error in step {self.current_step}: {e}")
            print(f"💾 State has been saved. Restart the script to continue.")
            raise
   
        return workbench

    def generate_report(self, user_input, workbench):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""# Reflection analysis
**Created on:** {timestamp}

---

## Original request
{user_input}

---

{workbench['free_reflection']}

---

{workbench['priority_profile']}

---

{workbench['aspect_exploration']}

---

{workbench['categorized_arguments']}

---

{workbench['stakeholders']}

---

{workbench['time_horizons']}

---

{workbench['assumptions']}

---

{workbench['final_analysis']}

---

{workbench['recommendations']}

---
"""