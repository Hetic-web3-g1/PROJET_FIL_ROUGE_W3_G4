import magic
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

from src.database.s3_engine import s3_client


def check_mimetype(file: UploadFile, file_type: str) -> tuple[str, str]:
    """
    Check if the mimetype is supported.

    Args:
        file (UploadFile): The file to upload.
        file_type (str): The type of the file.

    Raises:
        HTTPException: No file type
        HTTPException: Major type not supported
        HTTPException: Minor type not supported

    Returns:
        tuple: The major and minor type of the file.
    """
    conversion_file_types = {
        "image": "image",
        "video": "video",
        "partition": "application",
        "subtitle": "text",
    }

    supported_file_types = {
        "image": ["jpg", "jpeg", "png", "svg"],
        "video": ["mp4"],
        "application": ["pdf", "x-subrip"],
        "text": ["vtt"],
    }

    mime_type = file.content_type

    if mime_type is None:
        raise HTTPException(status_code=400, detail="No file type not supported")

    major_type, minor_type = mime_type.split("/")

    if major_type not in conversion_file_types[file_type]:
        raise HTTPException(
            status_code=400, detail="File type not supported for this specific file."
        )

    if major_type not in supported_file_types:
        raise HTTPException(status_code=400, detail="File type not supported")

    if minor_type not in supported_file_types[major_type]:
        raise HTTPException(status_code=400, detail="File type not supported")

    return major_type, minor_type


def file_validation(file: UploadFile, file_type: str) -> tuple[str, str]:
    """
    Validate the file.

    Args:
        file (UploadFile): The file to upload.
        file_type (str): The type of the file.

    Raises:
        HTTPException: No file provided
        HTTPException: Invalide file object
        HTTPException: File cursor position not at the start of the file.
        HTTPException: Empty File
        HTTPException: File too large.

    Returns:
        tuple: The major and minor type of the file.
    """
    KB = 1000
    MB = KB * KB

    # if major_type not in supported_file_types:
    # raise HTTPException(status_code=400, detail="File type not supported")

    # if minor_type not in supported_file_types[major_type]:
    #     raise HTTPException(status_code=400, detail="File type not supported")

    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.file is None:
        raise HTTPException(status_code=400, detail="Invalid file object")

    if file.file.tell() != 0:
        raise HTTPException(
            status_code=400,
            detail="File cursor position must be at the start of the file",
        )

    size = file.size

    if size is None:
        raise HTTPException(status_code=400, detail="File size is not available")

    if size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    if size > 10000 * MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large, max size is 10MB, this file weight {size} bytes",
        )

    type = check_mimetype(file, file_type)
    return type


def create_presigned_url(bucket_name, object_key, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    Args:
        bucket_name (string): Name of the S3 bucket
        object_name (string): S3 object name
        expiration (int): Time in seconds for the presigned URL to remain valid

    Returns:
        dict: Presigned URL as string. If error, returns None.
    """
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        return {"error": str(e)}

    return response
