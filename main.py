import os
import re

def process_directory(root_dir):
    knowledge_data = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            knowledge_data.extend(append_filename(filepath))
            if filepath.endswith('.c') or filepath.endswith('.h'):
                knowledge_data.extend(process_c_file(filepath))
            elif filepath.endswith('.inc'):
                knowledge_data.extend(process_inc_file(filepath))
    return knowledge_data

def append_filename(filepath):
    # Split the filepath into parts
    path_parts = filepath.split(os.sep)
    
    # Check if the path has enough parts to include one directory level
    if len(path_parts) > 1:
        # Reconstruct the desired part of the path (one directory level up + filename)
        partial_path = os.path.join(path_parts[-2], path_parts[-1])
    else:
        # If not, just use the filename
        partial_path = path_parts[-1]
    
    return [f"File Name: {partial_path}"]

def process_c_file(filepath):
    extracted_data = []
    with open(filepath, 'r') as file:
        content = file.read()
        extracted_data.extend(extract_function_definitions(content))
        extracted_data.extend(extract_struct_definitions(content))
        extracted_data.extend(extract_enum_definitions(content))
        extracted_data.extend(extract_includes(content))
    return extracted_data

def extract_function_definitions(content):
    pattern = r"\b(?:static\s+)?\w+\s+\w+\([^)]*\)"
    return ["Function: " + func for func in re.findall(pattern, content)]

def extract_struct_definitions(content):
    pattern = r"(?ms)struct\s+\w+\s*\{.*?\};"
    return ["Struct: " + struct for struct in re.findall(pattern, content)]

def extract_enum_definitions(content):
    pattern = r"enum\s+\{[^}]*\}"
    return ["Enum: " + enum for enum in re.findall(pattern, content)]

def extract_includes(content):
    pattern = r"#include\s+\"[^\"]+\""
    return [include for include in re.findall(pattern, content)]

def process_inc_file(filepath):
    extracted_data = []
    with open(filepath, 'r') as file:
        numLines = 0
        for line in file:
            line = line.strip()
            if line.endswith('::'):
                extracted_data.append(f"{numLines} lines.")
                extracted_data.append(parse_script(line))
                numLines = 0
            numLines = numLines + 1
            # Add more conditions as needed for other patterns in .inc files
    return extracted_data

def parse_set_command(line):
    # Example: .set LOCALID_MOM, 1 becomes "Local ID for MOM is set to 1."
    parts = line.split(',')
    if len(parts) >= 2:
        return f"{parts[0]} set to {parts[1].strip()}"
    return line

def parse_script(line):
    # Example: EventScript_Name:: becomes "Event script named 'EventScript_Name'."
    script_name = line.split('::')[0]
    return f"Script named '{script_name}'."

def main():
    # Ask the user to enter the relative path to the directory
    root_dir = input("Enter the relative path to your directory: ")

    # Process the directory and generate knowledge data
    knowledge_data = process_directory(root_dir)
    
    # Extract the last part of the path as the directory name
    directory_name = os.path.basename(os.path.normpath(root_dir))
    
     # Name the knowledge file after the root directory
    knowledge_filename = f"{directory_name}_knowledge.txt"

    # Write the knowledge data to a file
    with open(knowledge_filename, 'w') as file:
        for item in knowledge_data:
            file.write("%s\n" % item)

    # Inform the user that the process is complete
    print("Knowledge file created successfully.")

if __name__ == "__main__":
    main()
