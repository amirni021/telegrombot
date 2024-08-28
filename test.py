import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sqlite3

bot = telebot.TeleBot("7147645366:AAF1eXYyGyqauoR-cEwoynulyC8cFWXnj-8")



#گرفتن چندین ورودی
'''
@bot.message_handler(commands=["start"])
def first(message):
  bot.send_message(message.chat.id, "whats your name?")
  bot.register_next_step_handler(message, firstname)

def firstname(message):
  if message.content_type == 'text':
    name = message.text
    bot.send_message(message.chat.id, f"hello {name}\n how old are you? ")
    bot.register_next_step_handler(message, agef)
  else:
        bot.send_message(message.chat.id, "please enter text")

def agef(message):
   if message.content_type == 'text':
    age = message.text
    bot.send_message(message.chat.id, f"you are {age}y/o\n welcome!")
   else: bot.send_message(message.chat.id, "please enter text")
'''
#فرستادن پیام به اعضا
'''
user_id = []

@bot.message_handler(commands=["start"])
def gettingid(message):
  bot.send_message(message.chat.id, "welcome")
  if message.chat.id not in user_id:
    user_id.append(message.chat.id)

@bot.message_handler(commands=["ABUDID"])
def sendingmsg(message):
  for id in user_id:
    bot.send_message(id, f"{id}")
'''
#کال بک کردن دکمه های شیشه ای
'''
button1 = InlineKeyboardButton(text= "سایت", url= "https://uswr.ac.ir/")
button2 = InlineKeyboardButton(text= "نمره", callback_data= "btn2")
inline_keybord = InlineKeyboardMarkup(row_width = 1)
inline_keybord.add(button1, button2)

@bot.message_handler(commands=["start"])
def buttons(message):
  bot.send_message(message.chat.id, "welcome",reply_markup= inline_keybord)
@bot.callback_query_handler(func=lambda call : True)
def callBack(call):
  if call.data == "btn2":
    bot.answer_callback_query(call.id, "نمره شما 20", show_alert=True)
'''
#ساختن دکمه در منو
'''
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
reply_keyboard.add("AAA", "BBB")

@bot.message_handler(commands=["start"])
def menu(message):
  bot.send_message(message.chat.id, "welcome", reply_markup=reply_keyboard)

@bot.message_handler(func=lambda message: True)
def checkbutton(message):
  if message.text == "AAA":
    bot.reply_to(message, "AAA is empty")
  elif message.text == "BBB":
    bot.reply_to(message, "BBB is empty")
  else: bot.send_message(message.chat.id, "this is not available")
'''

#ساختن دیتا بیس


with sqlite3.Connection("usert.db") as connection:
  cursor = connection.cursor()
  create_table_query ="""
    CREATE TABLE IF NOT EXISTS user(
    id integer primary key,
    name text
    )
  """
  cursor.execute(create_table_query)

def mainmenu():
  keyboard = InlineKeyboardMarkup(row_width=1)
  button1 = InlineKeyboardButton(text="ثبتنام", callback_data= "register")
  button2 = InlineKeyboardButton(text="گروه بندی", callback_data="reserve")
  keyboard.add(button1, button2)
  return keyboard

@bot.message_handler(commands=["start"])
def askingcont(message):
  bot.send_message(message.chat.id, "welcome", reply_markup= mainmenu())    


def fetchingData():
    fetch_data_query = """
    SELECT id, name FROM user
    """
    with sqlite3.connect("usert.db") as connection:  # Open a new connection
        cursor = connection.cursor()
        cursor.execute(fetch_data_query)
        return cursor.fetchall()
 
 #ارسال پیام به اعضا 
@bot.message_handler(commands=["all"])
def send_amirn(message):
    bot.send_message(message.chat.id, "پیام موردنظر راارسال کنید")
    bot.register_next_step_handler(message, broadcast)
  
def broadcast(message):
      try:
        rows = fetchingData()  # Call the function
        numbers = []
        for row in rows:
            numbers.append(row[0])

        for num in numbers:
          bot.send_message(num,message.text)

      except Exception as e:
         print(f"failed to send message.{e}")
  

def makingData(message):
    try:
      name = message.text

      with sqlite3.connect("usert.db") as connection:  # Open a new connection
          cursor = connection.cursor()
          insert_data_query = """
          INSERT INTO user(id, name)
          VALUES(?, ?)
          """
          data = (message.chat.id, name)
          cursor.execute(insert_data_query, data)
          connection.commit()

      bot.send_message(message.chat.id, "ثبتنام انجام شد")
    except sqlite3.IntegrityError:
       bot.send_message(message.chat.id, "شما قبلا ثبتنام کرده اید")

def res_menu():
   keyboard = InlineKeyboardMarkup(row_width=1)
   butt1 = InlineKeyboardButton(text="شنبه 1/7", callback_data="res1")
   butt2 = InlineKeyboardButton(text="شنبه 2/7", callback_data="res2")
   butt3 = InlineKeyboardButton(text="شنبه 3/7", callback_data="res3")
   butt4 = InlineKeyboardButton(text="شنبه 4/7", callback_data="res4")
   Return = InlineKeyboardButton(text="برگشت", callback_data="retrMM")
   keyboard.add(butt1, butt2, butt3, butt4, Return)
   return keyboard


@bot.message_handler(commands=["joz"])
def sendJ(message):
   bot.send_message(message.chat.id, "جزوه را ارسال کنید")
   bot.register_next_step_handler(message, handleJ)

def handleJ(message):
   jozve = message.document.file_id
   rows = fetchingData()
   numbers = []
   for row in rows:
      numbers.append(row[0])
   for num in numbers:
      bot.send_document(num, jozve)


res1 = {"sub" : "", "group": ""}
res2 = {"sub" : "", "group": ""}
res3 = {"sub" : "", "group": ""}
res4 = {"sub" : "", "group": ""}

def sres1(message):
   if not res1["sub"]:
    sub = message.text
    res1["sub"] = sub
    bot.send_message(message.chat.id, "اسامی اعضا رو بفرسیتد")
    bot.register_next_step_handler(message, gres1)
   elif res1["sub"]:
      bot.send_message(message.chat.id, "از قبل رزرو شده", reply_markup= res_menu())
  
def gres1(message):
   gr = message.text
   res1["group"] = gr
   bot.reply_to(message, "رزرو شد")
   reservation(message)
   bot.send_message(message.chat.id, "منوی اصلی", reply_markup=mainmenu())
     


def sres2(message):
   if not res2["sub"]:
    sub = message.text
    res2["sub"] = sub
    bot.send_message(message.chat.id, "اسامی اعضا رو بفرسیتد")
    bot.register_next_step_handler(message, gres2)
   elif res2["sub"]:
      bot.send_message(message.chat.id, "از قبل رزرو شده", reply_markup= res_menu())
  
def gres2(message):
   gr = message.text
   res2["group"] = gr
   bot.reply_to(message, "رزرو شد")
   reservation(message)
   bot.send_message(message.chat.id, "منوی اصلی", reply_markup=mainmenu())
     

def sres3(message):
    if not res3["sub"]:
      sub = message.text
      res3["sub"] = sub
      bot.send_message(message.chat.id, "اسامی اعضا رو بفرسیتد")
      bot.register_next_step_handler(message, gres3)
    elif res3["sub"]:
        bot.send_message(message.chat.id, "از قبل رزرو شده", reply_markup= res_menu())
  
def gres3(message):
   gr = message.text
   res3["group"] = gr
   bot.reply_to(message, "رزرو شد")
   reservation(message)
   bot.send_message(message.chat.id, "منوی اصلی", reply_markup=mainmenu())
     

def sres4(message):
   if not res4["sub"]:
    sub = message.text
    res4["sub"] = sub
    bot.send_message(message.chat.id, "اسامی اعضا رو بفرسیتد")
    bot.register_next_step_handler(message, gres4)
   elif res4["sub"]:
      bot.send_message(message.chat.id, "از قبل رزرو شده", reply_markup= res_menu())
  
def gres4(message):
   gr = message.text
   res4["group"] = gr
   bot.reply_to(message, "رزرو شد")
   reservation(message)
   bot.send_message(message.chat.id, "منوی اصلی", reply_markup=mainmenu())
     





def reservation(message):
   bot.send_message(message.chat.id, f"""
    شنبه 1/7. موضوع:  {res1['sub']} - اعضا:  {res1['group']}\n
    شنبه 2/7. موضوع:  {res2['sub']} - اعضا:  {res2['group']}\n
    شنبه 3/7. موضوع:  {res3['sub']} - اعضا:  {res3['group']}\n
    شنبه 4/7. موضوع:  {res4['sub']} - اعضا:  {res4['group']}\n
  """)
   
@bot.callback_query_handler(func= lambda call : True)
def callback(call):
   if call.data == "register":
      bot.send_message(call.message.chat.id, "اسمت جیه")
      bot.register_next_step_handler(call.message, makingData)

   elif call.data == "reserve":
      bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="روز مدنظر خود را مشخص کنید", reply_markup= res_menu())

   elif call.data == "res1":
      bot.send_message(call.message.chat.id, "موضوع چیه؟")
      bot.register_next_step_handler(call.message, sres1)

   elif call.data == "res2":
      bot.send_message(call.message.chat.id, "موضوع چیه؟")
      bot.register_next_step_handler(call.message, sres2)

   elif call.data == "res3":
      bot.send_message(call.message.chat.id, "موضوع چیه؟")
      bot.register_next_step_handler(call.message, sres3)

   elif call.data == "res4":
      bot.send_message(call.message.chat.id, "موضوع چیه؟")
      bot.register_next_step_handler(call.message, sres4)

   elif call.data == "retrMM":
      bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="برگشتید منوی اصلی", reply_markup= mainmenu())
      


print("Bot is running...")

# ساختن منوایراد
'''
def main_menu():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True , row_width= 2)
  button1 = KeyboardButton(text="menu 1" callback_data= "menu1")
  button2 = keyboard(text = "menu 2", callback_data= "menu2")
  keyboard.add(button1, button2)
  return keyboard

def menu1():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text="submenu 1.1", callback_data= "subm1.1")
  button2 = KeyboardButton(text="submwnu 1.2", callback_data= "sunm1.2")
  Retrun = KeyboardButton(text="return", callback_data= "returMM")
  keyboard.add(button1, button2, Retrun)
  return keyboard

def smen1_1():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text= "buy1")
  button2 = ReplyKeyboardMarkup(text= "buy2")
  Retrun = KeyboardButton(text="return", callback_data= "returM1")
  keyboard.add(button1, button2, Retrun)
  return keyboard

def smen1_2():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text= "buy1")
  button2 = ReplyKeyboardMarkup(text= "buy2")
  Retrun = KeyboardButton(text="return", callback_data= "returM1")
  keyboard.add(button1, button2, Retrun)
  return keyboard

def menu2():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text="submenu 2.1", callback_data= "subm2.1")
  button2 = KeyboardButton(text="submwnu 2.2", callback_data= "sunm2.2")
  Retrun = KeyboardButton(text="return", callback_data= "returMM")
  keyboard.add(button1, button2, Retrun)
  return keyboard

def smen2_1():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text= "buy1")
  button2 = ReplyKeyboardMarkup(text= "buy2")
  Retrun = KeyboardButton(text="return", callback_data= "returM2")
  keyboard.add(button1, button2, Retrun)
  return keyboard

def smen2_2():
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  button1 = KeyboardButton(text= "buy1")
  button2 = ReplyKeyboardMarkup(text= "buy2")
  Retrun = KeyboardButton(text="return", callback_data= "returM2")
  keyboard.add(button1, button2, Retrun)
  return keyboard

@bot.message_handler(commands=["start"])
def intro(message):
  bot.send_message(message.chat.id, "you are in the main menu. choose one", reply_markup=main_menu)

@bot.callback_query_handler(funct=lambda call: True)
def callback(call):
  #main menu
  if call.data == "menu1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="you entered menu 1", reply_markup= menu1)
  elif call.data == "menu2":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="you entered menu 2", reply_markup= menu2)
  elif call.data == "returnMM":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="you are in the main menu. choose one ", reply_markup= main_menu)
  #menu 1
  elif call.data == "smenu1.1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="choose one", reply_markup= smen1_1)
  elif call.data == "smenu1.1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="choose one", reply_markup= smen1_2)
  elif call.data == "returnM1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="you entered menu 1", reply_markup= menu1)
  #menu2
  elif call.data == "smenu2.1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="choose one", reply_markup= smen2_1)
  elif call.data == "smenu2.1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="choose one", reply_markup= smen2_2)
  elif call.data == "returnM2":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text="you entered menu 2", reply_markup= menu2)
 
# Main Menu
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Menu 1")
    button2 = KeyboardButton(text="Menu 2")
    keyboard.add(button1, button2)
    return keyboard

# Menu 1
def menu1():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Submenu 1.1")
    button2 = KeyboardButton(text="Submenu 1.2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

def smen1_1():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Buy 1")
    button2 = KeyboardButton(text="Buy 2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

def smen1_2():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Buy 1")
    button2 = KeyboardButton(text="Buy 2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

# Menu 2
def menu2():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Submenu 2.1")
    button2 = KeyboardButton(text="Submenu 2.2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

def smen2_1():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Buy 1")
    button2 = KeyboardButton(text="Buy 2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

def smen2_2():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton(text="Buy 1")
    button2 = KeyboardButton(text="Buy 2")
    return_button = KeyboardButton(text="Return")
    keyboard.add(button1, button2, return_button)
    return keyboard

@bot.message_handler(commands=["start"])
def intro(message):
    bot.send_message(message.chat.id, "You are in the main menu. Choose one:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def menu_selection(message):
    if message.text == "Menu 1":
        bot.send_message(message.chat.id, "You entered Menu 1", reply_markup=menu1())
    elif message.text == "Menu 2":
        bot.send_message(message.chat.id, "You entered Menu 2", reply_markup=menu2())
    elif message.text == "Submenu 1.1":
        bot.send_message(message.chat.id, "Choose one:", reply_markup=smen1_1())
    elif message.text == "Submenu 1.2":
        bot.send_message(message.chat.id, "Choose one:", reply_markup=smen1_2())
    elif message.text == "Submenu 2.1":
        bot.send_message(message.chat.id, "Choose one:", reply_markup=smen2_1())
    elif message.text == "Submenu 2.2":
        bot.send_message(message.chat.id, "Choose one:", reply_markup=smen2_2())
    elif message.text == "Return":
        bot.send_message(message.chat.id, "You are in the main menu. Choose one:", reply_markup=main_menu())
'''
bot.polling()