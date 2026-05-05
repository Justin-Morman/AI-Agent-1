import os
import config
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file and returns the result",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING, description="File path to write to, relative to the working directory"),
            "content": types.Schema(type=types.Type.STRING, description="Content to write to the file"),
        },
    ),
)
def write_file(working_directory, file_path, content):
     try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
            # Will be True or False
            valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
            
            if os.path.isdir(target_file) is True:
                return(f'Error: Cannot write to "{file_path}" as it is a directory')
            
            if not valid_file_path:
                return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
            
            
            
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, 'w') as f:
                f.write(content)
            return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
     except Exception as e:
        return(f'Error: {e}')