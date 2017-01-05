from telepot import Bot
from functools import wraps
from nimmy.utils import Map
from threading import Thread


class Bot(Bot):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)

        # holds script functions
        self.scripts = []

    def _filter(self, filter_model, message, check):

        # checks for any exceptions with filters, find None, true or false
        try:
            filters = filter_model(message)
            if check(filters.values()):
                filters.update({'filter_name': filter_model.__name__})
                return filters
        except:
            return False

    def filter(self, filter_model, check=all):

        # argumented decoration, returns func with msg
        def decorator(func):

            # prevents cloning
            @wraps(func)
            def wrapper(msg):

                # converts dict to object with utils.Map
                message = Map(**msg)
                filterd = self._filter(filter_model, message, check)

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
        self.scripts.append(handle)

    def dummy_handler(self, msg):

        # acts like a handle returns a list of handles and execute
        for script in self.scripts:

            # threading to prevent filter blocks (eg: infinite loops)
            t = Thread(target=script, args=(msg, ))
            t.start()
