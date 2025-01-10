from datasets import load_dataset, Dataset
from huggingface_hub import HfApi, login
import os
import glob
import argparse

def login_to_hf(token):
    """Login to Hugging Face using token"""
    login(token=token)

def get_relative_path(base_path, full_path):
    """Get relative path from base path"""
    return os.path.relpath(full_path, base_path)

def list_folders(base_path):
    """List all folders under the given path"""
    folders = []
    for root, dirs, files in os.walk(base_path):
        if dirs:  # if there are directories in this level
            folders.extend([os.path.join(root, d) for d in dirs])
    return folders if folders else [base_path]

def upload_to_hf(folder_path, repo_id):
    """Upload folder to Hugging Face"""
    for folder in list_folders(folder_path):
        try:
            api = HfApi()
            api.upload_folder(
                folder_path=folder,
                path_in_repo=folder,
                repo_id=repo_id,
                repo_type="dataset"
            )
            print(f"Successfully uploaded {folder_path} to {repo_id}")
        except Exception as e:
            print(f"Error uploading dataset: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Upload folder to Hugging Face dataset")
    parser.add_argument("--token", required=True, help="Hugging Face API token")
    parser.add_argument("--repo_id", required=True, help="Repository ID (format: username/dataset-name)")
    parser.add_argument("--base_path", required=True, help="Base path containing folders to upload")
    
    args = parser.parse_args()
    
    # Login to Hugging Face
    login_to_hf(args.token)
    
    # Upload to Hugging Face
    upload_to_hf(args.base_path, args.repo_id)

if __name__ == "__main__":
    main()
