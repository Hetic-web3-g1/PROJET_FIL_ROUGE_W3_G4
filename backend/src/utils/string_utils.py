import unicodedata
import re


def sanitize_string(input_string: str) -> str:
    # Remove accents and special symbols from input_string
    sanitized_string = (
        unicodedata.normalize("NFKD", input_string)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    # Remove any remaining special symbols using regex
    sanitized_string = re.sub(r"[^\w\s]", "", sanitized_string)

    return sanitized_string


def sanitizeAndLowerCase(input_string: str) -> str:
    # Lowercase the input_string
    sanitized_string = sanitize_string(input_string)
    return sanitized_string.lower()
