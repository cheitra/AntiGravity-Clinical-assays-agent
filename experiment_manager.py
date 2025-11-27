import json
import csv
import os
import argparse
from anomaly_detection import detect_anomalies
from datetime import datetime

def approve_protocol(protocol_path, approval_number):
    if not os.path.exists(protocol_path):
        return "Protocol file not found."
    
    try:
        with open(protocol_path, 'r') as f:
            protocol = json.load(f)
            
        if "ethics_approval" not in protocol:
            protocol["ethics_approval"] = {}
            
        protocol["ethics_approval"]["approved"] = True
        protocol["ethics_approval"]["approval_number"] = approval_number
        protocol["ethics_approval"]["date"] = datetime.now().strftime("%Y-%m-%d")
        
        with open(protocol_path, 'w') as f:
            json.dump(protocol, f, indent=2)
            
        return f"Protocol approved with number {approval_number}."
        
    except Exception as e:
        return f"Error approving protocol: {str(e)}"

def validate_protocol(protocol_path):
    issues = []
    if not os.path.exists(protocol_path):
        return ["Protocol file not found."]
    
    try:
        with open(protocol_path, 'r') as f:
            protocol = json.load(f)
            
        required_fields = ["experiment_id", "title", "investigator", "sample_size", "inclusion_criteria", "exclusion_criteria", "ethics_approval"]
        for field in required_fields:
            if field not in protocol:
                issues.append(f"Missing field: {field}")
            elif not protocol[field]:
                issues.append(f"Field is empty: {field}")
                
        if "ethics_approval" in protocol:
            ethics = protocol["ethics_approval"]
            if not ethics.get("approved"):
                issues.append("Ethics approval is pending or not approved.")
            if not ethics.get("approval_number"):
                issues.append("Missing ethics approval number.")
                
    except json.JSONDecodeError:
        issues.append("Invalid JSON format in protocol file.")
    except Exception as e:
        issues.append(f"Error reading protocol: {str(e)}")
        
    return issues

def check_data_anomalies(log_path):
    issues = []
    if not os.path.exists(log_path):
        return ["Experiment log file not found."]
        
    try:
        data_columns = {"systolic_bp": [], "diastolic_bp": [], "heart_rate": [], "temperature": []}
        rows = []
        with open(log_path, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                rows.append(row)
                for col in data_columns:
                    if col in row and row[col]:
                        try:
                            data_columns[col].append(float(row[col]))
                        except ValueError:
                            pass # Ignore non-numeric
                            
        for col, values in data_columns.items():
            outliers = detect_anomalies(values)
            if outliers:
                for idx in outliers:
                    issues.append(f"Anomaly detected in {col} for row {idx+1} (Subject: {rows[idx].get('subject_id', 'Unknown')})")
                    
    except Exception as e:
        issues.append(f"Error analyzing data log: {str(e)}")
        
    return issues

def main():
    parser = argparse.ArgumentParser(description="Clinical Experiment Manager")
    parser.add_argument("--protocol", default="protocol_template.json", help="Path to protocol JSON file")
    parser.add_argument("--log", default="experiment_log_template.csv", help="Path to experiment log CSV file")
    parser.add_argument("--approve", action="store_true", help="Approve the protocol")
    parser.add_argument("--approval-number", help="Ethics approval number (required with --approve)")
    args = parser.parse_args()
    
    if args.approve:
        if not args.approval_number:
            print("Error: --approval-number is required when using --approve")
            return
        result = approve_protocol(args.protocol, args.approval_number)
        print(result)
        return
    
    response = {
        "status": "success",
        "issues": [],
        "next_steps": [],
        "actions": []
    }
    
    # 1. Validate Protocol
    protocol_issues = validate_protocol(args.protocol)
    if protocol_issues:
        response["status"] = "attention_required"
        response["issues"].extend(protocol_issues)
        response["next_steps"].append("Review and fix protocol issues.")
    else:
        response["actions"].append("Protocol validated successfully.")
        
    # 2. Check Data
    data_issues = check_data_anomalies(args.log)
    if data_issues:
        response["status"] = "attention_required"
        response["issues"].extend(data_issues)
        response["next_steps"].append("Investigate data anomalies.")
    else:
        response["actions"].append("Data log checked. No anomalies found.")
        
    print(json.dumps(response, indent=1))

if __name__ == "__main__":
    main()
