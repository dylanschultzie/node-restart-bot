## Installation

1. Requires python 3.11+
2. Install dependencies:
```
poetry install
```
3. Run it!
```
poetry run python3 main.py http://localhost:14957 --daemon gaiad --stall 2 --discord https://discord.com/api/webhooks/10795983352018684/k1FGa8RqEozJLronf1jj8IF1ks6o8PbNdzQvpjsMhQ0D6TZm3FPsmZvD2Fj0Zubx
```
install on crontab:
crontab -e
```
*/1 * * * * cd /home/USER/node-restart-bot && /home/USER/.local/bin/poetry run python3 /home/USER/node-restart-bot/main.py http://localhost:14957 --daemon gaiad --stall 2 --discord https://discord.com/api/webhooks/10795983152018684/k1FGa8RqEozJLronf1jj8IF1ks6o8PbNdzQvpjsMhQ0D6TZm3FPsmZvD2Fj0Zubx >> /logs/gaiad-node-restart.log 2>&1
```