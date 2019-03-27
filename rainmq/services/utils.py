class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = super().__new__(cls)
        return Singleton._instance
