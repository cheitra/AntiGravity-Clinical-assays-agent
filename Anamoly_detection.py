import statistics

def detect_anomalies(data, threshold=2):
    """
    Detects outliers in a list of numerical data using Z-score.
    
    Args:
        data (list): List of numerical values.
        threshold (float): Z-score threshold for identifying outliers.
        
    Returns:
        list: A list of indices where outliers were found.
    """
    if not data or len(data) < 2:
        return []
    
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)
    
    if stdev == 0:
        return []
        
    outliers = []
    for i, value in enumerate(data):
        z_score = (value - mean) / stdev
        if abs(z_score) > threshold:
            outliers.append(i)
            
    return outliers

if __name__ == "__main__":
    # Test with dummy data
    test_data = [10, 12, 12, 13, 12, 11, 100, 12]
    print(f"Data: {test_data}")
    outlier_indices = detect_anomalies(test_data)
    print(f"Outlier indices: {outlier_indices}")
    print(f"Outlier values: {[test_data[i] for i in outlier_indices]}")
