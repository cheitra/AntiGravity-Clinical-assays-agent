from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
import csv
from werkzeug.utils import secure_filename
from experiment_manager import validate_protocol, check_data_anomalies

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    if 'protocol' not in request.files or 'log' not in request.files:
        return redirect(request.url)
        
    protocol_file = request.files['protocol']
    log_file = request.files['log']
    
    if protocol_file.filename == '' or log_file.filename == '':
        return redirect(request.url)
        
    if protocol_file and log_file:
        protocol_filename = secure_filename(protocol_file.filename)
        log_filename = secure_filename(log_file.filename)
        
        protocol_path = os.path.join(app.config['UPLOAD_FOLDER'], protocol_filename)
        log_path = os.path.join(app.config['UPLOAD_FOLDER'], log_filename)
        
        protocol_file.save(protocol_path)
        log_file.save(log_path)
        
        # Run validation logic
        response = {
            "status": "success",
            "issues": [],
            "next_steps": [],
            "actions": []
        }
        
        # 1. Validate Protocol
        protocol_issues = validate_protocol(protocol_path)
        if protocol_issues:
            response["status"] = "attention_required"
            response["issues"].extend(protocol_issues)
            response["next_steps"].append("Review and fix protocol issues.")
        else:
            response["actions"].append("Protocol validated successfully.")
            
        # 2. Check Data
        data_issues = check_data_anomalies(log_path)
        if data_issues:
            response["status"] = "attention_required"
            response["issues"].extend(data_issues)
            response["next_steps"].append("Investigate data anomalies.")
        else:
            response["actions"].append("Data log checked. No anomalies found.")
            
        return render_template('report.html', report=response)

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('.', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
