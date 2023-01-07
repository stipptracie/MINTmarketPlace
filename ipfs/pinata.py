# load required libraries
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

# grab env variables for url requests
file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
}

json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
}


# create functions to use pinata api with json requests
# convert data to json format





# def convert_data_to_json(content):
#     data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
#     return json.dumps(data)

# # funciton to pin data to ipfs and return an ipfs hash
# def pin_file_to_ipfs(data):
#     r = requests.post(
#         "https://api.pinata.cloud/pinning/pinFileToIPFS",
#         files={'file': data},
#         headers=file_headers
#     )
#     print(r.json())
#     ipfs_hash = r.json()["IpfsHash"]
#     return ipfs_hash

# # function to pin json data to ipfs with right credentials
# def pin_json_to_ipfs(json):
#     r = requests.post(
#         "https://api.pinata.cloud/pinning/pinJSONToIPFS",
#         data=json,
#         headers=json_headers
#     )
#     print(r.json())
#     ipfs_hash = r.json()["IpfsHash"]
#     return ipfs_hash