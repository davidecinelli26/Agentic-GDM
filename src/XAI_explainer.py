import json
import autogen
from src.agents import llm_config

def generate_explanation(chat_history):
    """
    Acts as an Explainable AI (XAI) observer. 
    It reads the negotiation history and explains the reasoning behind the final decision.
    """
    print("\n[XAI MODULE] Analyzing the negotiation to generate a contrastive explanation...")
    
    # We create a specific agent whose only job is to analyze and explain
    explainer_agent = autogen.AssistantAgent(
        name="XAI_Explainer",
        system_message="""You are an expert XAI analyst. 
        Read the JSON states of the multi-agent negotiation. 
        Generate a Contrastive Explanation focusing on the utility scores.
        
        Output ONLY a valid JSON object with:
        - "final_decision": The chosen POI.
        - "contrastive_explanation": "Why they chose X instead of Y, referencing specific changes in utility scores."
        - "decisive_agent": Who drove the consensus.
        
        Do not add markdown formatting.""",
        llm_config=llm_config
    )

    # We format the chat history so the LLM can read it easily
    formatted_history = ""
    for msg in chat_history:
        sender = msg.get('name', 'Agent')
        content = msg.get('content', '')
        formatted_history += f"--- {sender}'s State ---\n{content}\n"
        
    prompt = f"Negotiation States Timeline:\n\n{formatted_history}\n\nPlease provide the JSON XAI explanation."

    # We use a trick to get a direct answer without starting a full conversation
    reply = explainer_agent.generate_reply(messages=[{"role": "user", "content": prompt}])
    
    print("\n=> ADVANCED XAI REPORT:")
    print(reply)
    
    # Attempt to parse it as JSON to ensure it's valid
    try:
        json_data = json.loads(reply)
        return json_data
    except json.JSONDecodeError:
        print("[WARNING] The XAI model did not return a perfect JSON. Returning raw text.")
        return reply