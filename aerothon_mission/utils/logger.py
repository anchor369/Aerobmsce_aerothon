# utils/logger.py

import json
import os

def log_mission_result(object_counts, disaster_location, log_dir="mission_log", filename="output.json"):
    """
    Save mission summary including detected objects and disaster status.
    """
    os.makedirs(log_dir, exist_ok=True)

    result = {
        "objects": object_counts,
        "disaster_location": disaster_location,
        "status": "Payload Dropped" if disaster_location else "No Disaster Found"
    }

    filepath = os.path.join(log_dir, filename)
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2)

    print(f"📝 Mission log saved to {filepath}")
