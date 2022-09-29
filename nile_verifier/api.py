import json
import logging
import requests

logging.getLogger("urllib3").setLevel(logging.WARNING)

class Api:
    def __init__(self, network):
        if not network in ['goerli', 'mainnet']:
            raise Exception("--network can only be mainnet or goerli")
        self.network = network
        subdomain = "api" if network == "mainnet" else "api-testnet"
        self.api_url = f"https://{subdomain}.starkscan.co/api"
      
    def get_scanner_link(self, class_hash):
        domain = "starkscan.co" if self.network == "mainnet" else "testnet.starkscan.co"
        return f"https://{domain}/class/{class_hash}#code"

    def create_job(self, data):
        headers = {'Content-type': 'application/json'}
        endpoint = f"{self.api_url}/verify_class"
        res = requests.post(endpoint, json=data, headers=headers)

        if res.status_code == 200:
            response = json.loads(res.text)
            return response['job_id']
        elif res.status_code == 400:
            logging.error(res.text)
        else:
            logging.error(f"Got error {res.status_code}")
            logging.error(res.text)

    def get_job_status(self, job_id):
        res = requests.get(f"{self.api_url}/verify_class_job_status/{job_id}")
        response = json.loads(res.text)
        return response['status']
        
    def is_hash_verifiable(self, class_hash):
        res = requests.get(f"{self.api_url}/hash/{class_hash}")
        if res.status_code == 200:
            if json.loads(res.text)['is_verified']:
                logging.info("")
                logging.info(f"✨ Contract is already verified:")
                logging.info("")
                logging.info(f"       {self.get_scanner_link(class_hash)}")
                logging.info("")
            else:
                return True
        elif res.status_code == 404 and "could not find hash" in res.text:
            logging.error(f"❌ Could not find any contract with hash {class_hash}")
            logging.error(f"🤔 Are you sure you deployed to {self.network}?")
        else:
            logging.error(f"Got error {res.status_code}")
            logging.error(res.text)

        return False
