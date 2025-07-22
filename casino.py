import random

# Символы и их веса для генерации
SYMBOLS = {
    "🍒": 35,
    "🍋": 30,
    "🍇": 25,
    "🔔": 15,
    "💎": 10,
    "7️⃣": 5
}

# Выигрышные комбинации
PAY_TABLE = {
    ("7️⃣", "7️⃣", "7️⃣"): 100,
    ("💎", "💎", "💎"): 50,
    ("🔔", "🔔", "🔔"): 20,
    ("🍇", "🍇", "🍇"): 15,
    ("🍋", "🍋", "🍋"): 10,
    ("🍒", "🍒", "🍒"): 7,
    ("🍒", "🍒", "🍒"): 5,
}

class SlotMachine:
    def __init__(self):
        self.reels = [list(SYMBOLS.keys()) for _ in range(3)]
        self.weights = list(SYMBOLS.values())
    
    def spin(self):
        return [
            random.choices(self.reels[0], weights=self.weights, k=1)[0],
            random.choices(self.reels[1], weights=self.weights, k=1)[0],
            random.choices(self.reels[2], weights=self.weights, k=1)[0]
        ]

def check_win(result):
    result_tuple = tuple(result)
    
    # Проверка выигрышных комбинаций
    for combination, payout in PAY_TABLE.items():
        if result_tuple == combination:
            return payout
    
    # Проверка двух одинаковых символов
    if result[0] == result[1] or result[1] == result[2]:
        return 2
    
    return 0
