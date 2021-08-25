import json
import requests
import subprocess
import shlex
from time import sleep

url = "http://127.0.0.1:9999"


template_text = "kubectl -n blockchain-testnet port-forward po/%s 9999:7777"
node_template = "blockchain-testnet-consensus-node-%s"
number_of_nodes = 6
# template_text = "kubectl -n blockchain-devnet port-forward po/%s 9999:7777"
# node_template = "blockchain-devnet-consensus-node-%s"
# number_of_nodes = 19


def get_node_status():
    r = requests.post(url, data=json.dumps(
        {"jsonrpc": "2.0", "method": "get_node_status", "params": {}, "id": 0}))
    return json.loads(r.text)["result"]["node_count"], json.loads(r.text)["result"]["peer_count"]


def check_number_of_peers():
    for idx in range(number_of_nodes):
        node = node_template % idx
        child = subprocess.Popen(shlex.split(
            template_text % node), stdout=subprocess.PIPE)
        try:
            sleep(3)
            nodes, peers = get_node_status()
            print(node + " see " + str(nodes) + " nodes and is connected to " + str(peers) + " peers")
            child.terminate()
        except:
            child.terminate()


if __name__ == "__main__":
    check_number_of_peers()
