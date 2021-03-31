from mongoengine import connect, disconnect

class db_manager(object):
    def __init__(self, host, port, auth_source, user, pwd, dbname):
        self.host = host
        self.port = int(port)
        self.auth_source = auth_source
        self.user = user
        self.pwd = pwd
        self.dbname = dbname

    def connectdb(self):
        connect(
            host=self.host,
            port=self.port,
            authentication_source=self.auth_source,
            username=self.user,
            password=self.pwd,
            db=self.dbname
        )

    def disconnectdb(self):
        disconnect()