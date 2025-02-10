import os
import zipfile
import shutil
from pathlib import Path
import cv2
import numpy as np
import subprocess

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

def make_video(input_dir, out_path):
    """
    Create a video from a sequence of PNG images in the input directory
    
    Args:
        input_dir (str): Directory containing PNG images
        output_dir (str): Directory to save the output video
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of PNG files and sort them
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    image_files.sort()  # This will sort numerically due to the zero-padding
    
    if not image_files:
        print(f"No PNG files found in {input_dir}")
        return
        
    # Read first image to get dimensions
    first_image = cv2.imread(os.path.join(input_dir, image_files[0]))
    height, width = first_image.shape[:2]
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 30.0, (width, height))
    
    # Write each image to video
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)
    
    # Release the video writer
    out.release()
    print(f"Video saved to {out_path}")

def compress_video(input_path, output_path, width=480):
    """
    Compress video using ffmpeg with reduced resolution and bitrate
    
    Args:
        input_path (str): Path to input video
        output_path (str): Path to save compressed video
        width (int): Target width in pixels (height will scale proportionally)
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # FFmpeg command to compress video
    # -vf scale=width:-2 maintains aspect ratio
    # -crf 28 is compression quality (23 is default, higher = more compression)
    # -preset medium balances compression speed and quality
    cmd = [
        'ffmpeg', '-i', input_path,
        '-vf', f'scale={width}:-2',
        '-c:v', 'libx264',
        '-crf', '28',
        '-preset', 'medium',
        '-y',  # Overwrite output file if exists
        output_path
    ]
    
    subprocess.run(cmd)
    
    # Remove original file after successful compression
    if os.path.exists(output_path):
        os.remove(input_path)
        print(f"Compressed video saved to: {output_path}")

# Example usage
if __name__ == "__main__":

    folder_list = ['indoor_train', 'outdoor_train']
    output_dir = 'vis'

    os.makedirs(output_dir, exist_ok=True)
    
    for folder in folder_list:
        sub_folder_list = os.listdir(folder)
        sub_folder_list = sorted(sub_folder_list)
        # map them to aa, ab, ac, ad, ...
        for i, sub_folder in enumerate(sub_folder_list):
            new_name = number_to_letters(i + 1)
            _input_dir = os.path.join(folder, sub_folder, 'clean_uint8')
            _output_dir = os.path.join(output_dir, folder, new_name)
            _preview_path = os.path.join(_output_dir, 'preview.mp4')
            _compressed_path = os.path.join(_output_dir, 'preview_compressed.mp4')
            
            os.makedirs(_output_dir, exist_ok=True)
            
            # Create original video first
            make_video(_input_dir, _preview_path)
            
            # Compress the video
            compress_video(_preview_path, _compressed_path, width=480)
    

