from telebot import types, TeleBot
import requests

bot = TeleBot("6342760015:AAGXlSF0c4x-GL9GpDsWsY8b7bAHIxJ3oNY", parse_mode=None)


# def for get library
def get_json_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Error when requesting to{url}: {response.status_code}")  #Exception events that occur during the execution of the program, which can lead to errors or abnormal termination of the program.


# library
data_curated = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=Curated%20headphone%20bundles")
data_flag = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=Flagship%20headphones")
data_in_ear = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=In-ear%20headphones%20%26%20earbuds")
data_nosie = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=Noise%20cancelling%20headphones")
data_over = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=Over%20%26%20on-ear%20headphonesё")
data_wires = get_json_response(
    "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=Wireless%20headphones")


#Function for sending category data
def send_category(chat_id, category_data):
    category_data=category_data.get("results")
    for item in category_data[:10]:
            if isinstance(item, dict):
                img_links = item.get("img_links", "")
                img_link = img_links.split()[0][2:] if img_links else None
                item_name = item.get("name", "Неизвестно")
                item_price = item.get("price", "Неизвестно")
                id_team = item.get('id')
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Сайт", url=f'https://shop.u2p.kz/detail.html?id={id_team}')
                markup.add(button1)

                if img_link:
                    bot.send_photo(chat_id, img_link,
                                   f"Name: {item_name}\nPrice: {item_price}", reply_markup=markup)
                else:
                    bot.send_message(chat_id, f"Name: {item_name}\nPrice: {item_price}", reply_markup=markup)
            else:
                bot.send_message(chat_id, "eror 202")





#start
@bot.message_handler(commands=['start'])
def start_command(message):
    start_menu = types.InlineKeyboardMarkup()
    start_menu.add(types.InlineKeyboardButton(text="Assistant's help", callback_data='assist'))
    start_menu.add(types.InlineKeyboardButton(text='By category', callback_data='categories'))

    bot.send_message(message.chat.id, f"Hi, I'll help you choose the headphones. Select an option:",
                     reply_markup=start_menu, )


@bot.callback_query_handler(func=lambda call: True)
def unified_callback_handler(call):
    if call.data == 'assist':
        bot.send_message(call.message.chat.id, "What kind of headphones do you want?")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, assist_api)

    elif call.data == 'categories':
        category_menu = types.InlineKeyboardMarkup()
        category_menu.add(types.InlineKeyboardButton(text="Curated headphone bundles", callback_data="category_in_ear"))
        category_menu.add(types.InlineKeyboardButton(text="Flagship headphones", callback_data="category_on_ear"))
        category_menu.add(types.InlineKeyboardButton(text="In-ear headphones & earbuds", callback_data="category_over_ear"))
        category_menu.add(types.InlineKeyboardButton(text="Noise cancelling headphones", callback_data="category_wireless"))
        category_menu.add(types.InlineKeyboardButton(text="Over & on-ear headphones", callback_data="category_flag"))
        category_menu.add(types.InlineKeyboardButton(text="Wireless headphones", callback_data="category_wires"))

        bot.send_message(
            call.message.chat.id,
            "Select a category:",
            reply_markup=category_menu,
        )

    elif call.data == "category_in_ear":
        send_category(call.message.chat.id, data_curated)

    elif call.data == "category_on_ear":
        send_category(call.message.chat.id, data_flag)

    elif call.data == "category_over_ear":
        send_category(call.message.chat.id, data_in_ear)

    elif call.data == "category_wireless":
        send_category(call.message.chat.id, data_nosie)

    elif call.data == "category_flag":
        send_category(call.message.chat.id, data_over)
    elif call.data == "category_wires":
        send_category(call.message.chat.id, data_wires)





def assist_api(message):
    user_query = message.text
    response = requests.get(
        f"https://pythonproject-production-009d.up.railway.app/api/v1/chatgpt-assistant/chat/?prompt={user_query}"
    )
    response_data = response.json()
    response_text = response_data.get("response", "Couldn't get a response.")

    bot.send_message(message.chat.id, response_text)

    for category in response_data.get("categories", []):
        items = category.get("items", [])

        for item in items:
            if isinstance(item, dict):
                img_links = item.get("img_links", "").split()
                img_link = img_links[0][2:] if img_links else None
                item_name = item.get("name", "Неизвестно")
                item_price = item.get("price", "Неизвестно")
                id_team = item.get("id")
                if img_link:
                    markup = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton("Website", url=f'https://shop.u2p.kz/detail.html?id={id_team}')
                    markup.add(button1)
                    bot.send_photo(
                        message.chat.id,
                        img_link,
                        f"Name: {item_name}\nPrice: {item_price} \n ",
                        reply_markup=markup)

                else:
                    bot.send_message(
                        message.chat.id,
                        f"Name: {item_name}\nName: {item_price} \n ",
                        reply_markup=markup)

    start_command(message)


bot.polling(none_stop=True)
