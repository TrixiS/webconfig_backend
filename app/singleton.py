class Singleton:
    _instance: "Singleton" = None

    @classmethod
    def instance(cls, *, new: bool = False):
        if cls._instance is None or new:
            cls._instance = cls()

        return cls._instance

    @classmethod
    def has_instance(cls):
        return cls._instance is not None
