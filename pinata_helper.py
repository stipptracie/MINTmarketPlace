# Module for helper functions to pin files to ipfs in pinata

# Required Libraries
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# json headers for the json metadata api interaction
json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
}

# file headers for pinata api interaction
file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
}

# Uses CID v.1 of api to create a json file of metadata
def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

# Uses the api to pin a file to pinata and generate its ipfs hash
def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

# pins the metadata to the ipfs hash for the actual piece of artwork
def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=json_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash