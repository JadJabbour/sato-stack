import sys

from lib import io_manager

from rpc import create_zrpc
from workers import ctrl_workers

p = None

def main():
    # load ZRPC server object
    zrpc_server = create_zrpc()

    # load celery workers & launch
    p = ctrl_workers('start')

    # start listening
    zrpc_server.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        io_manager.out(ex, is_exception=True, exception_info=sys.exc_info())
        if p is not None:
            p.kill()

    sys.exit()