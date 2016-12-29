# Nimmy
a pattern/extension built on top of telepot (telegram bot api wrapper)

## example
```python
from nimmy import Bot
from re import match, search

bot = Bot("TELEGRAM_BOT_API_TOKEN")

# filter model function returns, keys return None on failure
def adminOnly(msg):
    return {
        'admin': match('fatzombi', msg.chat['username'])
    }


def ping(msg):
  return {
    'text': search("^ping\s(.*)", msg.text)
    }


# executes only when filtering contents match takes filter function and check type: any or all
@bot.filter(adminOnly)
@bot.filter(ping)
def handle_this(msg):
  from subprocess import check_output

  hostname = msg.ping['text'].group(1)
  response = check_output(['ping', '-c 1', hostname])

  bot.sendMessage(msg.chat['id'], response)

  # feed the monitor!
  print("ping -> " + hostname)

# takes filtered functions as handle, binded on message_loop
bot.add_handle(handle_this)

# a simple run forever loop, takes message_loop args as loop={}
bot.run_forever()
```
