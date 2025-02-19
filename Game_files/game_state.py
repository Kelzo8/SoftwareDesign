# game_state.py
class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.coin_count = 0
            cls._instance.is_running = True
        return cls._instance

    def add_coin(self):
        self.coin_count += 1

    def stop_game(self):
        self.is_running = False
