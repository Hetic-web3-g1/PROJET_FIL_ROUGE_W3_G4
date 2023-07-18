import magic
from fastapi import HTTPException, UploadFile
from botocore.exceptions import ClientError

from src.utils.s3.s3_engine import s3_client


# TODO give the url for a true validation of the file
def check_mimetype(file: UploadFile, file_type: str):
    """
    Check if the mimetype is supported.

    Args:
        file (UploadFile): The file to upload.

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
        "subtitle": "application",
    }

    supported_file_types = {
        "image": ["jpg", "jpeg", "png", "svg"],
        "video": ["mp4"],
        "application": ["pdf", "x-subrip"],
    }

    # Use python-magic to detect the file's actual MIME type based on its content
    mime_type = magic.from_buffer(file.file.read(1024), mime=True)
    file.file.seek(0)

    if mime_type is None:
        raise HTTPException(status_code=400, detail="No file type not supported")

    major_type, minor_type = mime_type.split("/")

    if major_type not in supported_file_types:
        raise HTTPException(status_code=400, detail="File type not supported")

    if conversion_file_types[file_type] != major_type:
        raise HTTPException(status_code=400, detail="File type not supported")

    if minor_type not in supported_file_types[major_type]:
        raise HTTPException(status_code=400, detail="File type not supported")

    return major_type, minor_type


def file_validation(file: UploadFile, file_type: str) -> tuple:
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

    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.file is None:
        raise HTTPException(status_code=400, detail="Invalid file object")

    if file.file.tell() != 0:
        raise HTTPException(
            status_code=400,
            detail="File cursor position must be at the start of the file",
        )

    size = file.file.seek(0, 2)  # Get the size of the file using seek()
    file.file.seek(0)  # Reset the file cursor to the start of the file

    if size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    if size > 10 * MB:
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
