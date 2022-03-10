import random


class Cards:
    dic_of_terms = {}

    def get_key(self, dic_of_terms, user_input):
        for key, value in dic_of_terms.items():
            if user_input == value:
                return key

    def add(self):
        term = input(f'The term for card:\n')
        if term in self.dic_of_terms.keys():
            while term in self.dic_of_terms.keys():
                term = input(f'The term "{term}" already exists. Try again:\n')
        definition = input(f'The definition for card:\n')
        if definition in self.dic_of_terms.values():
            while definition in self.dic_of_terms.values():
                definition = input(f'The definition "{definition}" already exists. Try again:\n')
        self.dic_of_terms[term] = definition
        print(f'The pair ("{term}":"{definition}") has been added.')

    def remove(self, card_to_del):
        if card_to_del in self.dic_of_terms:
            del self.dic_of_terms[card_to_del]
            print('The card has been removed.')
        elif card_to_del not in self.dic_of_terms:
            print(f"Can't remove \"{card_to_del}\": there is no such card.")

    def import_file(self, file_with_cards):
        try:
            file = open(f'{file_with_cards}', 'r')
            cards = file.readlines()
            [self.dic_of_terms.update({i.split()[0]: i.split()[1]}) for i in cards]
            print(f'{len(cards)} cards have been loaded.')
        except FileNotFoundError:
            print('File not found.')

    def export(self, file_for_export):

        file = open(file_for_export, 'w')
        for key, value in self.dic_of_terms.items():
            file.writelines(' '.join([key, value + '\n']))
        print(f'{len(self.dic_of_terms)} cards have been saved.')
        file.close()

    def ask(self):
        print('How many times to ask?')
        times = int(input())
        for i in range(times):
            element = random.choice(list(self.dic_of_terms.keys()))
            print(f'Print the definition of "{element}"')
            user_input = input()
            if user_input == self.dic_of_terms[element]:
                print('Correct')
            elif user_input != self.dic_of_terms[element] and user_input in self.dic_of_terms.values():
                print(
                    f'Wrong. The right answer is "{self.dic_of_terms[element]}", but your definition is correct for "{self.get_key(self.dic_of_terms, user_input)}".')
            else:
                print((f'Wrong. The right answer is "{self.dic_of_terms[element]}"', 'Correct!')[
                          self.dic_of_terms[element] == user_input])


cartochki = Cards()
while True:
    user_choice = input('Input the action (add, remove, import, export, ask, exit):\n')
    if user_choice == 'add':
        cartochki.add()
    elif user_choice == 'remove':
        cartochki.remove(input('Which card?\n'))
    elif user_choice == 'import':
        file = input('File name:\n')
        cartochki.import_file(file)
        pass
    elif user_choice == 'export':
        file_for_export = input('File name:\n')
        cartochki.export(file_for_export)
    elif user_choice == 'ask':
        cartochki.ask()
    elif user_choice == 'exit':
        print('Bye bye!')
        break
