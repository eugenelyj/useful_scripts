import os
import zipfile
import shutil
from pathlib import Path

def create_selective_zip(input_dir, output_dir, keys):
    """
    Create a zip file containing only specified keys from the input directory
    
    Args:
        input_dir (str): Path to input directory
        output_dir (str): Path to output directory
        keys (list): List of folder/file names to include in zip
    """

    os.makedirs(output_dir, exist_ok=True)
    
    # Create zip file
    for key in keys:
        zip_path = os.path.join(output_dir, f"{key}.zip")
        key_path = os.path.join(input_dir, key)
            

        # Check if path exists
        if not os.path.exists(key_path):
            print(f"Warning: {key} not found in {input_dir}")
            continue

        if not os.path.isdir(key_path):
            # copy the file
            save_path = os.path.join(output_dir, key)
            shutil.copy(key_path, save_path)
            os.system(f'rm {zip_path}')
            print(f"Copy file: {save_path}")
            continue


        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
               
            # If it's a directory, walk through it and add all files
            for root, _, files in os.walk(key_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate path relative to input_dir for zip structure
                    arcname = os.path.relpath(file_path, input_dir)
                    zipf.write(file_path, arcname)
        
            print(f"Created zip file: {zip_path}")

def number_to_letters(n):
    """
    Convert a number to two-letter combination (1 -> aa, 2 -> ab, ..., 27 -> ba, etc.)
    
    Args:
        n (int): Number between 1 and 100
        
    Returns:
        str: Two-letter combination
    """
    # Subtract 1 to make it 0-based for easier calculation
    n = n - 1
    
    # First letter (a-z) is determined by integer division by 26
    first = chr(ord('a') + (n // 26))
    
    # Second letter (a-z) is determined by remainder
    second = chr(ord('a') + (n % 26))
    
    return first + second

# Example usage
if __name__ == "__main__":

    folder_list = ['indoor_train', 'outdoor_train']
    output_dir = 'individual'

    # Keys to include in zip
    keys_to_zip = [
        "poses.npz",
        "metadata.json",
    ]

    os.makedirs(output_dir, exist_ok=True)
    
    for folder in folder_list:
        sub_folder_list = os.listdir(folder)
        sub_folder_list = sorted(sub_folder_list)
        # map them to aa, ab, ac, ad, ...
        for i, sub_folder in enumerate(sub_folder_list):
            new_name = number_to_letters(i + 1)
            _input_dir = os.path.join(folder, sub_folder)
            _output_dir = os.path.join(output_dir, folder, new_name)
    
            create_selective_zip(_input_dir, _output_dir, keys_to_zip)

