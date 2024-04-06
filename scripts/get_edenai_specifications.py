import os
from pathlib import Path
from context import split_openapi_spec

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / 'data' / 'eden'
    openapi_file = data_dir / 'Eden AI.json'
    output_dir = data_dir / 'specifications'

    os.makedirs(output_dir, exist_ok=True)
    split_openapi_spec(openapi_file, output_dir)
