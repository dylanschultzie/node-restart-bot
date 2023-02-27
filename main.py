from typing import Dict
import requests

def get_status_info(sync_info: Dict) -> tuple:
    catching_up = sync_info["catching_up"]
    latest_block_time = sync_info["latest_block_time"]
    return catching_up, latest_block_time

def get_peer_info(net_info: Dict) -> int:
    return net_info['result']['n_peers']


def main():
    # status = requests.get("http://localhost:16257/status").json()
    # net_info = requests.get("http://localhost:16257/net_info").json()
    status = requests.get("https://juno-rpc.lavenderfive.com/status").json()
    net_info = requests.get("https://juno-rpc.lavenderfive.com/net_info").json()

    catching_up, latest_block_time = get_status_info(status["result"]["sync_info"])
    peer_count = get_peer_info(net_info)

    print(catching_up)
    print(latest_block_time)
    print(peer_count)

if __name__ == "__main__":
    main()