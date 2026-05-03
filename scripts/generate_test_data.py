import pandas as pd
import pandavro as pdv
import os
import json

assets_dir = "tests/assets"

def ensure_assets_exist():
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # Define explicit Avro schema for nested data
    avro_schema = {
        "type": "record",
        "name": "EmployeeRecord",
        "fields": [
            {"name": "emp_id", "type": "int"},
            {"name": "project", "type": "string"},
            {
                "name": "details",
                "type": {
                    "type": "record",
                    "name": "DetailsRecord",
                    "fields": [
                        {"name": "dept", "type": "string"},
                        {"name": "site", "type": "string"}
                    ]
                }
            }
        ]
    }

    # Data matching the explicit schema
    df_avro = pd.DataFrame({
        'emp_id': [101, 102],
        'project': ['UniversalParser', 'AI-Integration'],
        'details': [
            {'dept': 'Engineering', 'site': 'Gurgaon'}, 
            {'dept': 'R&D', 'site': 'Remote'}
        ]
    })
    
    avro_path = os.path.join(assets_dir, "test.avro")
    # Pass the explicit schema here to bypass inference bugs
    pdv.to_avro(avro_path, df_avro, schema=avro_schema)
    print(f"✅ Generated: {avro_path}")

    # JSON Asset
    json_data = [{"id": 1, "name": "Arshdeep", "role": "Developer"}]
    with open(os.path.join(assets_dir, "test.json"), "w") as f:
        json.dump(json_data, f)
    print(f"✅ Generated: tests/assets/test.json")

if __name__ == "__main__":
    ensure_assets_exist()