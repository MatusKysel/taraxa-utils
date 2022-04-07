import json
import requests
from time import sleep

net = "test"
#net = "dev"
week = 14

url = "https://rpc." + net + "net.taraxa.io"
get_url = "https://explorer." + net + "net.taraxa.io/api/nodes?limit=1000&week=" + \
    str(week) + "&year=2022"


def get_stake(account):
    r = requests.post(url, data=json.dumps(
        {"jsonrpc": "2.0", "method": "taraxa_queryDPOS", "params": [{"account_queries": {account: {"with_staking_balance": True}}}], "id": 0}))
    return int(json.loads(r.text)["result"]["account_results"][account]["staking_balance"], 16) / 100000000000000000000000


def number_of_nodes():
    output = {}
    r = requests.get(get_url)
    nodes = json.loads(r.text)["result"]["nodes"]
    print("Number of nodes : " + str(len(nodes)))
    for node in nodes:
        output[node["_id"]] = node["count"]
    return output


if __name__ == "__main__":
    nodes = number_of_nodes()
    for node in nodes:
        stake = int(get_stake(node))
        print("node: " + node + " " + str(nodes[node]) + " " + str(stake))

    # print(nodes["0x710fc2dcb4eb91af83510a7ee3f5d3ddefbd29e3"])
