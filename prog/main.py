import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Подключение к базе данных SQLite прошло успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    return connection


connection = create_connection(".\\pet_store.sql")
cursor = connection.cursor()


class Pet_store():
    def __init__(self, animals=[]):
        self.animals = []
        for pet in animals:
            self.animals += [pet]
        self.DB_init()
        return

    def DB_init(self):
        querry = """
        CREATE TABLE IF NOT EXISTS pets (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          type TEXT NOT NULL,
          age INTEGER,
          commands TEXT,
          class TEXT
        );
        """
        try:
            cursor.execute(querry)
            connection.commit()
            # print('success')
        except Error as e:
            print(f"error: {e}")
        querry = 'select count(*) from pets'
        cursor.execute(querry)
        res = cursor.fetchall()
        print(res[0][0])
        if res[0][0] == 0:
            for pet in self.animals:
                querry = f'insert into pets (type, age, commands, class) values ("{pet.type}", {pet.age}, "{str(pet.commands)}", "{pet.animal_class}")'
                cursor.execute(querry)
                connection.commit()
        else:
            return
        return

    def new_animal(self, pet):
        self.animals += [pet]
        querry = f'insert into pets (type, age, commands, class) values ("{pet.type}", {pet.age}, "{str(pet.commands)}", "{pet.animal_class}")'
        cursor.execute(querry)
        connection.commit()
        return

    def check_animals_list(self):
        querry = 'select id, type from pets'
        cursor.execute(querry)
        res = cursor.fetchall()
        for line in res:
            print(line)
        return

    def check_commands(self, number):
        querry = f'select commands from pets where id={number}'
        cursor.execute(querry)
        res = cursor.fetchall()
        return res[0][0]

    def add_command(self, number, command):
        commands = str(self.check_commands(number)).replace('[', '').replace(']', '').replace("'", '').replace(" ",
                                                                                                               "").split(
            ',')
        print(commands)
        commands += [command]
        querry = f'update pets set commands="{str(commands)}" where id = {number}'
        print(querry)
        cursor.execute(querry)
        connection.commit()


class Animal():
    def __init__(self, type="Cat", commands=['sleep', 'jump', 'eat'], age=0):
        self.type = type
        self.commands = commands
        self.age = age
        self.animal_class = self.check_animal_class(self)
        return

    def check_animal_class(self, animal):
        if animal.type in ['Cat', 'Dog', 'Rat', 'Hamster']:
            return 'Domestic'
        else:
            return 'Cattle'

    def get_pet_commands(self):
        return self.commands

    def set_pet_commands(self, new_command):
        self.commands += [new_command]
        return


Cat = Animal("Cat", ['sleep', 'jump', 'eat'], age=3)
Dog = Animal("Dog", ['run', 'jump', 'play'], age=5)
Rat = Animal("Rat", ['hide', 'run', 'squeak'], age=2)
Cow = Animal("Cow", ['eat', 'walk', 'drink'], age=13)
Capri = Animal("Capri", ['run', 'walk', 'growl'], age=7)
Pig = Animal("Pig", ['eat', 'wash', 'play'], age=1)


def navigation():
    while (1):
        print("please select an option:\n1. Завести новое животное\n2. Увидеть список команд животного\n"
              "3. Обучить животное новым командам\n4. Вывести полный список животных\n"
              "0. Выйти из программы")
        n = input()
        if n == '0':
            return 0
        if n == '1':
            print("Введите тип нового животного")
            type = input()
            print("Введите список команд нового животного")
            commands = input()
            print("Введите возраст нового животного")
            age = int(input())
            New_pet = Animal(type, commands, age)
            MyStore.new_animal(New_pet)
        if n == '2':
            MyStore.check_animals_list()
            print("Выберите номер животного для просмотра комманд")
            num = int(input())
            print(MyStore.check_commands(num))
        if n == '3':
            MyStore.check_animals_list()
            print("Выберите номер животного для просмотра комманд")
            num = int(input())
            print("Введите новую команду для питомца")
            command = input()
            MyStore.add_command(num, command)
        if n == '4':
            MyStore.check_animals_list()


MyStore = Pet_store([Cat, Dog, Rat, Cow, Capri, Pig])
# MyStore = Pet_store()
MyStore.check_animals_list()
navigation()
