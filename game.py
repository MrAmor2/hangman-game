import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 6
WORDS = [
    "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА", 
    "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА", 
    "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ", 
    "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
]

stats = {
    "games_played": 0,
    "games_won": 0,
    "total_score": 0,
    "best_score": 0
}

def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")
    
    # Загрузка статистики
    global stats
    
    while True:
        # Выбор случайного слова
        secret_word = choose_random_word(WORDS)
        guessed_letters = set()
        attempts_left = MAX_ATTEMPTS
        game_won = False
        
        # Игровой цикл
        while attempts_left > 0:
            # Отрисовка текущего состояния игры
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + get_masked_word(secret_word, guessed_letters))
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            
            # Ввод буквы

            letter = get_user_guess(guessed_letters)
            guessed_letters.add(letter)
            
            # Проверка угадана ли буква

            if secret_word.count(letter) == 0:
                print("Этой буквы нет в слове")
                attempts_left -= 1
            else:
                print("Эта буква есть в слове")

            
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_letters):
                game_won = True
                break
        
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")

            score = calculate_score(secret_word, MAX_ATTEMPTS - attempts_left)
            print(f"Ваш счет: {score}")
            update_stats(True, score)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")

            update_stats(False, 0)
            draw_gallows(0)
        
        show_stats()
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)

def get_masked_word(secret_word: str, guessed_letters: Set[str]) -> str:
    """Генерация замаскированного слова"""

    masked_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            masked_word += letter
        else:
            masked_word += '*'
    return masked_word

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    
    body_pieces = [
        """
        --------  
        |      |  
        |      O  
        |     \|/ 
        |      |  
        |     / \ 
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |     \|/ 
        |      |  
        |     / \ 
        -         
        """
        ,
        """
        --------  
        |      |  
        |     \ / 
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |     \   
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |         
        |     / \ 
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |         
        |     /   
        |         
        -         
        """
        ,
        """
        --------  
        |      |  
        |         
        |         
        |         
        |         
        -         
        """
    ]

    print(body_pieces[attempts_left])
    

def get_user_guess(guessed_letters: Set[str]) -> str:
    """Ввод и валидация буквы от пользователя"""

    while True:
        print("Введите букву")

        letter = input().upper()

        if letter in guessed_letters:
            print("Эта буква была введена ранее")
            continue
        if len(letter) != 1:
            print("Введено более одного символа")
            continue
        if not letter.isalpha():
            print("Введена не буква")
            continue

        return letter

def check_win(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Проверка, угадано ли все слово"""

    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""

    return len(secret_word) + (MAX_ATTEMPTS - attempts_used)

def update_stats(won: bool, score: int):
    """Обновление статистики в памяти"""
    global stats

    stats["games_played"] += 1

    if won:
        stats["games_won"] += 1

        if score > stats["best_score"]:
            stats["best_score"] = score

        stats["total_score"] += score
    

def show_stats():
    """Отображение статистики"""
    global stats
    
    win_percentage = stats["games_won"] / stats["games_played"] * 100
    average_score = stats["total_score"] / stats["games_played"]
    
    print("\n=== Статистика ===")
    
    print(f"Всего игр: {stats['games_played']}")
    print(f"Побед: {stats['games_won']} ({win_percentage:.1f}%)")
    print(f"Лучший счёт: {stats['best_score']}")
    if stats["games_won"] > 0:
        print(f"Средний счёт: {average_score:.1f}")

if __name__ == "__main__":
    main()