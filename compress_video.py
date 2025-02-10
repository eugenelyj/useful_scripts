import os
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


def compress_video(input_path, output_path, width=480, target_fps=20):
    """
    Compress video using ffmpeg with reduced resolution, bitrate, and adjusted fps
    
    Args:
        input_path (str): Path to input video
        output_path (str): Path to save compressed video
        width (int): Target width in pixels (height will scale proportionally)
        target_fps (int): Target frames per second (duration will adjust to keep same frame count)
    """
    import subprocess
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # FFmpeg command to compress video and adjust speed
    cmd = [
        'ffmpeg', '-i', input_path,
        '-ss', '0',
        '-t', '20',
        '-vf', f'scale={width}:-2,setpts=30/{target_fps}*PTS',  # Adjust video duration based on fps change
        '-c:v', 'libx264',
        # '-r', f'{target_fps}',
        '-crf', '27',
        '-preset', 'medium',
        '-y',
        output_path
    ]
    
    subprocess.run(cmd)
    
    # Remove original file after successful compression
    if os.path.exists(output_path):
        print(f"Compressed video saved to: {output_path}")

# Update the main script to include compression
if __name__ == "__main__":
    # folder_list = ['indoor_people', 'indoor_tour', 'outdoor']
    # output_dir = 'vis'
    # save_dir = 'vis_compressed'
    
    # os.makedirs(output_dir, exist_ok=True)
    
    # for folder in folder_list:
    #     sub_folder_list = os.listdir(f'{output_dir}/{folder}')
    #     sub_folder_list = sorted(sub_folder_list)
        
    #     for i, sub_folder in enumerate(sub_folder_list):
    #         new_name = number_to_letters(i + 1)
    #         _output_dir = os.path.join(output_dir, folder, new_name)
    #         _preview_path = os.path.join(_output_dir, 'preview.mp4')
    #         basename = f'{folder}_{new_name}'
    #         _compressed_path = os.path.join(save_dir, f'{basename}.mp4')
            
    #         os.makedirs(_output_dir, exist_ok=True)
            
    #         # Compress the video
    #         compress_video(_preview_path, _compressed_path, width=480, target_fps=20)

    for key in ['rgb', 'depth', 'flow', 'event', 'rainbow_particle']:
        input_path = f'data/teaser_results/{key}.mp4'
        output_path = f'data/teaser_results/{key}_compressed.mp4'
        compress_video(input_path, output_path, width=480, target_fps=30)

