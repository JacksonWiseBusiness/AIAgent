import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

    except Exception as e:
        return (f"Error: listing files: {e}")

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
