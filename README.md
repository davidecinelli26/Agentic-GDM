# Agentic-GDM: Explainable Multi-Agent Group Decision Making

## Overview

**Agentic-GDM** is an advanced Multi-Agent System (MAS) built with Microsoft AutoGen and powered by Large Language Models (LLaMA-3 via Groq). It simulates a Group Decision Making (GDM) scenario where four autonomous agents—representing users with distinct, conflicting preferences—negotiate to select a Point of Interest (POI) to visit in Granada, Spain.

Moving beyond standard text-based LLM chats, this project implements a **Hybrid Neuro-Symbolic approach**. It forces agents to maintain and output an internal cognitive state (Utility Tracking) during negotiations. This enables a mathematical evaluation of the group's consensus and allows an Explainable AI (XAI) observer to generate highly accurate **Contrastive Explanations** rather than relying on post-hoc text rationalization.

## Key Features

* **Persona-Driven Agents**: Four specialized LLM agents (`Culture Enthusiast`, `Foodie`, `Party Goer`, `Budget Traveler`) designed to negotiate based on strict internal constraints.
* **Internal State & Utility Tracking**: Agents communicate strictly via structured JSON. While they exchange natural language "spoken messages", they secretly track their evolving utility scores (1-10) for each POI, exposing their internal reasoning to the system.
* **Mathematical Consensus Evaluation (GDM)**: Uses the **Ordered Weighted Averaging (OWA)** operator to calculate a pessimistic/fair global consensus score (0 to 1). It mathematically detects whether the group achieved a true compromise or if a dominant agent forced a decision, risking group conflict.
* **Advanced XAI Module**: An independent XAI Analyst reads the time-series of the agents' internal utility states (not just their chat history) to generate a **Contrastive Explanation** (e.g., *"Why did the group choose X instead of Y?"*), pinpointing exactly whose utility shifted and who drove the consensus.

## Technologies Used

* **Framework**: [Microsoft AutoGen](https://microsoft.github.io/autogen/)
* **LLM Provider**: [Groq](https://groq.com/) (using `llama-3.3-70b-versatile` for ultra-fast, high-reasoning inference)
* **Language**: Python 3.11.8

## Project Structure

```text
Agentic-GDM/
│
├── data/
│   └── granada_pois.json       # Dataset of Points of Interest in Granada
│
├── src/
│   ├── agents.py               # Agent definitions & JSON formatting instructions
│   ├── consensus_eval.py       # Math module for OWA consensus calculation
│   └── XAI_explainer.py        # LLM-based analyst for contrastive explanations
│
├── main.py                     # Main orchestrator script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules (excludes .env, .cache, etc.)
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/davidecinelli26/Agentic-GDM.git
cd Agentic-GDM
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up Environment Variables:**
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

To run the full simulation (Negotiation -> Consensus Evaluation -> XAI Report), simply execute:

```bash
python main.py
```

### What to Expect in the Console:

1. **Negotiation Phase:** You will see the agents communicating in JSON format, exposing both their hidden utility scores and their public spoken messages.
2. **GDM Module:** The system will parse the final decision and calculate the mathematical consensus using OWA weights.
3. **XAI Report:** The Explainer agent will output a final JSON explaining the group's dynamic, who compromised, and why the final POI was chosen over the alternatives based on the utility shifts.