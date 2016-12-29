from telepot import Bot
from functools import wraps
from nimmy.utils import Map


class Bot(Bot):
    """
    extending telepot.Bot
    """
    bot_functions = {}

    def _filter(self, filter_model, message):

        # checks for any exceptions with filters, find None, true or false
        try:
            filters = filter_model(message)
            if all(filters.values()):
                filters.update({'filter_name': filter_model.__name__})
                return filters
        except:
            pass

    def filter(self, filter_model):

        # argumented decoration, returns func with msg
        def decorator(func):

            # prevents cloning
            @wraps(func)
            def wrapper(msg):

                # converts dict to object with utils.Map
                message = Map(**msg)
                filterd = self._filter(filter_model, message)

                if filterd:
                    setattr(message, filterd['filter_name'], filterd)
                    return func(message)
            return wrapper
        return decorator

    def run_forever(self, sleep_for=10, **loop):
        # telepot message_loop with dummy_handler
        print('Listening ...')
        self.message_loop(self.dummy_handler, **loop)

        from time import sleep
        # simple loop sleeps: sleep_for
        while 1:
            sleep(sleep_for)

    def add_handle(self, handle):
        # add filter handles to a list
        try:
            Bot.bot_functions[id(self)]
        except KeyError:
            Bot.bot_functions[id(self)] = []

        Bot.bot_functions[id(self)].append(handle)

    def dummy_handler(self, msg):
        # acts like a handle returns a list of handles and execute
        return [h(msg) for h in Bot.bot_functions[id(self)]]
