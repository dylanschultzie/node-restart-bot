## Installation

1. Requires python 3.11+
3. Requires poetry 1.4.0+
```
curl -sSL https://install.python-poetry.org | python3 -
```
2. Install dependencies:
```
poetry install
```
3. Run it!
```sh
poetry run python3 ./src/main.py http://localhost:14957 --daemon gaiad --stall 2 --discord https://discord.com/api/webhooks/10795983352018684/k1FGa8RqEozJLronf1jj8IF1ks6o8PbNdzQvpjsMhQ0D6TZm3FPsmZvD2Fj0Zubx
```

## crontab
install on crontab:
```sh
crontab -e
```

```sh
*/1 * * * * cd /home/USER/node-restart-bot && /home/USER/.local/bin/poetry run python3 /home/USER/node-restart-bot/src/main.py --rpc http://localhost:14957 --daemon gaiad --stall 2 --discord https://discord.com/api/webhooks/10795983152018684/k1FGa8RqEozJLronf1jj8IF1ks6o8PbNdzQvpjsMhQ0D6TZm3FPsmZvD2Fj0Zubx >> /logs/gaiad-node-restart.log 2>&1
```

to then get the logs:

```
cat /logs/gaiad-node-restart.log
```
