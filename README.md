### CarHunter

Usage:
1. Create a Telegram Bot
2. Start a conversation between the bot and your main Telegram account (just text it)
3. Go to `https://api.telegram.org/bot<your_bot_token>/getUpdate` and find your chat token there
4. Put it in the `.env` file, along with other env vars

Dependencies (install using pip):
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [requests](https://pypi.org/project/requests)