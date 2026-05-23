import os
import json
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# Load environment variables
load_dotenv()

# Initialize Cerebras Client
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

# Load SOP Data
def load_sop():
    with open("data/sop.json", "r") as file:
        return file.read()

SOP_DATA = load_sop()

# System Prompt defining the AI's persona, rules, and stages
SYSTEM_PROMPT = f"""
You are an AI customer support assistant for Bloom Aesthetics Clinic. 
Your tone is professional, warm, and helpful, suited for a high-end SMB clinic.

Here is your Standard Operating Procedure (SOP) data:
{SOP_DATA}

You must strictly adhere to the following 4 stages:

STAGE 1: FAQ Answering
- Answer questions ONLY using the provided SOP data.
- Do NOT hallucinate or guess. If the answer is not in the SOP, acknowledge the gap and escalate.

STAGE 2: Lead Qualification
- If the user asks to book or inquire about a specific treatment, seamlessly ask 1-2 qualification questions from the SOP to understand their needs. Do not interrogate; be conversational.

STAGE 3: Escalation Detection
- You MUST escalate and hand off to a human agent immediately if you detect:
  1. A complaint or angry sentiment.
  2. A medical question (we cannot give medical advice).
  3. Pricing negotiation.
  4. Out-of-scope questions not covered in the SOP.
- If escalating, clearly state: "[ESCALATION TRIGGERED] - Reason: <insert reason>" and politely inform the customer someone will be in touch.

STAGE 4: Conversation Summary
- Do not trigger this yourself. The system will prompt you for a summary when the chat ends.
"""

def generate_summary(conversation_history):
    """Handles Stage 4: Generating the structured end-of-session summary."""
    print("\n--- Generating Conversation Summary ---")
    summary_prompt = {
        "role": "user",
        "content": "The session has ended. Please provide a clean, structured summary containing: 1. Customer Intent, 2. Key Details Collected, 3. SOP Gaps Identified (if any), 4. Recommended Next Action."
    }
    
    messages = conversation_history + [summary_prompt]
    
    response = client.chat.completions.create(
        model="llama3.1-8b", # Cerebras supported model
        messages=messages,
        temperature=0.2
    )
    print(response.choices[0].message.content)

def main():
    print("Welcome to Closira AI Agent Simulator! (Type 'quit' or 'exit' to end the chat and see the summary)")
    print("-" * 80)
    
    # Initialize conversation with the system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input("\nCustomer: ")
        
        if user_input.lower() in ['quit', 'exit']:
            generate_summary(messages)
            break
            
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="llama3.1-8b", # Cerebras supported model
                messages=messages,
                temperature=0.2 # Low temperature for factual consistency with SOP
            )
            
            ai_reply = response.choices[0].message.content
            print(f"\nAI: {ai_reply}")
            
            messages.append({"role": "assistant", "content": ai_reply})
            
            # If the AI triggered an escalation, stop the chat automatically
            if "[ESCALATION TRIGGERED]" in ai_reply:
                print("\n*** Handoff to human agent initiated. Ending chat. ***")
                generate_summary(messages)
                break
                
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()