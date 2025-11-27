# AntiGravity-Clinical-assays-agent
Clinical experiments automation agentic agent using google anti gravity

User → Frontend UI → Gemini Agent → Tools
                        |-> Tool 1: Protocol Checker (Python)
                        |-> Tool 2: Sample Logger (Firestore/Sheets)
                        |-> Tool 3: Anomaly Detector (Python ML)
                        |-> Tool 4: Calendar Scheduler (Google Calendar API)
clinical-agentic-ai/
    ├── README.md
    ├── agent.py
    ├── tools/
    │      ├── protocol_checker.py
    │      ├── anomaly_detector.py
    │      ├── scheduler.py
    ├── prompts/
    │      ├── system_prompt.txt
    │      ├── tool_instructions.txt
    ├── examples/
    │      ├── protocol_validation_example.md
    │      ├── anomaly_example.md
    ├── requirements.txt
# Agentic AI for Clinical Experiment Automation (Google Gemini)

This project automates clinical research workflows using Google Gemini 1.5 and Agentic AI capabilities.  
It performs:

✔ Protocol validation  
✔ Sample tracking (datastore or Sheets)  
✔ Anomaly detection  
✔ Scheduling in Google Calendar  
✔ Research lifecycle automation  

## Features
- Multi-tool agent architecture
- Uses Gemini model for reasoning
- Python tools for compliance & automation
- JSON structured outputs
- Ready for deployment on Cloud Run or Firebase

## Run locally

pip install -r requirements.txt

export GEMINI_API_KEY="your_key"

python agent.py

## Folder Structure
See project tree in repository root.

