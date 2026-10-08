"""
Local file storage + validation for resume uploads.

"""

import io
import os
import uuid
import zipfile
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
RESUME_DIR = UPLOAD_DIR / "resumes"
RESUME_DIR.mkdir(parents=True, exist_ok=True)

MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5 MB

# The first bytes of a real file ("magic bytes") for each allowed extension.
# We check these because the extension and Content-Type are set by the
# client and can be faked.
SIGNATURES = {
    ".pdf": [b"%PDF-"],
    ".doc": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"],
    ".docx": [b"PK\x03\x04"],
}


def read_and_validate_resume(file: UploadFile) -> tuple[bytes, str, str]:
    """Returns (content, extension, clean_original_filename) or raises HTTPException."""
    original_name = os.path.basename(file.filename or "")
    ext = os.path.splitext(original_name)[1].lower()

    if ext not in SIGNATURES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only PDF, DOC and DOCX files are allowed")

    # Read at most MAX+1 bytes, so a huge upload can't fill our memory
    content = file.file.read(MAX_RESUME_SIZE + 1)
    if len(content) > MAX_RESUME_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail="File too large (maximum 5 MB)")
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    if not any(content.startswith(sig) for sig in SIGNATURES[ext]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File content does not match its extension")

    # A .docx is a zip archive, so any zip file would pass the check above.
    # Make sure it really contains a Word document.
    if ext == ".docx":
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                if "word/document.xml" not in z.namelist():
                    raise zipfile.BadZipFile
        except zipfile.BadZipFile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid DOCX file")

    return content, ext, original_name


def save_resume_file(content: bytes, ext: str) -> str:
    """Saves under a random name and returns the path relative to UPLOAD_DIR."""
    stored_name = f"{uuid.uuid4().hex}{ext}"
    (RESUME_DIR / stored_name).write_bytes(content)
    return f"resumes/{stored_name}"


def resolve_path(relative_path: str) -> Path:
    path = (UPLOAD_DIR / relative_path).resolve()
    if not path.is_relative_to(UPLOAD_DIR.resolve()):
        raise ValueError("Invalid file path")
    return path


def delete_file(relative_path: str) -> None:
    try:
        resolve_path(relative_path).unlink(missing_ok=True)
    except ValueError:
        pass