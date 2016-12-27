from telepot import Bot
from functools import wraps
from nimmy.utils import Map


class Bot(Bot):
    bot_functions = []

    def check_filters(self, filters, msg_object):
        try:
            f = filters(msg_object)
        except:
            return False

        if None in f:
            return False
        else:
            return True

    def _filter(self, filters, msg):
        validate = self.check_filters(filters, msg)
        return validate

    def filter(self, filter_model):
        def decorator(func):
            @wraps(func)
            def wrapper(msg):
                message = Map(**msg)
                if self._filter(filter_model, message):
                    return func(message)
            return wrapper
        return decorator

    def run_forever(self, loop={}, sleep_for=10):

        print('Loading ...')
        self.message_loop(self.dummy_handler, **loop)

        from time import sleep
        while 1:
            sleep(sleep_for)

    def add_handle(self, handle):
        Bot.bot_functions.append(handle)

    def dummy_handler(self, msg):
        return [h(msg) for h in Bot.bot_functions]
