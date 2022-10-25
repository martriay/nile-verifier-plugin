# First, import click dependency
import time
import click
import logging
from os.path import basename, splitext
from nile.common import get_hash
from nile_verifier.api import Api
from yaspin import yaspin
from yaspin.spinners import Spinners

@click.command()
@click.argument("main_file", nargs=1)
@click.option("--network", nargs=1, required=True)
@click.option("--compiler_version", nargs=1, default="0.10.0")
def verify(main_file, network, compiler_version):
    """
    Command for automatically verify the sourcecode of a contract on starkscan.co.
    """
    api = Api(network)
    contract_name = get_contract_name(main_file)
    class_hash = hex(get_hash(contract_name))

    if api.is_hash_verifiable(class_hash):
        logging.info(f"🔎  Verifying {contract_name} on {network}...")
        job_id = api.create_job({
            "main_file_path": basename(main_file),
            "class_hash": class_hash,
            "name": contract_name,
            "compiler_version": compiler_version,
            "is_account_contract": check_is_account(main_file),
            "files": get_files(main_file),
        })

        status = 'PENDING'
        with yaspin(Spinners.earth, text="Waiting for verification result") as sp:
            while status == 'PENDING':
                time.sleep(1)
                status, response = api.get_job_status(job_id)

        if status == 'FAILED':
            logging.error("💥  Verification failed:")
            logging.error(response['error_message'])
        else:
            scanner_url = api.get_scanner_link(class_hash)
            logging.info(f"✅  Success! {scanner_url}")


def check_is_account(main_file):
    # to do: improve detection
    contract_name = get_contract_name(main_file)
    return contract_name.endswith("Account")

def get_files(main_file):
    # to do: support multifile
    contract_paths = [main_file]

    files = {}
    for contract_path in contract_paths:
        contract_filename = basename(contract_path)
        with open(contract_path) as f:
            files[contract_filename] = f.read()

    return files

def get_contract_name(path):
    return splitext(basename(path))[0]
