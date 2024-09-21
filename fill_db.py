from db import WordsDatabase
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
database = WordsDatabase(name=config['DATABASE']['NAME'],
                         user=config['DATABASE']['USER'],
                         password=config['DATABASE']['PASSWORD'])

database.create_tables()
database.fill_table_main_words('Привет', 'Hola')
database.fill_table_main_words_variants(1, ['Hora', 'Ola', 'Hilo'])

