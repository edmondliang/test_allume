import queries


class DBAPI:
    __dburi = None
    __pool_max_size = None

    @staticmethod
    def init(dburi, pool_max_size):
        DBAPI.__dburi = dburi
        DBAPI.__pool_max_size = pool_max_size

    def __enter__(self):
        assert self.__pool_max_size
        self.session = queries.Session(self.__dburi, pool_max_size=self.__pool_max_size)
        self.session.query("SET TIME ZONE 'UTC';")
        self.session.connection.set_session(autocommit=False)
        return self.session.__enter__()

    def __exit__(self, exec_type, exec_instance, traceback):
        if exec_instance:
            self.session.connection.rollback()
        else:
            self.session.connection.commit()
        self.session.__exit__(exec_type, exec_instance, traceback)
        return exec_instance is None
