# First, import click dependency
import click
import requests
from os.path import basename, splitext
from nile.cli import network_option
from nile.utils import get_hash

@click.command()
@click.argument("main_file", nargs=1)
@click.option("--compiler_version", nargs=1)
@network_option
def verify(main_file, network, compiler_version):
    """
    Command for automatically verify the sourcecode of a contract on starkscan.co.
    """
    contract_name = get_basename(main_file)

    if compiler_version is None:
        compiler_version = "0.10.0"

    data = {
      "main_file_path": main_file,
      "class_hash": get_hash(contract_name),
      "name": contract_name,
      "compiler_version": compiler_version,
      "is_account_contract": get_is_account(main_file),
      "files": get_files([main_file]),
    }

    subdomain = "api" if network == "mainnet" else "api-testnet"
    url = f"https://{subdomain}.starkscan.co/api/verify_class"

    print(f"Submitting to {url}")
    print(f"Submitting {data}")
    # res = requests.post(url=url, data=data)
    # print(res)



def get_is_account(main_file):
    # to do improve detection
    contract_name = get_basename(main_file)
    return contract_name.endswith("Account")

def get_files(contract_paths):
    files = {}

    for contract_path in contract_paths:
        contract_name = get_basename(contract_path)

        with open(contract_path) as f:
            file_contents = f.readlines()

        files[contract_name] = file_contents

    return files


def get_basename(path):
    return splitext(basename(path))[0]
