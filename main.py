from typing import Dict
import requests
from datetime import datetime, timedelta
import subprocess
import argparse
from discord import SyncWebhook
import logging

DAEMON: str
STALL_MINUTES: int
DISCORD_WEBHOOK: SyncWebhook
RPC: str

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(message)s")
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


def get_status_info(sync_info: Dict) -> tuple:
    catching_up = sync_info["catching_up"]
    latest_block_time = sync_info["latest_block_time"]
    return catching_up, latest_block_time


def get_peer_info(net_info: Dict) -> int:
    return net_info["result"]["n_peers"]


def handle_lost_peers() -> tuple:
    message = f"❌ | node: { RPC } | peers lost, node restarted"
    status = subprocess.run(f"systemctl restart { DAEMON }", shell=True)
    return message, status


def handle_stalled(catching_up: bool, latest_block_time: str) -> tuple:
    message: str = ""
    status: str = ""
    block_time = datetime.strptime(latest_block_time, "%Y-%m-%dT%H:%M:%S")
    if not catching_up and node_stalled(block_time):
        status = subprocess.run(f"systemctl restart { DAEMON }", shell=True)
        message = f"❌ | node: { RPC } | stalled, node restarted"
    return message, status


def node_stalled(block_time: datetime) -> bool:
    return block_time < (datetime.now() - timedelta(minutes=STALL_MINUTES))


def parseArgs():
    parser = argparse.ArgumentParser(description="Create script that will check if node is stalled, and restart if so.")
    parser.add_argument(
        "-r",
        "--rpc",
        dest="rpc",
        required=True,
        help="local rpc endpoint (ex. http://localhost:26657)",
    )
    parser.add_argument(
        "-d",
        "--daemon",
        dest="service_file_name",
        required=True,
        help="service file name (ex. junod)",
    )
    parser.add_argument(
        "-s",
        "--stall",
        dest="stall_minutes",
        default=2,
        type=int,
        help="how long can a node be stalled before restarting",
    )
    parser.add_argument(
        "--discord",
        dest="discord",
        help="discord webhook url",
    )
    return parser.parse_args()


def reduce_block_time(block_time: str) -> str:
    # turns block time from 2023-02-27T00:48:50.822051683Z to 2023-02-27T00:48:50
    return block_time[:19]


def main():
    global DAEMON
    global DISCORD_WEBHOOK
    global STALL_MINUTES
    global RPC
    args = parseArgs()

    DAEMON = args.service_file_name
    STALL_MINUTES = args.stall_minutes
    DISCORD_WEBHOOK = SyncWebhook.from_url(args.discord)
    RPC = args.rpc

    message: str

    status = requests.get(f"{ RPC }/status").json()
    net_info = requests.get(f"{ RPC }/net_info").json()

    catching_up, latest_block_time = get_status_info(status["result"]["sync_info"])
    peer_count = get_peer_info(net_info)
    if not peer_count:
        message, status = handle_lost_peers()
    else:
        message, status = handle_stalled(catching_up, reduce_block_time(latest_block_time))

    if message:
        logger.info(message + f" | status: { status }")
        if DISCORD_WEBHOOK:
            DISCORD_WEBHOOK.send(message)
    else:
        logger.info(f"✅ | node: { RPC } | healthy")


if __name__ == "__main__":
    main()
