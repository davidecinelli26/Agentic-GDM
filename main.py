import json
import autogen
from src.agents import cultural_agent, foodie_agent, party_agent, budget_agent, llm_config

# 1. Load the Granada Points of Interest (POIs) dataset
with open('data/granada_pois.json', 'r') as file:
    pois = json.load(file)

# Format the POIs into a readable string for the prompt
poi_list = "\n".join([f"- {poi['name']} ({poi['category']}, Cost: ${poi['cost']}): {poi['description']}" for poi in pois])

# 2. Setup the Group Chat
groupchat = autogen.GroupChat(
    agents=[cultural_agent, foodie_agent, party_agent, budget_agent],
    messages=[],
    max_round=6  # Limit the conversation to 6 messages to reach consensus quickly
)

# The Manager orchestrates the conversation, deciding who speaks next based on context
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 3. Create a User Proxy (This acts as the "Narrator" or the system starting the chat)
user_proxy = autogen.UserProxyAgent(
    name="System",
    human_input_mode="NEVER",
    code_execution_config=False
)

# 4. The Initial Prompt that kicks off the negotiation
prompt = f"""
Hello everyone! We need to agree on ONE single activity to do today in Granada.
Here are our options from the dataset:
{poi_list}

Please discuss with each other, negotiate based on your personal preferences, and reach a consensus on which single activity we should choose.
"""

# 5. Start the simulation
print("--- GRANADA TRIP NEGOTIATION STARTED ---")
user_proxy.initiate_chat(manager, message=prompt)