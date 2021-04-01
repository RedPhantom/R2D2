# Purpose: contain application exceptions.

class AppExceptions:
    def __init__(self):
        pass

    class InvalidPathException(Exception):
        def __init__(self, invalid_path, message="The specified path does not exist: %s"):
            self._path = invalid_path
            self._message = message

            super().__init__(self._message % (self._path,))

    class SerialException(Exception):
        pass
