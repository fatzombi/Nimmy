# Nimmy
a sadistic pattern/extension for telepot (telegram bot api client)

this is an extension on top of `telepot`

## simple example
```python
from nimmy import Bot
from re import match

bot = Bot("TELEGRAM_BOT_API_TOKEN")

# filtering content
def adminOnly(msg):
    return [
        match('fatzombi', msg.chat['username'])
    ]

# executes only when filtering contents match
@bot.filter(adminOnly)
def handle_this(msg):
    print(msg.chat)
    bot.sendMessage(msg.chat['id'], 'hi')

# takes filtered functions as handle, binded on message_loop
bot.add_handle(handle_this)

# a simple loop
bot.run_forever()
```
