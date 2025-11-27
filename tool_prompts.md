Tool: check_protocol
Purpose: Validate clinical research protocol
Input fields:
- study_title
- inclusion_criteria
- exclusion_criteria
- sample_size
- ethics_id

Return issues list + corrected suggestions.
Tool: update_log
Purpose: Create or update sample log in Firestore or Google Sheets
Input: sample_id, status, timestamp
Tool: detect_anomaly
Purpose: Detect outliers in experiment readings.
Input: list of measurements
Tool: schedule_event
Purpose: Schedule experiment session in Google Calendar.
Input: title, date, duration, participants[]
