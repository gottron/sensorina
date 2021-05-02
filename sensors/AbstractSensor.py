class AbstractSensor:
    def __init__(self) :
        pass

    def setup(self, db) :
        pass

    def shutdown(self) :
        pass

    def get_reading(self) :
        pass

    def min_call_delay(self):
        pass