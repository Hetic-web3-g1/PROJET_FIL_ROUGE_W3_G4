from fastapi import Response, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Union
import uuid, json, re

from src.utils.json_encoder import CustomJSONEncoder

def check_id(id: Union[str, int]):
    id_str = str(id)  # Convert id to a string
    if isinstance(id, str):
        # Check if the string matches the UUID format
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        if re.match(uuid_pattern, id, re.IGNORECASE):
            try:
                uuid.UUID(id)  # Validate the id as a UUID string
                return  # Return if the string is a valid UUID
            except ValueError:
                pass  # Proceed to integer validation if it's not a valid UUID
        try:
            int(id)  # Attempt to convert the id string to an integer
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID: Not a valid UUID or integer")        
        if int(id) < 0:
            raise HTTPException(status_code=400, detail="Invalid ID: Negative value")
    else:
        try:
            uuid.UUID(id_str)  # Validate the id as a UUID string
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID")

def get_route_response(response, code_success, code_error, error_message):
    if isinstance(response, list) and response:
        serialized_response = [item.dict() for item in response]  # Convert objects to dictionaries
        return JSONResponse(content=json.loads(json.dumps(serialized_response, cls=CustomJSONEncoder)), status_code=code_success)
    else:
        if response:
            serialized_response = response.dict()  # Convert object to dictionary
            return JSONResponse(content=json.loads(json.dumps(serialized_response, cls=CustomJSONEncoder)), status_code=code_success)
        else:
            return JSONResponse(content={"data": error_message}, status_code=code_error)

def route_response(response, code_success, code_error, success_message=None, error_message=None):
    if response is not None and response.get("status") == "success":
        if success_message is not None:
            return Response(content=json.dumps({"data": success_message}), status_code=code_success)
        else:
            return Response(content=json.dumps({"data": response}), status_code=code_success)
    else:
        if error_message is not None:
            return Response(content=json.dumps({"data": error_message}), status_code=code_error)
        else:
            return Response(content=json.dumps({"data": response}), status_code=code_error)