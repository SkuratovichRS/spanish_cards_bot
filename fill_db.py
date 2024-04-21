from db import WordsDatabase
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
database = WordsDatabase(name=config['DATABASE']['NAME'],
                         user=config['DATABASE']['USER'],
                         password=config['DATABASE']['PASSWORD'])

database.create_tables()
database.fill_table_main_words('Привет', 'Hello')
database.fill_table_main_words_variants(1, ['Hell', 'All', 'Low'])
database.fill_table_main_words('Пока', 'Bye')
database.fill_table_main_words_variants(2, ['By', 'Buy', 'Bee'])
database.fill_table_main_words('Он', 'He')
database.fill_table_main_words_variants(3, ['She', 'It', 'Him'])
database.fill_table_main_words('Красный', 'Red')
database.fill_table_main_words_variants(4, ['Blue', 'Green', 'White'])
database.fill_table_main_words('Солнце', 'Sun')
database.fill_table_main_words_variants(5, ['Moon', 'Soon', 'Sky'])
database.fill_table_main_words('Машина', 'Car')
database.fill_table_main_words_variants(6, ['Bike', 'Bus', 'Care'])
database.fill_table_main_words('Имя', 'Name')
database.fill_table_main_words_variants(7, ['None', 'Surname', 'Numb'])
database.fill_table_main_words('Голова', 'Head')
database.fill_table_main_words_variants(8, ['Arm', 'Hand', 'Leg'])
database.fill_table_main_words('Человек', 'Person')
database.fill_table_main_words_variants(9, ['Woman', 'Son', 'Dog'])
database.fill_table_main_words('День', 'Day')
database.fill_table_main_words_variants(10, ['Night', 'World', 'Morning'])
