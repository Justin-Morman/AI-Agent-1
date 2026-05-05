import os
import subprocess
import config
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
               