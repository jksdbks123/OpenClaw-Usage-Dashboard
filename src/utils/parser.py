import json
import os
import glob
from datetime import datetime

def parse_usage_from_jsonl(file_path):
    total_input = 0
    total_output = 0
    sessions_data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    # Check for message type and usage field
                    if data.get('type') == 'message' and 'usage' in data:
                        usage = data['usage']
                        total_input += usage.get('input', 0)
                        total_output += usage.get('output', 0)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return {
        "file": os.path.basename(file_path),
        "input_tokens": total_input,
        "output_tokens": total_output,
        "last_updated": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    }

def get_all_usage_data(sessions_dir):
    pattern = os.path.join(sessions_dir, "*.jsonl")
    files = glob.glob(pattern)
    all_stats = [parse_usage_from_jsonl(f) for f in files]
    return all_stats

if __name__ == "__main__":
    # Test path
    sessions_path = os.path.expanduser("~/.openclaw/agents/main/sessions/")
    stats = get_all_usage_data(sessions_path)
    print(json.dumps(stats, indent=2))
