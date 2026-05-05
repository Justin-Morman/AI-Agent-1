import os
import subprocess
import config
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns the output",
    parameters=types.Schema(
        required=["file_path", "args"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to pass to the Python file (optional)",
            ),
        },
    ),
)
def run_python_file(working_directory, file_path, args=None):
    try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            # Will be True or False
            valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

            if os.path.isfile(target_file) is False:
                return(f'Error: "{file_path}" does not exist or is not a regular file')
            if not valid_file_path:
                return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
            if not target_file.endswith('.py'):
                return(f'Error: "{file_path}" is not a Python file')
            
            result = subprocess.run(['python', target_file] + (args or []), capture_output=True, timeout=config.TIMEOUT, text=True)
            heading = ''
            if result.returncode != 0:
                heading = "Process exited with code X"
            if result.stdout and result.stderr is None:
                heading = "No output produced"
            return(f"{heading}\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}")
    except Exception as e:
        return(f"Error: executing Python file: {e}")
               