import json
import autogen
from src.agents import llm_config

def generate_explanation(chat_history):
    """
    Acts as an Explainable AI (XAI) observer. 
    It reads the negotiation history and explains the reasoning behind the final decision.
    """
    print("\n[XAI MODULE] Analyzing the negotiation to generate an explanation...")
    
    # We create a specific agent whose only job is to analyze and explain
    explainer_agent = autogen.AssistantAgent(
        name="XAI_Explainer",
        system_message="""You are an Explainable AI (XAI) analyst. 
        Your task is to analyze the following group chat negotiation and explain how the final decision was reached.
        You must output ONLY a valid JSON object with the exact following keys:
        - "final_decision": The specific POI or category they agreed upon.
        - "reasoning": A brief explanation of why this was chosen.
        - "compromises": Who had to compromise their initial preferences and why.
        
        Do not add any markdown formatting (like ```json), just return the raw JSON string.""",
        llm_config=llm_config
    )

    # We format the chat history so the LLM can read it easily
    formatted_history = ""
    for msg in chat_history:
        # We handle cases where the message might not have a 'name' explicitly
        sender = msg.get('name', 'Agent')
        content = msg.get('content', '')
        formatted_history += f"{sender}: {content}\n"
        
    prompt = f"Here is the negotiation chat history:\n\n{formatted_history}\n\nPlease provide the JSON explanation."

    # We use a trick to get a direct answer without starting a full conversation
    reply = explainer_agent.generate_reply(messages=[{"role": "user", "content": prompt}])
    
    print("\n=> XAI EXPLANATION REPORT:")
    print(reply)
    
    # Attempt to parse it as JSON to ensure it's valid
    try:
        json_data = json.loads(reply)
        return json_data
    except json.JSONDecodeError:
        print("[WARNING] The XAI model did not return a perfect JSON. Returning raw text.")
        return reply

if __name__ == "__main__":
    mock_history = [
        {"name": "Sophia", "content": "I want to go to the Alhambra!"},
        {"name": "Marco", "content": "I am hungry, let's go eat Tapas."},
        {"name": "Sophia", "content": "Ok, if we eat tapas near the Alhambra, I accept."}
    ]
    generate_explanation(mock_history)