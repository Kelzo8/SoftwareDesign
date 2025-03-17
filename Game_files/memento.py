# memento.py
class Memento:
    def __init__(self, player_car_x, player_car_y, enemy_cars, coins):
        self.player_car_x = player_car_x
        self.player_car_y = player_car_y
        self.enemy_cars = enemy_cars[:]
        self.coins = coins[:]

    def get_state(self):
        return (self.player_car_x, self.player_car_y, self.enemy_cars, self.coins)