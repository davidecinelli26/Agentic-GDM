import json
import autogen
import os
from dotenv import load_dotenv

from src.agents import cultural_agent, foodie_agent, party_agent, budget_agent, llm_config
from src.consensus_eval import calculate_group_consensus
from src.XAI_explainer import generate_explanation

# 1. DATA LOADING
base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, 'data', 'granada_pois.json')

try:
    with open(data_path, 'r') as file:
        pois = json.load(file)
except FileNotFoundError:
    print(f"Error: Could not find the dataset at {data_path}")
    exit()

# Format the POIs into a readable string for the LLM prompt
poi_list = "\n".join([f"- {poi['name']} ({poi['category']}, Cost: ${poi['cost']}): {poi['description']}" for poi in pois])

# 2. MULTI-AGENT GROUP CHAT SETUP
# Define the participants and the management logic
groupchat = autogen.GroupChat(
    agents=[cultural_agent, foodie_agent, party_agent, budget_agent],
    messages=[],
    max_round=8  # Allowance for multiple negotiation turns
)

# The Manager acts as the moderator to decide the speaking order
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 3. INTERFACE SETUP
# The User Proxy represents the system starting the discussion (autonomous mode)
user_proxy = autogen.UserProxyAgent(
    name="System",
    human_input_mode="NEVER",
    code_execution_config=False
)

# 4. INITIALIZATION PROMPT
# Setting the context: 4 friends with different profiles deciding on a trip in Granada
prompt = f"""
Hello everyone! We need to agree on ONE single activity to do today in Granada.
Here are our options from the dataset:
{poi_list}

Please discuss, negotiate based on your preferences, and reach a final consensus. 
Important: Your last message MUST clearly state the chosen activity name.
"""

# 5. EXECUTE NEGOTIATION
print("--- [SIMULATION] GRANADA TRIP NEGOTIATION STARTED ---")
user_proxy.initiate_chat(manager, message=prompt)

# --- POST-NEGOTIATION ANALYSIS ---

# 6. OUTPUT PARSING
# Retrieve the full chat history to identify the final decision
history = groupchat.messages
if not history:
    print("Error: No messages generated during negotiation.")
    exit()

final_msg = history[-1]['content'].lower()

# Map the chat result to a category for the mathematical GDM module
chosen_category = "Culture" # Default fallback
if any(word in final_msg for word in ["tapas", "food", "eat"]):
    chosen_category = "Food"
elif any(word in final_msg for word in ["club", "nightlife", "west", "dancing"]):
    chosen_category = "Nightlife"
elif any(word in final_msg for word in ["viewpoint", "mirador", "sunset", "nicolas"]):
    chosen_category = "Viewpoint"
elif "alhambra" in final_msg:
    chosen_category = "Culture"

print(f"\n[SYSTEM] Decision identified: {chosen_category}")

# 7. GDM MODULE (Mathematical Evaluation)
# Calculate group satisfaction using the OWA (Ordered Weighted Averaging) operator
calculate_group_consensus(chosen_category)

# 8. XAI MODULE (Qualitative Evaluation)
# Use an LLM-based analyst to explain 'why' and 'how' the consensus was reached
generate_explanation(history)

print("\n--- [SIMULATION] PROCESS COMPLETED SUCCESSFULLY ---")