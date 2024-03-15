import json
import os

def split_openapi_schema(openapi_schema):
    global_schema = json.loads(openapi_schema)

    domains = {}

    for path, details in global_schema["paths"].items():
        domain = path.split("/")[1]

        if domain not in domains:
            domains[domain] = {
                "openapi": global_schema.get("openapi", "3.0.0"),
                "info": global_schema.get("info", {}),
                "paths": {},
                "servers": global_schema.get("servers", []),
                "components": global_schema.get("components", {}),
            }

        domains[domain]["paths"][path] = details

    return domains


if __name__ == "__main__":
    eden_openapi_schema = open("../data/eden/Eden AI.json", encoding='utf-8').read()
    schemas = split_openapi_schema(eden_openapi_schema)

    os.makedirs("../data/eden/sub_domains", exist_ok=True)

    for sub_domain, schema in schemas.items():
        with open(f"../data/eden/sub_domains/{sub_domain}.json", "w") as f:
            f.write(json.dumps(schema, indent=2))
