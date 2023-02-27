install on crontab:
crontab -e
*/1 * * * * cd /home/deploy/node-restart-bot && /home/deploy/.local/bin/poetry run python3 /home/deploy/node-restart-bot/main.py http://localhost:14957 --daemon gaiad --stall 2 --discord https://discord.com/api/webhooks/1079598335285018684/k1FGa8RqEozJLronf1jj8IF1ks6o8PbNdzQvpjsMhQ0D6TZm3FPsmZvD2Fj0Zx3rNkWubx >> /logs/gaiad-node-restart.log 2>&1