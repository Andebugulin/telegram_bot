from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def custom_markup_for_the_menu() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_the_menu was used\n'
    print(CONSOLE)
    deactivate_account_btn = KeyboardButton(text="DEACTIVATE")
    first_row = [deactivate_account_btn]
    
    working_activity_btn = KeyboardButton(text="Working")
    template_activity_btn = KeyboardButton(text="Template")
    second_row = [working_activity_btn, template_activity_btn]
    
    key_board = [first_row, second_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_working() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_working was used\n'
    print(CONSOLE)
    add_activity_btn = KeyboardButton(text="Add")
    delete_activity_btn = KeyboardButton(text="Delete")
    start_activity_btn = KeyboardButton(text="Start/Stop")
    menu_activity_btn = KeyboardButton(text="Menu")

    first_row = [start_activity_btn]
    second_row = [add_activity_btn, delete_activity_btn]
    third_row = [menu_activity_btn]
    
    key_board = [first_row, second_row, third_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_working_add_activity() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_working_add_activity was used\n'
    print(CONSOLE)
    new_1_activity_btn = KeyboardButton(text='learning chess' + ' ' + str(10))
    new_2_activity_btn = KeyboardButton(text='Andrew Tate' + ' ' + str(210))
    menu_activity_btn = KeyboardButton(text="Menu")

    first_row = [new_1_activity_btn]
    second_row = [new_2_activity_btn] 
    third_row = [menu_activity_btn]  

    key_board = [first_row, second_row, third_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_working_start_activity(task_dictionary: dict, chat_id: int) -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_working_start_activity was used\n'
    print(CONSOLE)
    
    key_board = []  

    rows = []
    buttons_in_one_row = []
    flag_finished = False
    for task in task_dictionary[chat_id]:
        if task.remaining_time > 0:    
            if len(task.name) > 25:
                buttons_in_one_row = [KeyboardButton(text=task.name)]
                rows.append(buttons_in_one_row)
                buttons_in_one_row = []
                flag_finished = True
            else:
                if len(buttons_in_one_row) == 0:
                    buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))
                    flag_finished = False
                elif len(buttons_in_one_row) == 1:
                    if ((sum([len(btn_text) for btn, btn_text in buttons_in_one_row]) + len(task.name)) < 40): # if all task names would fit in a row
                        buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))

                        rows.append([btn for btn, btn_text in buttons_in_one_row])
                        buttons_in_one_row = []
                        flag_finished = True
                    else:
                        rows.append([btn for btn, btn_text in buttons_in_one_row])

                        buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                        flag_finished = False
                else:
                    rows.append([btn for btn, btn_text in buttons_in_one_row])

                    buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                    flag_finished = False
    if not flag_finished:
        rows.append([btn for btn, btn_text in buttons_in_one_row])

    for row in rows:
        key_board.append(row)

    key_board.append([KeyboardButton(text='Menu')])

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_working_delete_activity(task_dictionary: dict, chat_id: int) -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_working_delete_activity was used\n'
    print(CONSOLE)
    key_board = []

    rows = []
    buttons_in_one_row = []
    flag_finished = False
    for task in task_dictionary[chat_id]:
        if len(task.name) > 25:
            buttons_in_one_row = [KeyboardButton(text=task.name)]
            rows.append(buttons_in_one_row)
            buttons_in_one_row = []
            flag_finished = True
        else:
            if len(buttons_in_one_row) == 0:
                buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))
                flag_finished = False
            elif len(buttons_in_one_row) == 1:
                if ((sum([len(btn_text) for btn, btn_text in buttons_in_one_row]) + len(task.name)) < 40): # if all task names would fit in a row
                    buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))

                    rows.append([btn for btn, btn_text in buttons_in_one_row])
                    buttons_in_one_row = []
                    flag_finished = True
                else:
                    rows.append([btn for btn, btn_text in buttons_in_one_row])

                    buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                    flag_finished = False
            else:
                rows.append([btn for btn, btn_text in buttons_in_one_row])

                buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                flag_finished = False
    if not flag_finished:
        rows.append([btn for btn, btn_text in buttons_in_one_row])

    for row in rows:
        key_board.append(row)

    key_board.append([KeyboardButton(text='Menu')])

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_template() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_template was used\n'
    print(CONSOLE)   
    tasks_template_activity_btn = KeyboardButton(text="Replace current tasks with template")
    first_row = [tasks_template_activity_btn]

    template_tasks_activity_btn = KeyboardButton(text="Replace template with current tasks")
    second_row = [template_tasks_activity_btn] 

    add_activity_btn = KeyboardButton(text="Add")
    delete_activity_btn = KeyboardButton(text="Delete")
    third_row = [add_activity_btn, delete_activity_btn]

    menu_activity_btn = KeyboardButton(text="Menu")
    forth_row = [menu_activity_btn]

    key_board = [first_row, second_row, third_row, forth_row]


    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_template_add_activity() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_template_add_activity was used\n'
    print(CONSOLE)
    new_1_activity_btn = KeyboardButton(text='learning chess' + ' ' + str(10))
    new_2_activity_btn = KeyboardButton(text='Andrew Tate' + ' ' + str(210))
    menu_activity_btn = KeyboardButton(text="Menu")


    first_row = [new_1_activity_btn]
    second_row = [new_2_activity_btn] 
    third_row = [menu_activity_btn]  

    key_board = [first_row, second_row, third_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_template_delete_activity(task_dictionary: dict, chat_id: int) -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_template_delete_activity was used\n'
    print(CONSOLE)
    key_board = []

    rows = []
    buttons_in_one_row = []
    flag_finished = False
    for task in task_dictionary[chat_id].tasks_template:
        if len(task.name) > 25:
            buttons_in_one_row = [KeyboardButton(text=task.name)]
            rows.append(buttons_in_one_row)
            buttons_in_one_row = []
            flag_finished = True
        else:
            if len(buttons_in_one_row) == 0:
                buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))
                flag_finished = False
            elif len(buttons_in_one_row) == 1:
                if ((sum([len(btn_text) for btn, btn_text in buttons_in_one_row]) + len(task.name)) < 40): # if all task names would fit in a row
                    buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))

                    rows.append([btn for btn, btn_text in buttons_in_one_row])
                    buttons_in_one_row = []
                    flag_finished = True
                else:
                    rows.append([btn for btn, btn_text in buttons_in_one_row])

                    buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                    flag_finished = False
            else:
                rows.append([btn for btn, btn_text in buttons_in_one_row])

                buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
                flag_finished = False
    if not flag_finished:
        rows.append([btn for btn, btn_text in buttons_in_one_row])

    for row in rows:
        key_board.append(row)

    key_board.append([KeyboardButton(text='Menu')])

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup
