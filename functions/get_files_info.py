import os

def get_files_info(working_directory, directory="."):
    try:
    
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if os.path.isdir(target_dir) is False:
            return(f'Error: "{directory}" is not a directory')
        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        result = []
        for file in os.listdir(target_dir):
            if os.path.isfile(os.path.join(target_dir, file)):
                is_dir = False
            else:
                is_dir = True
            
            result.append(f"- {file}: file_size = {os.path.getsize(os.path.join(target_dir, file))} bytes, is_dir={is_dir}")
        return(f"Result for {directory} directory: \n {"\n".join(result)}")
    except Exception as e:
        return(f'Error: {e}')