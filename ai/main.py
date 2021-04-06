import sys

import zerorpc

from lib import io_manager
from interface.mq import zero_router

from jobs import worker

cw = None

def main():
    io = io_manager(do_init=False)

    io.load_config(config_file_path='config.ini')

    protocol, host, port, name = io.load_zmq_config()

    server = zerorpc.Server(zero_router(), name=name)
    server.bind(':'.join(['://'.join([str(protocol), str(host)]), str(port)]))
    cw = worker()
    server.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        io_manager.out(ex, is_exception=True, exception_info=sys.exc_info())
        if cw is not None:
            cw.terminate()
    
    sys.exit()