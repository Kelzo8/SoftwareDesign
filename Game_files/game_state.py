class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.coin_count = 0
            cls._instance.is_running = True
            cls._instance.observers = []
            cls._instance.player_name = ""
        return cls._instance

    def set_player_name(self, name):
        self.player_name = name

    def add_coin(self):
        self.coin_count += 1

    def stop_game(self):
        self.is_running = False
        self.notify_observers()

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.player_name, self.coin_count)