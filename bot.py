import asyncio
import random
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)




logging.basicConfig(
    level=logging.INFO, 
    filename = "mylog.log", 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
    )


#Блок обработки текста

def is_russian(q):
    logging.info('проверяю на русскость букв')
    for char in q:
        # Проверяем, является ли символ русской буквой
        if not ('а' <= char.lower() <= 'я' or char == 'ё' or char == 'Ё'):
            return False
    return True

def is_normal_name(stroka):
    logging.info('проверяю корректность введенных данных')
    a =True
    b = stroka.split()
    if len(b)>2:
        return False
    else:

        for i in b:

            a = a and is_russian(i)
        return a
       
def translit(text):
    logging.info('транслитерирую')
    tran_dict = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ы': 'y', 'ъ': 'ie', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
}
    a = text.lower().split()
    logging.info(a)
    char_list = [tran_dict[i] for i in a[0]]
    logging.info(char_list)  
    if len(a)>1:
        char_list2 = [tran_dict[i] for i in a[-1]]
        new_text =''.join(char_list).capitalize()+ ' '+ ''.join(char_list2).capitalize()
    else:
        new_text = ''.join(char_list).capitalize()
    logging.info(new_text)
    return new_text

#клавиатура 
def keybo():
      keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/start")]],
        resize_keyboard=True)
      return keyboard
        
# блок бота

@dp.message(Command('start'))
async def start_bottom(x: types.Message):
    
    user_name = x.from_user.first_name
    
    response = f"Здравствуйте {user_name}!\nНапишите имя и фамилию в любом порядке на русском языке и получите транслитерацию в соответсвии с Приказом МИД России от 12.02.2020 № 2113"
    
    keyboard = keybo()
  

    # Логируем
    logging.info(f"\n[{datetime.now().strftime('%H:%M:%S')}] {user_name}: {x.text}")
    logging.info(f"Бот: {response}")
    
    await x.answer(response, reply_markup=keyboard)


@dp.message()
async def auto_mess(y: types.Message):
    try:
        user_name = y.from_user.first_name
    
        user_text = y.text
        
        if is_normal_name(user_text):  
            response = translit(user_text)
        else: 
            response = f'Некорректный формат ввода данных'

        
        logging.info(f"\n[{datetime.now().strftime('%H:%M:%S')}] {user_name}: {user_text}")
        logging.info(f"Бот: {response}")
        
        photo = types.FSInputFile(random.choice(["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg", "photo11.jpg", "photo12.jpg", "photo13.jpg"]))
        await y.answer(response)
        await y.answer_photo(photo=photo)
    except:
        logging.warning('отправили сообщение которое поспринилось как текст и не смоголо обработаться')

async def main():
    logging.info("Бот запущен. Логирование включено...")
    print("Бот запущен. Логирование включено...")
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())