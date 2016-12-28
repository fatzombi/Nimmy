from nimmy import Bot
from re import match, search

bot = Bot("TELEGRAM_BOT_API_TOKEN")


def adminOnly(msg):
    return {
        'admin': match('fatzombi', msg.chat['username'])
    }


def ping(msg):
    return {
        'text': search("^ping\s(.*)", msg.text)
    }


@bot.filter(adminOnly)
@bot.filter(ping)
def handle_this(msg):
    from subprocess import check_output

    hostname = msg.filter['text'].group(1)
    response = check_output(['ping', '-c 1', hostname])

    bot.sendMessage(msg.chat['id'], response)

    print("ping -> " + hostname)

bot.add_handle(handle_this)

bot.run_forever()
