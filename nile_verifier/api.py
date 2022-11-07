import json
import logging
import requests

logging.getLogger("urllib3").setLevel(logging.WARNING)

NETWORKS = ['goerli', 'goerli2', 'integration', 'mainnet']

class Api:
    def __init__(self, network):
        if not network in NETWORKS:
            raise Exception(f"--network can only be one of {NETWORKS}")
        self.network = network
        subdomain = {
            "mainnet": "api",
            "goerli": "api-testnet",
            "goerli2": "api-testnet-2",
            "integration": "api-integration"
        }[network]
        self.api_url = f"https://{subdomain}.starkscan.co/api"
      
    def get_scanner_link(self, class_hash):
        domain = {
            "mainnet": "starkscan.co",
            "goerli": "testnet.starkscan.co",
            "goerli2": "testnet-2.starkscan.co",
            "integration": "integration.starkscan.co"
        }[self.network]
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
        return response['status'], response
        
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
