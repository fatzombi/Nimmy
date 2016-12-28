# Nimmy
a pattern/extension for telepot (telegram bot api client)

this is an extension on top of `telepot`

## simple example
```python
from nimmy import Bot
from re import match

bot = Bot("TELEGRAM_BOT_API_TOKEN")

# filtering content
def adminOnly(msg):
    return {
        'admin': match('fatzombi', msg.chat['username'])
    }


def ping(msg):
  return {
    'text': search("^ping\s(.*)", msg.text)
    }


# executes only when filtering contents match
@bot.filter(adminOnly)
def handle_this(msg):
  from subprocess import check_output
  hostname = msg.filter['text'].group(1)
  response = check_output(['ping', '-c 1', hostname])
  bot.sendMessage(msg.chat['id'], response)

  # feed the monitor!
  print("ping -> " + hostname)

# takes filtered functions as handle, binded on message_loop
bot.add_handle(handle_this)

# a simple run forever loop, takes message_loop args as loop={}
bot.run_forever()
```
