from pydantic import BaseModel, ValidationError

def validate_astra_contract(data: dict, model: BaseModel) -> bool:
    """
    Validates a data dictionary against a Pydantic model.

    Args:
        data: The dictionary to validate.
        model: The Pydantic model to validate against.

    Returns:
        True if the data is valid, False otherwise.
    """
    try:
        model(**data)
        return True
    except ValidationError as e:
        print(f"Astra contract validation failed: {e}")
        return False
