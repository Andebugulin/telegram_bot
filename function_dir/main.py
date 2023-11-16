import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
import json
from dotenv import load_dotenv
import os
from telebot import types
import datetime
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states_dir.statesform import StepsForm
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json
import random
from classes_dir.to_do_list_class import ToDoList
from classes_dir.task_class import Task
from markups_dir.markups import *



# * loading env, 
# * you can create .env file and put there your 'BOT_TOKEN' variable
load_dotenv()

# * logging helps to check follow whether everything is working properly.
logging.basicConfig(level=logging.INFO)

# Initialize your Telegram Bot Token
# ! don't you ever put a token to the code !!!!!!
bot_token = str(os.getenv("BOT_TOKEN"))

# Initialize the bot
bot = Bot(token=bot_token)

# dispatcher
dp = Dispatcher()

good_night_sentences = {
    "Wishing you a peaceful night filled with sweet dreams.",
    "May the stars whisper lullabies to guide you into a restful sleep.",
    "As the night falls, may your worries fade away, and your dreams be filled with joy.",
    "Sending you a blanket of stars to keep you warm tonight.",
    "Close your eyes and let the serenity of the night embrace you.",
    "Sleep tight, dream big, and wake up ready to conquer tomorrow.",
    "May your dreams be as beautiful as the night sky.",
    "Good night! Rest your mind and rejuvenate your spirit for a new day.",
    "Wishing you a night so peaceful that even the moonlight pauses to admire.",
    "Sweet dreams are made of starlight and whispers of the night.",
    "May your sleep be deep, and your dreams be delightful.",
    "Drift into the night, and let the magic of dreams unfold.",
    "The night is a canvas, and your dreams are the masterpiece.",
    "As you lay down to sleep, remember that tomorrow is a new canvas waiting for your brushstroke.",
    "Close your eyes, take a deep breath, and let the night cradle you in its soothing embrace.",
    "Wishing you a night filled with tranquility and the promise of a brighter tomorrow.",
    "Dreams are the night's way of showing you a preview of the beauty that tomorrow holds.",
    "Sleep peacefully, knowing that you are cherished and valued.",
    "The night sky is a testament to the beauty that exists even in the darkness. Sweet dreams!",
    "As the night unfolds, may your dreams be filled with joy, love, and all things good.",
    "Embrace the quiet of the night as you drift into a world of dreams.",
    "May your sleep be as peaceful as a moonlit lake.",
    "Dreamland awaits with open arms, ready to transport you to magical realms.",
    "Close your eyes, and let the night unfold its mysteries in your dreams.",
    "As the stars twinkle above, may your dreams sparkle with joy.",
    "Wishing you a night filled with the gentle whispers of the wind and the rustling of leaves.",
    "Sleep like a baby, wrapped in the warmth of serenity and love.",
    "May your dreams be a tapestry woven with threads of happiness and fulfillment.",
    "Good night! Tomorrow is a blank page; tonight, rest well to write a beautiful story.",
    "Let go of today's worries; tomorrow is a new chapter waiting to be written.",
    "In the realm of dreams, may you find the answers to your heart's desires.",
    "The night sky is a celestial dance; let your dreams join the cosmic ballet.",
    "Drift into the night like a leaf carried by a gentle breeze, and let your dreams soar.",
    "As the world sleeps, may your dreams be a symphony of peace and harmony.",
    "Sleep with the knowledge that you are surrounded by love and positivity.",
    "Good night! May your dreams be the stepping stones to a brighter and happier future.",
    "Close your eyes, and let the moonlight guide you to a land of enchantment.",
    "Wishing you a night filled with the soft melody of crickets and the rustling of leaves.",
    "As the night deepens, may your dreams reach new heights of creativity and inspiration.",
    "Sleep is the best meditation; may your night be a peaceful journey within.",
    "Dreams are the stars of the night; may yours shine the brightest.",
    "Good night! Tomorrow is a canvas; tonight, rest well to paint a masterpiece.",
    "May the night wrap you in its comforting embrace, and your dreams be a source of joy.",
    "Close your eyes and let the night unfold its tapestry of dreams just for you.",
    "Wishing you a night filled with the magic of possibility and the promise of tomorrow.",
    "May the moonlight be your guide as you journey into the realm of dreams.",
    "As you sleep, may the night weave a blanket of peace around your soul.",
    "Good night! Rest your body, recharge your spirit, and wake up ready to conquer the day.",
    "May the night be a sanctuary where your mind finds solace and your dreams find wings.",
    "Close your eyes, and let the night be a canvas for the most beautiful dreams to paint.",
    "Wishing you a night filled with the sweet fragrance of dreams and the gentle touch of sleep."
}

pickup_lines = {
    "If you were a puzzle, you'd be the missing piece I've been searching for.",
    "Are you a bookstore? Because every time I read you, I discover something new.",
    "Is your name Espresso? Because you’re short, strong, and keep me up all night.",
    "Do you have a name or can I call you mine? I promise I won't write it in my notebook... unless you want me to.",
    "Are you a compass? Because I always find my direction when I'm with you.",
    "If you were a song, you'd be the melody that never leaves my mind.",
    "Are you a scientist? Because you just made my heart undergo a chemical reaction.",
    "Do you have a sunburn, or are you always this electric?",
    "Is your name Autumn? Because you've just fallen for me.",
    "Are you a time traveler? Because I can see you in my future for a long time.",
    "If you were a cookie, you'd be a 'fortune'-ate one.",
    "Do you have a name, or can I call you mine? Because I'm claiming you as my happiness.",
    "Are you a telescope? Because every time I look at you, my world expands.",
    "If beauty were time, you'd be an everlasting moment.",
    "Do you have a Band-Aid? Because I just hurt my knee falling... for you.",
    "Is your name Atlas? Because you've shouldered your way into my heart.",
    "Are you a garden? Because I'm digging you.",
    "If you were a song, you'd be a symphony of perfection.",
    "Do you have a sunburn, or are you always this fiery?",
    "Is your name Cinderella? Because when you walked in, time stood still.",
    "Are you a painter? Because you've colored my world with joy.",
    "If you were a star, you'd be the constellation of my dreams.",
    "Do you have a map? Because I just got lost in your eyes... again.",
    "Is your name Winter? Because you make my heart feel ice-struck.",
    "Are you a sculptor? Because you've crafted the masterpiece of my desires.",
    "If you were a planet, you'd be the one I'd revolve around.",
    "Do you have a name, or can I call you mine? Because I'm ready to start our story together.",
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Do you have a map? I keep getting lost in your eyes.",
    "If you were a vegetable, you'd be a cute-cumber!",
    "Are you a Wi-Fi signal? Because I'm feeling a connection.",
    "Do you have a sunburn, or are you always this hot?",
    "Can I follow you home? Cause my parents always told me to follow my dreams.",
    "Are you a camera? Every time I look at you, I smile.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Excuse me, but I think the stars tonight are outshone by your smile.",
    "If you were a cat, you'd purr-fect.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Can I take you out for dinner? Because I can't seem to get you out of my mind.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Are you a time traveler? Because I can't imagine my future without you.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Can I borrow a map? I keep getting lost in your eyes.",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Are you a loan? Because you have my interest.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is this the Hogwarts Express? Because it feels like you and I are headed somewhere magical.",
    "If beauty were time, you’d be an eternity.",
    "Are you a time traveler? Because I can't seem to get you out of my future.",
    "Is your name Wi-fi? Because I'm feeling a connection.",
    "Do you have a pencil? Because I want to erase your past and write our future.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Do you have a sunburn, or are you always this hot?",
    "Is it hot in here, or is it just you?",
    "If you were a cat, you’d purr-suade me to take you out.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Do you have a map? I keep getting lost in your eyes.",
    "If you were words on a page, you’d be fine print.",
    "Are you a camera? Every time I look at you, I smile.",
    "Do you have a mirror in your pocket? Because I can see myself in your pants.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "If beauty were time, you'd be an eternity.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Are you a loan? Because you have my interest.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is this the Hogwarts Express? Because it feels like you and I are headed somewhere magical.",
    "If beauty were time, you’d be an eternity.",
    "Are you a time traveler? Because I can't seem to get you out of my future.",
    "Is your name Wi-fi? Because I'm feeling a connection.",
    "Do you have a pencil? Because I want to erase your past and write our future.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Do you have a sunburn, or are you always this hot?",
    "Is it hot in here, or is it just you?",
    "If you were a cat, you’d purr-suade me to take you out.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Do you have a map? I keep getting lost in your eyes.",
    "If you were words on a page, you’d be fine print.",
    "Are you a camera? Every time I look at you, I smile.",
    "Do you have a mirror in your pocket? Because I can see myself in your pants.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "If beauty were time, you'd be an eternity.",
    "Do you believe in love at first sight, or should I walk by again?",
    "If you were a vegetable, you'd be a cute-cumber!",
    "Are you a Wi-Fi signal? Because I'm feeling a connection.",
    "Do you have a sunburn, or are you always this hot?",
    "Can I follow you home? Cause my parents always told me to follow my dreams.",
    "Are you a camera? Every time I look at you, I smile.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Excuse me, but I think the stars tonight are outshone by your smile.",
    "If you were a cat, you'd purr-fect.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Can I take you out for dinner? Because I can't seem to get you out of my mind.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Are you a time traveler? Because I can't imagine my future without you.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Can I borrow a map? I keep getting lost in your eyes.",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is this the Hogwarts Express? Because it feels like you and I are headed somewhere magical.",
    "If beauty were time, you’d be an eternity.",
    "Are you a time traveler? Because I can't seem to get you out of my future.",
    "Is your name Wi-fi? Because I'm feeling a connection.",
    "Do you have a pencil? Because I want to erase your past and write our future.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Do you have a sunburn, or are you always this hot?",
    "Is it hot in here, or is it just you?",
    "If you were a cat, you’d purr-suade me to take you out.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Do you have a map? I keep getting lost in your eyes.",
    "If you were words on a page, you’d be fine print.",
    "Are you a camera? Every time I look at you, I smile.",
    "Do you have a mirror in your pocket? Because I can see myself in your pants.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "If beauty were time, you'd be an eternity.",
    "Do you believe in love at first sight, or should I walk by again?",
    "If you were a vegetable, you'd be a cute-cumber!",
    "Are you a Wi-Fi signal? Because I'm feeling a connection.",
    "Do you have a sunburn, or are you always this hot?",
    "Can I follow you home? Cause my parents always told me to follow my dreams.",
    "Are you a camera? Every time I look at you, I smile.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Excuse me, but the stars tonight are outshone by your smile.",
    "If you were a cat, you'd purr-fect.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Can I take you out for dinner? Because I can't seem to get you out of my mind.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Are you a time traveler? Because I can't imagine my future without you.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Can I borrow a map? I keep getting lost in your eyes.",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is this the Hogwarts Express? Because it feels like you and I are headed somewhere magical.",
    "If beauty were time, you’d be an eternity.",
    "Are you a time traveler? Because I can't seem to get you out of my future.",
    "Is your name Wi-fi? Because I'm feeling a connection.",
    "Do you have a pencil? Because I want to erase your past and write our future.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Do you have a sunburn, or are you always this hot?",
    "Is it hot in here, or is it just you?",
    "If you were a cat, you’d purr-suade me to take you out.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Do you have a map? I keep getting lost in your eyes.",
    "If you were words on a page, you’d be fine print.",
    "Are you a camera? Every time I look at you, I smile.",
    "Do you have a mirror in your pocket? Because I can see myself in your pants.",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "If beauty were time, you'd be an eternity.",
    "Do you believe in love at first sight, or should I walk by again?",
    "If you were a vegetable, you'd be a cute-cumber!",
    "Are you a Wi-Fi signal? Because I'm feeling a connection.",
    "Do you have a sunburn, or are you always this hot?",
    "Can I follow you home? Cause my parents always told me to follow my dreams.",
    "Are you a camera? Every time I look at you, I smile.",
    "Are you made of copper and tellurium? Because you're Cu-Te.",
    "Excuse me, but the stars tonight are outshone by your smile.",
    "If you were a cat, you'd purr-fect.",
    "Do you believe in love at first sight, or should I walk by again?",
    "Excuse me, but I think you dropped something: MY JAW!",
    "Can I take you out for dinner? Because I can't seem to get you out of my mind.",
    "Are you a parking ticket? Because you've got 'FINE' written all over you.",
    "Are you a time traveler? Because I can't imagine my future without you.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Is your name Google? Because you've got everything I've been searching for.",
    "Can I borrow a map? I keep getting lost in your eyes.",
    "Are you a campfire? Because you're hot, and I want s'more.",
    "Excuse me, but I think you dropped something: MY JAW!"
}

@dp.message(Command("start", "restart"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    global task_dictionary, message_id
    chat_id = message.from_user.id 
    message_id = message.message_id
    CONSOLE = f'''\n 
                        CONSOLE: start\n
                        STATE: Menu\n
                        CHAT_ID: {chat_id}\n
               '''
    print(CONSOLE)
    if chat_id not in task_dictionary.keys():
        task_dictionary[chat_id] = ToDoList(chat_id) 
    await state.set_state(StepsForm.MENU)
    task_dictionary[chat_id].check(datetime.datetime.now())

    markup = custom_markup_for_the_menu()

    await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.strip() == 'DEACTIVATE')
async def deactivate_account(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.MENU:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: !DEACTIVATE! account\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
            
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='/start')]], one_time_keyboard=False)
        del task_dictionary[chat_id]
        
        await bot.send_message(chat_id, "<code> Sir, your account, OH NOO, SIR\n\n IT's successfully gone</code>", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.strip() == 'Menu')
async def menu_activity(message: types.Message, state: FSMContext) -> None: 
    if await state.get_state() != StepsForm.MENU:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.MENU)
        
        markup = custom_markup_for_the_menu()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: Menu\n
                        STATE: Menu\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
@dp.message(F.text.strip() == 'Working')
async def working_activity(message: types.Message, state: FSMContext) -> None:  
    
    if await state.get_state() == StepsForm.MENU:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.WORKING)

        markup = custom_markup_for_working()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Working:\nWhat task do you want to start or stop, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
        
        CONSOLE = f'''\n 
                        CONSOLE: Working\n
                        STATE: Working\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Template')
async def template_activity(message: types.Message, state: FSMContext) -> None:  
    
    if await state.get_state() == StepsForm.MENU:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.TEMPLATE)

        markup = custom_markup_for_template()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + "Template:\nWhat do you want to do within a template, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
        
        CONSOLE = f'''\n 
                        CONSOLE: Menu\n
                        STATE: Menu\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Start/Stop')
async def working_start_activity(message: types.Message, state: FSMContext) -> None:  
    if await state.get_state() == StepsForm.WORKING:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.WORKING_START)
        

        markup = custom_markup_for_working_start_activity(task_dictionary=task_dictionary, chat_id=chat_id)
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Working:\nStart/Stop:\nWhat task do you want to start or stop, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
        CONSOLE = f'''\n 
                        CONSOLE: Working START/STOP\n
                        STATE: Working start\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Add')
async def add_activity(message: types.Message, state: FSMContext) -> None: 
    
    if await state.get_state() == StepsForm.WORKING:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.WORKING_ADD)

        markup = custom_markup_for_working_add_activity()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Working:\nAdd:\nTask's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: WORKING ADD\n
                        STATE: working add\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
    
    if await state.get_state() == StepsForm.TEMPLATE:
        chat_id = message.from_user.id
        await state.set_state(StepsForm.TEMPLATE_ADD)

        markup = custom_markup_for_template_add_activity()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + "Template:\nAdd:\nTask's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: TEMPLATE ADD\n
                        STATE: template add\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)

    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Delete')
async def delete_activity(message: types.Message, state: FSMContext) -> None: 
    
    if await state.get_state() == StepsForm.WORKING: 
        
        chat_id = message.from_user.id
        await state.set_state(StepsForm.WORKING_DELETE)

        markup = custom_markup_for_working_delete_activity(task_dictionary=task_dictionary, chat_id=chat_id)
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Working:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: WORKING DELETE\n
                        STATE: working delete\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
    if await state.get_state() == StepsForm.TEMPLATE: 
        
        chat_id = message.from_user.id
        await state.set_state(StepsForm.TEMPLATE_DELETE)

        markup = custom_markup_for_template_delete_activity(task_dictionary, chat_id)
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + "Template:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: TEMPLATE DELETE\n
                        STATE: template delete\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)


    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Replace current tasks with template')
async def current_task_to_template(message: types.Message, state: FSMContext) -> None:  
    global task_dictionary
    
    if await state.get_state() == StepsForm.TEMPLATE:
        chat_id = message.from_user.id
        
        markup = custom_markup_for_template()

        task_dictionary[chat_id].tasks = [Task(task.name, task.remaining_time) for task in task_dictionary[chat_id].tasks_template]
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + "Template:\nWhat do you want to do within a template, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: replace current tasks with template\n
                        STATE: template\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)

    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() == 'Replace template with current tasks')
async def template_to_current_task(message: types.Message, state: FSMContext) -> None:  
    global task_dictionary
    
    if await state.get_state() == StepsForm.TEMPLATE:
        chat_id = message.from_user.id
        
        markup = custom_markup_for_template()

        task_dictionary[chat_id].tasks_template = [Task(task.name, task.remaining_time) for task in task_dictionary[chat_id].tasks if task.remaining_time >= 0]
        for task in task_dictionary[chat_id].tasks_template:
            task.going = False
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + "Template:\nWhat do you want to do within a template, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        CONSOLE = f'''\n 
                        CONSOLE: template with current tasks\n
                        STATE: template\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

@dp.message(F.text.strip() != 'Delete' and F.text.strip() != 'Start/Stop' and F.text.strip() != 'Add')
async def handle_activity(message: types.Message, state: FSMContext) -> None:
    global task_dictionary
    if await state.get_state() == StepsForm.WORKING_START:
        
        chat_id = message.from_user.id
        
        CONSOLE = f'''\n 
                        CONSOLE: WORKING_START\n
                        STATE: WORKING_START\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
        try:
            task_to_start_or_stop_from_user_splitted = message.text

            if task_dictionary[chat_id].start_activity(task_to_start_or_stop_from_user_splitted, date_time=message.date):
                
                markup = custom_markup_for_working_start_activity(task_dictionary=task_dictionary, chat_id=chat_id)
                task_dictionary[chat_id].check(datetime.datetime.now())

                await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + 'Successfully started or stopped \n' +  "Working:\nStart/Stop:\nWhat task do you want to start or stop, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
            else:

                markup = custom_markup_for_working_start_activity(task_dictionary=task_dictionary, chat_id=chat_id)
                task_dictionary[chat_id].check(datetime.datetime.now())

                await bot.send_message(chat_id, 'Task was not touched \n\n' +  "Working:\nStart/Stop:\nWhat task do you want to start or stop, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        except Exception as e:
            print(e)

            await bot.send_message(chat_id, 'Task was not touched \n' +  "Working:\nStart/Stop:\nWhat task do you want to start or stop, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    elif await state.get_state() == StepsForm.WORKING_ADD:
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: WORKING ADD\n
                        STATE: working add\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)


        markup = custom_markup_for_working_add_activity()
        
        try:

            task_from_user_splitted = message.text.split()
            task_from_user = (' '.join(task_from_user_splitted[:-1]), task_from_user_splitted[-1])
            name_of_task, duration = task_from_user
            duration = int(duration)
            if (task_dictionary[chat_id].append(Task(name=name_of_task, duration=duration))) and (task_dictionary[chat_id].len_tasks() <= 30):
                task_dictionary[chat_id].check(datetime.datetime.now())

                await bot.send_message(chat_id,  task_dictionary[chat_id].__str__() + '\n\n\n' + 'Successfully added \n' +  "Working:\nAdd:\nTask's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
            else:
                await bot.send_message(chat_id,  task_dictionary[chat_id].__str__() + '\n\n\n' + 'Working:\nAdd:\nTask with the same name exists or you achieved limit\n' +  "Task's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        except Exception as e:
            print(e)
            await bot.send_message(chat_id, "Task was not added\n\nWorking:\nAdd:\nTask's name and duration in minutes, sweetie?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    elif await state.get_state() == StepsForm.WORKING_DELETE:
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: WORKING DELETE\n
                        STATE: working delete\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
        
        markup = custom_markup_for_working_delete_activity(task_dictionary=task_dictionary, chat_id=chat_id)

        try:
            task_to_delete_from_user_splitted = message.text
            print()
            print(list(map(lambda x: x.name, task_dictionary[chat_id].tasks)))
            if task_dictionary[chat_id].delete_task(task_to_delete_from_user_splitted):
                print(list(map(lambda x: x.name, task_dictionary[chat_id].tasks)))
                print()
                markup = custom_markup_for_working_delete_activity(task_dictionary=task_dictionary, chat_id=chat_id)
                task_dictionary[chat_id].check(datetime.datetime.now())
                await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + 'Successfully deleted \n' +  "Working:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
            else:
                await bot.send_message(chat_id, 'Task was not deleted \n\n' +  "Working:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
        except Exception as e:
            print(e)
            await bot.send_message(chat_id, 'Task was not deleted \n' +  "Working:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    elif await state.get_state() == StepsForm.TEMPLATE_ADD:
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: TEMPLATE ADD\n
                        STATE: template add\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        markup = custom_markup_for_template_add_activity()
        
        try:
            task_from_user_splitted = message.text.split()
            task_from_user = (' '.join(task_from_user_splitted[:-1]), task_from_user_splitted[-1])
            name_of_task, duration = task_from_user
            duration = int(duration)
            print(list(map(lambda x: x.name, task_dictionary[chat_id].tasks)))
            if (task_dictionary[chat_id].append_to_template(Task(name=name_of_task, duration=duration))) and (task_dictionary[chat_id].len_tasks_template() <= 30):
                print(list(map(lambda x: x.name, task_dictionary[chat_id].tasks)))
                task_dictionary[chat_id].check(datetime.datetime.now())
                await bot.send_message(chat_id,  task_dictionary[chat_id].print_template() + '\n\n\n' + 'Successfully added \n' +  "Template:\nAdd:\nTask's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
            else:
                await bot.send_message(chat_id,  task_dictionary[chat_id].print_template() + '\n\n\n' + 'Task with the same name exists or you achieved limit\n' +  "Template:\nAdd:\nTask's name and duration in minutes, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

        except Exception as e:
            print(e)
            await bot.send_message(chat_id, "Task was not added\n\nTemplate:\nAdd:\nTask's name and duration in minutes, sweetie?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    elif await state.get_state() == StepsForm.TEMPLATE_DELETE:
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: TEMPLATE DELETE\n
                        STATE: template delete\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        
        markup = custom_markup_for_template_delete_activity(task_dictionary, chat_id)

        try:
            task_to_delete_from_user_splitted = message.text

            if task_dictionary[chat_id].delete_task_from_template(task_to_delete_from_user_splitted):
                markup = custom_markup_for_template_delete_activity(task_dictionary, chat_id)

                await bot.send_message(chat_id, task_dictionary[chat_id].print_template() + '\n\n\n' + 'Successfully deleted \n' +  "Template:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
            else:
                await bot.send_message(chat_id, 'Task was not deleted \n\n' +  "Template:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
        except Exception as e:
            print(e)
            await bot.send_message(chat_id, 'Task was not deleted \n' +  "Template:\nDelete:\nWhat task do you want to delete, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    else:
        await if_your_state_is_initial_redirect_to_the_menu(state, message.from_user.id)

    save_dict_to_json(data=task_dictionary, json_file=FILE_NAME)

async def if_your_state_is_initial_redirect_to_the_menu(state: FSMContext, chat_id: int) -> None:
    if await state.get_state() not in ( StepsForm.MENU, 
                                        StepsForm.TEMPLATE,
                                        StepsForm.TEMPLATE_ADD,
                                        StepsForm.TEMPLATE_DELETE,
                                        StepsForm.WORKING,
                                        StepsForm.WORKING_START, 
                                        StepsForm.WORKING_ADD, 
                                        StepsForm.WORKING_DELETE):
        
        await state.set_state(StepsForm.MENU)
        
        markup = custom_markup_for_the_menu()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

async def on_startup(chat_id:int, task_dictionary:dict) -> None:   
    await bot.send_message(chat_id, "Bot has been started!", disable_notification=True)

    # Schedule the message to be sent daily at 12:00
    asyncio.create_task(scheduled_messages(task_dictionary))

async def action_over_time(current_time) -> None:
    global task_dictionary
    date_time = current_time
    current_time = current_time.time()
    h, m = current_time.hour, current_time.minute
    if current_time.hour == 21 and current_time.minute == 59: # night message
        # Send the scheduled message
        for chat_ids in task_dictionary.keys():
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <good night message>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            task_dictionary[chat_ids].check(date_time)
            await bot.send_message(chat_ids, f'''\n 
                                                \U0001FA90 {random.choice(list(good_night_sentences))}
                                                \n\n      ---\n{random.choice(list(pickup_lines))}\n      ---\n
                                                    <strong>I Love You</strong> ''', 
                                    parse_mode='HTML', 
                                    disable_notification=True)   

    if (current_time.hour != 1 and current_time.minute == 0) and \
         (current_time.hour != 2 and current_time.minute == 0) and \
         (current_time.hour != 3 and current_time.minute == 0) and \
         (current_time.hour != 22 and current_time.minute == 0):
        for chat_ids in task_dictionary.keys():
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <success, so far>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            await bot.send_message(
                chat_ids,
                task_dictionary[chat_ids].__str__() + '\n\n\n\n' + f"      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n<i>your progress</i> \n\n<code>Great job</code>",
                parse_mode='HTML',
                disable_notification=True
                                    )
    if (current_time.hour == 22 and current_time.minute == 0):
        for chat_ids in task_dictionary.keys():
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <success for today>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            await bot.send_message(
                chat_ids,
                task_dictionary[chat_ids].__str__() + '\n\n\n' + f"      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n<i><b>Today's</b> accomplishments.</i> \n\n<code>Great job</code>",
                parse_mode='HTML',
                disable_notification=True
                                    )    
    if (current_time.hour == 1 and current_time.minute == 0): # 03:00
        for chat_ids in task_dictionary.keys():
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <reset today's tasks>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            task_dictionary[chat_ids].tasks = [Task(task.name, task.remaining_time) for task in task_dictionary[chat_ids].tasks_template]
            await bot.send_message(chat_ids, f"\n      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n Your tasks for today have been set up", parse_mode='HTML', disable_notification=True)

async def scheduled_messages(task_dictionary:dict):
    while True:
        # current time
        current_time = datetime.datetime.now()
        
        await action_over_time(current_time) # perform actions at a specific time.

        # Sleep for a minute and check again
        await asyncio.sleep(60)

def save_dict_to_json(data:dict, json_file:str) -> None:
    new_data = data.copy()
    for chat_id, to_do_list in new_data.items():
        new_data[chat_id] = to_do_list.__dict__()
    with open(json_file, 'w') as file:
        json.dump(new_data, file, indent=4)
 
def initial_set_up(json_file:str) -> dict:
    try:
        new_data = {}
        with open(json_file, 'r') as file:
            data = json.load(file)

            if isinstance(data, dict):
                for key, value in data.items():
                    to_do_list = ToDoList(key) # chat id
                    to_do_list.unpacking(dictionary=value)
                    new_data[int(key)] = to_do_list

                return new_data
            else:
                raise ValueError("The JSON file does not contain a valid dictionary.")
    except FileNotFoundError:
        print('\n\n\n\nJSON file was not observed\n\n\n\n')
        return {}
    except json.JSONDecodeError:
        raise ValueError(f"\n\n\n\nThe JSON file '{json_file}' is not valid JSON.\n\n\n\n")
        return {}
    except ValueError as e:
        print('\n\n\n\nCheck initial_set_up() function and JSON file, something is bad here')
        print(e)
        print('\n\n\n')
        return {}
    return {}

async def main() -> None:

    try:
        global FILE_NAME, FSMContext_file, task_dictionary
        
        FILE_NAME = './data.json'
        task_dictionary = initial_set_up(FILE_NAME)
        await on_startup(773603143, task_dictionary) # my chat id

        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
