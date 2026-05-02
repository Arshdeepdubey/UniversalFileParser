import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

# Ensure the directory exists
assets_dir = "tests/assets"
os.makedirs(assets_dir, exist_ok=True)

# 1. Create JSON Test Data
json_data = [
    {"id": 1, "name": "Arshdeep", "role": "Developer", "metadata": {"status": "active"}},
    {"id": 2, "name": "Gemini", "role": "AI", "metadata": {"status": "learning"}}
]
with open(f"{assets_dir}/test.json", "w") as f:
    json.dump(json_data, f)

# 2. Create Test Data (Complex Schema)
df = pd.DataFrame({
    'emp_id': [101, 102],
    'project': ['UniversalParser', 'AI-Integration'],
    'details': [{'dept': 'Engineering', 'site': 'Gurgaon'}, {'dept': 'R&D', 'site': 'Remote'}]
})

# Save as Parquet (always works)
table = pa.Table.from_pandas(df)
pq.write_table(table, f"{assets_dir}/test.parquet")

# Try to save as Avro (optional if avro-python3 is available)
try:
    import avro.datafile
    import avro.io
    from avro.schema import parse as parse_schema
    
    # Define Avro schema
    avro_schema = {
        "type": "record",
        "name": "EmployeeRecord",
        "fields": [
            {"name": "emp_id", "type": "int"},
            {"name": "project", "type": "string"},
            {"name": "details", "type": {"type": "map", "values": "string"}}
        ]
    }
    
    schema = parse_schema(json.dumps(avro_schema))
    records = df.to_dict('records')
    
    with avro.datafile.DataFileWriter(open(f"{assets_dir}/test.avro", "wb"), avro.io.DatumWriter(), schema) as writer:
        for record in records:
            writer.append(record)
    
    print(f"✅ Test assets generated in {assets_dir} (including Avro)")
except (ImportError, ModuleNotFoundError):
    print(f"✅ Test assets generated in {assets_dir} (Avro skipped - avro-python3 not installed)")