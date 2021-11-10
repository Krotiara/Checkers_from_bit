from enum import Enum

class GameMods(Enum):
    two_players = '2 players'
    player_vs_ai = 'Player vs AI'
    ai_vs_ai = 'AI vs AI'
    black_color = 'Black'
    white_color = 'White'
    easy_ai = 'Easy'
    normal_ai = 'Normal'
    hard_ai = 'Hard'