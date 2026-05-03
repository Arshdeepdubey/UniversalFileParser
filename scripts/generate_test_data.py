import pandas as pd
import pandavro as pdv
import os
import json

# Define the target directory
assets_dir = "tests/assets"

def ensure_assets_exist():
    """Creates the assets directory and generates test files."""
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created directory: {assets_dir}")

    # 1. Generate the Complex Avro File (Critical for Phase 4 tests)
    # The 'details' column is a dictionary that the Cleaner will flatten
    df_avro = pd.DataFrame({
        'emp_id': [101, 102],
        'project': ['UniversalParser', 'AI-Integration'],
        'details': [
            {'dept': 'Engineering', 'site': 'Gurgaon'}, 
            {'dept': 'R&D', 'site': 'Remote'}
        ]
    })
    
    avro_path = os.path.join(assets_dir, "test.avro")
    pdv.to_avro(avro_path, df_avro)
    print(f"✅ Generated: {avro_path}")

    # 2. Generate a JSON File (for general testing)
    json_data = [
        {"id": 1, "name": "Arshdeep", "role": "Developer"},
        {"id": 2, "name": "Gemini", "role": "AI"}
    ]
    json_path = os.path.join(assets_dir, "test.json")
    with open(json_path, "w") as f:
        json.dump(json_data, f)
    print(f"✅ Generated: {json_path}")

if __name__ == "__main__":
    ensure_assets_exist()