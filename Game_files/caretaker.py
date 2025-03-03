# caretaker.py
class Caretaker:
    def __init__(self):
        self.memento = None

    def save_memento(self, memento):
        self.memento = memento

    def get_last_memento(self):
        temp = self.memento
        self.memento = None
        return temp