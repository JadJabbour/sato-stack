import zerorpc

from lib import io_manager
from interface.zrpc import zero_router

def create_zrpc():
    io = io_manager(do_init=False)

    io.load_config(config_file_path='config.ini')

    protocol, host, port, name = io.load_zmq_config()
    
    server = zerorpc.Server(zero_router(), name=name)
    server.bind(':'.join(['://'.join([str(protocol), str(host)]), str(port)]))
    return server
