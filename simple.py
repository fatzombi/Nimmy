from re import match, search
from nimmy import Bot

bot = Bot("300090949:AAFt233ePJW-tafv7g28Dj-1hPYmw2uoP4E")


def adminOnly(msg):
    return {
        'admin': match('fatzombi', msg.chat['username'])
    }


def ping(msg):
    return {
        'text': search("^ping\s(.*)", msg.text),
        'admin': adminOnly(msg)
    }


@bot.filter(ping)
def handle_this(msg):
    from subprocess import check_output

    hostname = msg.ping['text'].group(1)
    response = check_output(['ping', '-c 1', hostname])

    bot.sendMessage(msg.chat['id'], response)

    print("ping -> " + hostname)

# bot handle executes from top to bottom
bot.add_handle(handle_this)

bot.run_forever()
