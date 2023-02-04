from typing import List


def create_api_doc_params(place_in: str, description: str, schema: dict) -> dict:
    return {
        'in': f'{place_in}',
        'description': description,
        'schema': schema
    }


def create_schema(schema_type: str, properties: dict, required_fields: List[str]) -> dict:
    return {
        'type': schema_type,
        'properties': properties,
        'required': required_fields
    }


def create_schema_properties(properties: dict) -> dict:
    """
    Create schema properties
    :parameter properties: dict with Key: data-type and Value: list of fields
        {'string': [email, password]}
    """
    schema_prop = {}
    for data_type, fields in properties.items():
        props = {field: {'type': f'{data_type}'} for field in properties.get(data_type)}
        schema_prop.update(props)

    return schema_prop
