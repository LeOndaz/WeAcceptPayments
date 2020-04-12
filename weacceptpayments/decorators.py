class classonlymethod(classmethod):
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("This method is available only on the class itself and not on instances.")
        return super().__get__(instance, cls)