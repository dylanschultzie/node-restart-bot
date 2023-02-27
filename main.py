from typing import Dict
import requests
from datetime import datetime, timedelta
import subprocess
import argparse

DAEMON=''
STALL_MINUTES=''
DISCORD_WEBHOOK=''

def get_status_info(sync_info: Dict) -> tuple:
    catching_up = sync_info["catching_up"]
    latest_block_time = sync_info["latest_block_time"]
    return catching_up, latest_block_time


def get_peer_info(net_info: Dict) -> int:
    return net_info["result"]["n_peers"]


def handle_lost_peers():
    status = subprocess.run("systemctl restart {{ DAEMON }}", shell=True)


def handle_stalled(catching_up: bool, latest_block_time: str):
    block_time = datetime.strptime(latest_block_time, "%Y-%m-%dT%I:%M:%S")
    if not catching_up and node_stalled():
        status = subprocess.run("systemctl restart {{ DAEMON }}", shell=True)


def node_stalled(block_time: datetime) -> bool:
    return block_time < (datetime.now() - timedelta(minutes=STALL_MINUTES))

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Create script that will check if node is stalled, and restart if so."
    )
    parser.add_argument(
        "--daemon",
        dest="service_file_name",
        required=True,
        help="service file name (ex. junod)",
    )
    parser.add_argument(
        "--stall",
        dest="stall_minutes",
        default=2,
        help="how long can a node be stalled before restarting",
    )
    parser.add_argument(
        "--discord",
        dest="discord",
        help="discord webhook url",
    )
    return parser.parse_args()



def main():
    global DAEMON
    global DISCORD_WEBHOOK
    global STALL_MINUTES
    args = parseArgs()
    DAEMON = args.service_file_name
    DISCORD_WEBHOOK = args.stall_minutes
    STALL_MINUTES = args.discord

    # status = requests.get("http://localhost:16257/status").json()
    # net_info = requests.get("http://localhost:16257/net_info").json()
    status = requests.get("https://juno-rpc.lavenderfive.com/status").json()
    net_info = requests.get("https://juno-rpc.lavenderfive.com/net_info").json()

    catching_up, latest_block_time = get_status_info(status["result"]["sync_info"])
    block_time = datetime.strptime(latest_block_time[:19], "%Y-%m-%dT%I:%M:%S")
    peer_count = get_peer_info(net_info)
    if not peer_count:
        handle_lost_peers()
        exit("Restarted daemon")

    handle_stalled()


if __name__ == "__main__":
    main()
