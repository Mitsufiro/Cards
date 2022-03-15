import random
from io import StringIO
import argparse


class Logger:  # логер
    def __init__(self):
        self.container = StringIO()

    def logged_input(self, prompt=""):  # логирование ввода
        _in = "\u21A9"  # символ ↩
        _out = "\u21AA"  # символ ↪
        _input = input(prompt)
        self.container.write(f"{_out} {''.join(prompt)}\n{_in} {str(_input)}\n")
        return _input

    def print_and_log(self, *args, **kwargs):  # логирование вывода
        _out = "\u21AA"  # символ ↪
        print(*args, **kwargs)

        print(_out, *args, **kwargs, file=self.container)

    def save_logs(self):  # сохранение в файл
        logger_file = self.logged_input("File name:\n")
        with open(logger_file, "w") as log_file:
            for line in self.container.getvalue():
                log_file.write(line)
        print("The log has been saved.")


class Cards:
    dic_of_terms = {}

    def dict_to_str(self, hardest_card):  # конвертер словаря в сторку с ковычками у каждого элемента
        line = []
        for i in list(hardest_card.keys()):
            line.append('"' + str(i) + '"')
        return ', '.join(line)

    def counter_of_mistakes(self, element):  # счетчик ошибок при опросе
        self.dic_of_terms[element][1] = self.dic_of_terms[element][1] + 1

    def get_key(self, dic_of_terms, user_input):  # получение ключа по значению
        for key, value in dic_of_terms.items():
            if user_input == value[0]:
                return key

    def add(self):  # добавление новой карточки
        term = logger.logged_input(f'The term for card:\n')
        if term in self.dic_of_terms.keys():
            while term in self.dic_of_terms.keys():
                term = logger.logged_input(f'The term "{term}" already exists. Try again:\n')
        definition = logger.logged_input(f'The definition for card:\n')

        if definition in list(map(lambda x: x[0], self.dic_of_terms.values())):
            while definition in list(map(lambda x: x[0], self.dic_of_terms.values())):
                definition = logger.logged_input(f'The definition "{definition}" already exists. Try again:\n')
        self.dic_of_terms[term] = [definition, 0]

        logger.print_and_log(f'The pair ("{term}":"{definition}") has been added.')

    def remove(self, card_to_del):  # удаление карточки
        if card_to_del in self.dic_of_terms:
            del self.dic_of_terms[card_to_del]
            logger.print_and_log('The card has been removed.')
        elif card_to_del not in self.dic_of_terms:
            logger.print_and_log(f"Can't remove \"{card_to_del}\": there is no such card.")

    def import_file(self, file_with_cards):  # импортирование карточек из файла
        try:
            file = open(f'{file_with_cards}', 'r')
            cards = file.readlines()
            [self.dic_of_terms.update({i.split()[0]: [i.split()[1], int(i.split()[2])]}) for i in cards]
            logger.print_and_log(f'{len(cards)} cards have been loaded.')
        except FileNotFoundError:
            logger.print_and_log('File not found.')

    def export(self, file_for_export):  # экспортирование записанных карточек в файл

        file = open(file_for_export, 'w')
        for key, value in self.dic_of_terms.items():
            file.writelines(' '.join([key, value[0], str(value[1]) + '\n']))
        logger.print_and_log(f'{len(self.dic_of_terms)} cards have been saved.')
        file.close()

    def ask(self):  # функция для запуска опроса
        logger.print_and_log('How many times to ask?')
        times = int(logger.logged_input())
        for i in range(times):
            element = random.choice(list(self.dic_of_terms.keys()))
            logger.print_and_log(f'Print the definition of "{element}"')
            user_input = logger.logged_input()
            if user_input == self.dic_of_terms[element][0]:
                logger.print_and_log('Correct')
            elif user_input != self.dic_of_terms[element][0] and user_input in list(
                    map(lambda x: x[0], self.dic_of_terms.values())):
                cards.counter_of_mistakes(element)
                logger.print_and_log(
                    f'Wrong. The right answer is "{self.dic_of_terms[element][0]}", but your definition is correct for "{self.get_key(self.dic_of_terms, user_input)}".')
            elif self.dic_of_terms[element][0] == user_input:
                logger.print_and_log('Correct')
            else:
                cards.counter_of_mistakes(element)
                logger.print_and_log((f'Wrong. The right answer is "{self.dic_of_terms[element][0]}"', 'Correct!')[
                                         self.dic_of_terms[element][0] == user_input])

    def hardest_card(self):  # вывод названий самых сложных карточек
        hardest_card = {'key': ['value', 0]}
        for key, value in self.dic_of_terms.items():
            if value[1] > list(hardest_card.values())[0][1]:
                hardest_card.clear()
                hardest_card[key] = value
            elif value[1] == list(hardest_card.values())[0][1] and value[1] > 0:
                hardest_card[key] = value
        if len(hardest_card) == 1 and 'key' in hardest_card.keys():
            print('There are no cards with errors.')
        elif len(hardest_card) > 1:
            print(f'The hardest cards are {cards.dict_to_str(hardest_card)}.')
        elif len(hardest_card) == 1:
            print(
                f'The hardest card is {list(hardest_card.keys())[0]}. You have {list(hardest_card.values())[0][1]} errors answering it.')

    def reset_stats(self):  # обновление статистики ошибок
        for i in self.dic_of_terms:
            self.dic_of_terms[i][1] = 0
        print('Card statistics have been reset.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # ввод аргументов при работе с терминалом
    parser.add_argument("--import_from", type=str)
    parser.add_argument("--export_to", type=str)
    _args = parser.parse_args()

    logger = Logger()
    cards = Cards()

    if _args.import_from:
        file = _args.import_from
        cards.import_file(file)

    while True:
        user_choice = logger.logged_input(
            'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')  # ввод команды пользователя
        if user_choice == 'add':
            cards.add()

        elif user_choice == 'remove':
            cards.remove(logger.logged_input('Which card?\n'))

        elif user_choice == 'import':
            file = logger.logged_input('File name:\n')
            cards.import_file(file)

        elif user_choice == 'export':
            file_for_export = logger.logged_input('File name:\n')
            cards.export(file_for_export)

        elif user_choice == 'ask':
            cards.ask()

        elif user_choice == 'log':
            logger.save_logs()

        elif user_choice == 'hardest card':
            cards.hardest_card()

        elif user_choice == 'reset stats':
            cards.reset_stats()

        elif user_choice == 'exit':
            if _args.export_to:
                file_for_export = _args.export_to
                cards.export(file_for_export)
            logger.print_and_log('Bye bye!')
            break
