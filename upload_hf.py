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
    flist = []
    for f in os.listdir(base_path):
        ftype = "f" if os.path.isfile(os.path.join(base_path, f)) else "d"
        flist.append({
            "rel": f,
            "abs": os.path.join(base_path, f),
            "type": ftype
        })

    return flist

def upload_to_hf(folder_path, remote_path, repo_id):
    """Upload folder to Hugging Face"""
    for fdata in list_folders(folder_path):
        try:
            api = HfApi()
            ftype = fdata["type"]
            rel_path = fdata["rel"]
            abs_path = fdata["abs"]
            if ftype == "d":
                api.upload_folder(
                    folder_path=abs_path,
                    path_in_repo=rel_path,
                    repo_id=repo_id,
                    repo_type="dataset"
                )
            else:
                api.upload_file(
                    path_or_fileobj=abs_path,
                    path_in_repo=rel_path,
                    repo_id=repo_id,
                    repo_type="dataset"
                )
            print(f"Successfully uploaded {rel_path} to {repo_id}")
        except Exception as e:
            print(f"Error uploading dataset: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Upload folder to Hugging Face dataset")
    parser.add_argument("--token", required=True, help="Hugging Face API token")
    parser.add_argument("--repo_id", required=True, help="Repository ID (format: username/dataset-name)")
    parser.add_argument("--local_path", required=True, help="Local path containing folders to upload")
    parser.add_argument("--remote_path", required=True, help="Remote path to upload to")
    
    args = parser.parse_args()
    
    # Login to Hugging Face
    login_to_hf(args.token)
    
    # Upload to Hugging Face
    upload_to_hf(args.local_path, args.remote_path, args.repo_id)

if __name__ == "__main__":
    main()
