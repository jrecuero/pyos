class DbMO:
    """DbMO class is the database class.
    """

    _ID = 0

    def __init__(self, name):
        self.name = name
        self._repo = {}
        self._indexes = {}

    def _next_id(self):
        """_next_id returns the next unique ID.
        """
        DbMO._ID += 1
        return DbMO._ID

    def add(self, entry):
        """add adds a new entry to the database.
        """
        pass

    def delete(self, entry):
        """delete deletes an entry from the database.
        """
        pass

    def get(self, entry):
        """get retrieves an entry from the database.
        """
        pass

    def reindex(self):
        """reindex reindexes the database.
        """
        pass
