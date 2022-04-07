from web3 import Web3
from eth_account import Account
import threading
import secrets

url = "https://rpc.testnet.taraxa.io"
#url = "https://rpc-pr-1676.prnet.taraxa.io"

number_of_trx = 1000

def thread_functions(name):
    pk = "0x" + secrets.token_hex(32)
    print("Thread " + name + ": private key " + pk + " account " + Account.from_key(pk).address)
    w3 = Web3(Web3.HTTPProvider(url))
    chain_id = w3.eth.chain_id
    print("Thread " + name + ": sending " + str(number_of_trx) + " transactions ...")
    for x in range(number_of_trx):
        w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(dict(
            nonce=x,
            to='0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
            value=0,
            gas=100000,
            gasPrice=0,
            data=b'blabla',
            chainId=chain_id,
        ), pk).rawTransaction)
        if (x and x % (number_of_trx/10) == 0):
            print("Thread " + name + ": sent " + str(x) + " transactions")

def test_connection():
    #for url in urls:
    w3 = Web3(Web3.HTTPProvider(url))
    print(w3.eth.chain_id)

def transaction_benchmark():
    threads = list()
    for index in range(10):
        x = threading.Thread(target=thread_functions, args=(str(index),))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # acct = Account.from_key(pk)
    # print(acct.address)
    #test_connection()
    transaction_benchmark()