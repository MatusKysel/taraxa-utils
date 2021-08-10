import json
import requests
import subprocess
import shlex
from time import sleep

url = "http://127.0.0.1:7777"


template_text = "kubectl port-forward po/%s 7777:7777"
nodes = {"blockchain-testnet-boot-node-2",
         "blockchain-testnet-boot-node-1",
         "blockchain-testnet-boot-node-0"}


def get_pbft_chain_size():
    r = requests.post(url, data=json.dumps(
        {"jsonrpc": "2.0", "method": "get_pbft_chain_size", "params": {}, "id": 0}))
    return int(json.loads(r.text)["result"]["value"])
    # return height


def get_pbft_block_hash(block_num):
    r = requests.post(url, data=json.dumps(
        {"jsonrpc": "2.0", "method": "get_pbft_chain_blocks", "params": [{"height": block_num, "count": 1, "include_json": "true"}], "id": 0}))
    return json.loads(r.text)["result"]["value"][0]["block"]


def check_for_fork():
    lowest_chain = 999999999
    old_block = ''
    old_node = ''
    for node in nodes:
        child = subprocess.Popen(shlex.split(
            template_text % node), stdout=subprocess.PIPE)
        try:
            sleep(3)
            size = get_pbft_chain_size()
            if(lowest_chain > size):
                lowest_chain = size
            child.terminate()
        except:
            child.terminate()
    print(lowest_chain)
    for node in nodes:
        child = subprocess.Popen(shlex.split(
            template_text % node), stdout=subprocess.PIPE)
        try:
            sleep(3)
            block = get_pbft_block_hash(lowest_chain)
            if(len(old_block) != 0 and old_block != block):
                print(node)
                print(block)
                print(old_node)
                print(old_block)
            old_block = block
            old_node = node
            child.terminate()
        except:
            child.terminate()


if __name__ == "__main__":
    check_for_fork()
