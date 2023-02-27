import argparse
import logging
import subprocess

from datetime import datetime, timedelta
from discord import SyncWebhook
from typing import Dict
from utils.request import get_response

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


def is_stalled(catching_up: bool, latest_block_time: str) -> bool:
    block_time = datetime.strptime(latest_block_time, "%Y-%m-%dT%H:%M:%S")
    return not catching_up and node_stalled(block_time)


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


def format_block_time(block_time: str) -> str:
    # turns block time from 2023-02-27T00:48:50.822051683Z to 2023-02-27T00:48:50
    return block_time[:19]


def handle_restart(peer_count: int, catching_up: bool, block_time: str) -> tuple:
    alert_message = f"❌ | node: { RPC } | "
    restart = False

    if is_stalled(catching_up, format_block_time(block_time)):
        restart = True
        alert_message = f"{ alert_message } node stalled, node restarted"
    elif peer_count == 0:
        restart = True
        alert_message = f"{ alert_message } peers lost, node restarted"

    if restart:
        output = subprocess.run(f"sudo systemctl restart { DAEMON }", shell=True, capture_output=True)
        restart_output = output.stdout.decode("utf-8")
        logger.warning(f"node output: { restart_output }, code: { output.returncode }")

    return restart, alert_message


def alert(alert_message: str):
    if DISCORD_WEBHOOK:
        DISCORD_WEBHOOK.send(alert_message)


def get_args():
    global DAEMON
    global DISCORD_WEBHOOK
    global STALL_MINUTES
    global RPC

    args = parseArgs()
    DAEMON = args.service_file_name
    STALL_MINUTES = args.stall_minutes
    DISCORD_WEBHOOK = SyncWebhook.from_url(args.discord)
    RPC = args.rpc


def main():
    get_args()

    status = get_response(f"{ RPC }/status")
    net_info = get_response(f"{ RPC }/net_info")

    catching_up, latest_block_time = get_status_info(status["result"]["sync_info"])
    peer_count = get_peer_info(net_info)

    restart, alert_message = handle_restart(peer_count, catching_up, format_block_time(latest_block_time))

    if restart:
        alert(alert_message)
    else:
        logger.info(f"✅ | node: { RPC } | healthy")


if __name__ == "__main__":
    main()
