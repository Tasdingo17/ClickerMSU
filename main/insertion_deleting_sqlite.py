"""D"""

import sqlite3
#from matplotlib.pyplot import text
#import pandas
#from sqlalchemy import create_engine
import telebot
from restricted_area import token_crypto
import io
import json
import urllib
from urllib.request import urlopen
import ssl



# engine = create_engine('sqlite://', echo=False)

# df = pandas.read_csv(csvfile)
# df.to_sql("MSK_test", con=engine, if_exists='append', index=False)




API_TOKEN = token_crypto

bot = telebot.TeleBot(API_TOKEN)

global_data_chat = 721641425
global_data_message = 430
global_file_id = "BQACAgIAAxkDAAIBrmKbrXkKo_0d3Nbo-Cmr1Zpy0_fWAALzGwACYDDgSFN_tbcimLj3JAQ"

def get_data():
    print(global_file_id)
    file_data = bot.get_file(global_file_id)
    print("ok")
    # Получаем файл по url
    file_data_path = file_data.file_path
    print(file_data_path)
    print("ok")
    file_url_data = bot.get_file_url(global_file_id)
    print("ok")
    print(file_url_data)
    # Считываем данные с файла
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(file_url_data, context=context) as f:
        json_file = f.read().decode('utf-8')
    #json_file= urlopen(file_url_data).read()
    print("ok")

    # Переводим данные из json в словарь и возвращаем
    return json.loads(json_file)

@bot.message_handler(content_types=["document", "video", "audio"])
def handle_files(message):
  document_id = message.document.file_id
  file_info = bot.get_file(document_id)
  print(document_id) # Выводим file_id
  print(f'http://api.telegram.org/file/bot{token_crypto}/{file_info.file_path}') 
  bot.send_message(message.chat.id, document_id) 

@bot.message_handler(commands = ["update"])
def update_data(messg):
    # server case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    # data = get_data()
    # cursor.executemany("INSERT INTO users VALUES (?,?,?)", data)
    # connect.commit() 

    # local case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    admin_id = global_data_chat
    config_id = global_data_message
    try:
        # Обновляем  наш файл с данными
        bot.edit_message_media(chat_id  = global_data_chat, message_id = global_data_message, media = telebot.types.InputMediaDocument(io.StringIO(str_data)))

    except Exception as ex:
        print(ex)

    #print(get_data())

"""Use this for initial message for bot-server"""
@bot.message_handler(commands = ["save"])
def save_data(messg):
    # server case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    # data = get_data()
    # cursor.executemany("INSERT INTO users VALUES (?,?,?)", data)
    # connect.commit() 

    # local case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    send_document = bot.send_document(messg.chat.id, io.StringIO(str_data))
    bot.send_message(messg.chat.id, 'admin_id = {}'.format(messg.chat.id))
    bot.send_message(messg.chat.id, 'config_id = {}'.format(messg.message_id+1))
    admin_id = messg.chat.id
    config_id = messg.message_id+1
    global global_data_chat 
    global global_data_message 
    global global_file_id
    global_data_chat = messg.chat.id
    global_data_message = messg.message_id+1
    global_file_id = send_document.document.file_id
    bot.send_message(messg.chat.id, 'file_id = {}'.format(global_file_id))

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()  # or use fetchone()
    try:
        # Переводим словарь в строку
        str_data=json.dumps(data)

        # Обновляем  наш файл с данными
        bot.edit_message_media(chat_id  = admin_id, message_id = config_id, media = telebot.types.InputMediaDocument(io.StringIO(str_data)))

    except Exception as ex:
        print(ex)

@bot.message_handler(commands = ["register"])
def register(messg, username_in = None, password_in = None): 
    # server case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    data = get_data()
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", data)
    connect.commit() 

    # local case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    # connect.commit() 


    # регистрация
    print("Регистрация: ")
    if username_in == None:
        username_in = str(input("username: "))

    # includes case when registration initiated with telegram app
    try:
        user_id = [messg.chat.id]
    except:
        user_id = [0]

    cursor.execute(f"SELECT username FROM login_id WHERE username = ?", (username_in,))
    name_out = cursor.fetchone()
    if name_out is None: 
        if password_in == None: 
            password_in = str(input("password: "))
        cursor.execute("INSERT INTO login_id (id, username, password) VALUES (?, ?, ?);", (user_id[0], username_in, password_in))
        connect.commit() 
        print("Done")
        update_data(None)
        cursor.execute("SELECT id, username FROM login_id ORDER BY id DESC LIMIT 10;") 
        results_10 = cursor.fetchall()
        #cursor.execute(f"SELECT ROW_NUMBER() over(ORDER BY id DESC) num, id, username FROM login_id  WHERE username = (?) ORDER BY username;", (username_in,))
        cursor.execute("SELECT id, username, ROW_NUMBER() over(ORDER BY id DESC) AS Row FROM login_id;")
        #cursor.executemany("SELECT id, username, Row FROM login_id WHERE username = (?);", (username_in,))

        user_place = cursor.fetchall()
        user_place = [i for i in user_place if i[1] == username_in]
        #connect.commit() 
        #cursor.execute(f"SELECT username, password FROM login_id WHERE username = ?", (username_in,))
        return results_10, user_place
    else: 
        print("Same user also exists...")
        return None, None

    


@bot.message_handler(commands = ["sighin"])
def sighin(messg): 

    # server case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    data = get_data()
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", data)
    connect.commit() 

    # local case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);") 
    # connect.commit() 

    #вход с логином и паролем
    username_in = str(input("username: "))
    cursor.execute(f"SELECT username, password FROM login_id WHERE username = ?", (username_in,))
    name_out = cursor.fetchone()
    if name_out is None: 
        bot.send_message(messg.chat.id, "Вы ещё не регестрировались.")
        print("Вы ещё не регестрировались.")
    else: 
        password_in = str(input("password: "))
        if name_out[1] == password_in:
            print("Вы успешно вошли")
            #...
        else: 
            print("Пароль неверный")

    #

    # if people_id_data is None: 
    #     user_id = [messg.chat.id]
    #     cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
    #     connect.commit() 
    # else: 
    #     bot.send_message(messg.chat.id, "Уже есть такой")

# @bot.message_handler(commands = ["find"])
# def start(messg): 
#     connect = sqlite3.connect('./DB/test.db')
#     cursor = connect.cursor()




def listener(messages):  
    print(type(messages[0].de_json))
    #print(dir(messages[0].de_json))
    #print(messages[0].de_json())




@bot.message_handler(commands = ["delete"])
def delete(messg): 
    bot.send_message(messg.chat.id, f"Deleting")
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    people_id = messg.chat.id 
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    people_id_data = cursor.fetchone()
    
    

    if people_id_data is None: 
        bot.send_message(messg.chat.id, "NO SUCH USER IN DATABASE") 
    else: 
        cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
        bot.send_message(messg.chat.id, f"Deleted user {people_id}")
        connect.commit() 
    
    connect.commit() 



bot.set_update_listener(listener)
bot.polling()
