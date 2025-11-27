from google.generativeai import client, types
import numpy as np
import datetime

# -----------------------
# Tool functions
# -----------------------

def check_protocol(params):
    issues = []
    if not params.get("ethics_id"):
        issues.append("Ethics approval ID missing.")
    if params.get("sample_size", 0) < 30:
        issues.append("Sample size too small for statistical significance.")
    if not params.get("inclusion_criteria"):
        issues.append("Inclusion criteria not defined.")

    return {
        "issues": issues,
        "suggestions": ["Add ethics ID", "Increase sample size", "Define missing criteria"]
    }


def detect_anomaly(params):
    data = np.array(params["measurements"])
    mean = data.mean()
    std = data.std()
    anomalies = [x for x in data if abs(x-mean) > 2*std]

    return {"anomalies": anomalies}


def schedule_event(params):
    # Pseudo scheduling logic
    event_id = "EVT-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "event_id": event_id,
        "status": "Scheduled",
        "title": params["title"],
        "date": params["date"]
    }


# Map tools
tools = {
    "check_protocol": check_protocol,
    "detect_anomaly": detect_anomaly,
    "schedule_event": schedule_event
}


# -----------------------
# Gemini Agent
# -----------------------

def run_agent(user_prompt):

    client.configure(api_key="YOUR_GEMINI_API_KEY")

    agent = types.GenerativeModel(
        model="gemini-1.5-pro",
        tools=tools
    )

    response = agent.generate_content(user_prompt)
    return response.text


# -----------------------
# Test Agent
# -----------------------

if __name__ == "__main__":
    prompt = """
    Validate this experiment:
    Study title: Neural Response in Diabetic Patients
    Sample size: 12
    Inclusion: adults 25–50
    Exclusion: pregnant patients
    Ethics ID: 
    """

    print(run_agent(prompt))
