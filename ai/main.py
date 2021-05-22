import sys

from lib import io_manager

from rpc import create_zrpc
from workers import ctrl_workers

ps = None

def main():
    # load ZRPC server object
    zrpc_server = create_zrpc()

    # load celery workers & launch
    ps = ctrl_workers('start')

    # start listening
    zrpc_server.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        io_manager.out(ex, is_exception=True, exception_info=sys.exc_info())
        if ps is not None:
            for p in ps:
                print('Killing celery worker')
                p.kill()

    sys.exit()