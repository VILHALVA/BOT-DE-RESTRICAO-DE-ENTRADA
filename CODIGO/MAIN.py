from TOKEN import *
import telebot
import json
from datetime import datetime, timedelta, timezone

bot = telebot.TeleBot(TOKEN)

def load_config():
    with open('CONFIG.json', 'r') as file:
        config_data = json.load(file)
    return config_data

def calculate_restriction_duration(days):
    if days == "SEMPRE":
        return None  
    else:
        return datetime.now(timezone.utc) + timedelta(days=int(days))

def restrict_member_permissions(chat_id, user_id, config_data):
    can_send_messages = config_data.get('ENVIAR_MENSAGENS', 'OFF') == 'ON'
    can_send_media_messages = config_data.get('ENVIAR_MIDIAS', 'OFF') == 'ON'
    can_send_stickers = can_send_media_messages  
    can_add_web_page_previews = config_data.get('PREVIA_DE_LINKS', 'OFF') == 'ON'
    can_send_polls = config_data.get('ENVIAR_ENQUETES', 'OFF') == 'ON'
    can_invite_users = config_data.get('ADICIONAR_MEMBROS', 'OFF') == 'ON'
    can_pin_messages = config_data.get('FIXAR_MENSAGENS', 'OFF') == 'ON'
    can_change_info = config_data.get('ALTERAR_DADOS_DO_GRUPO', 'OFF') == 'ON'

    permissions = telebot.types.ChatPermissions(
        can_send_messages=can_send_messages,
        can_send_media_messages=can_send_media_messages,
        can_send_stickers=can_send_stickers,
        can_add_web_page_previews=can_add_web_page_previews,
        can_send_polls=can_send_polls,
        can_invite_users=can_invite_users,
        can_pin_messages=can_pin_messages,
        can_change_info=can_change_info
    )

    duration_end_date = calculate_restriction_duration(config_data.get('DIAS', '30'))

    bot.restrict_chat_member(chat_id, user_id, permissions=permissions, until_date=duration_end_date)

@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    config_data = load_config()
    for new_member in message.new_chat_members:
        restrict_member_permissions(message.chat.id, new_member.id, config_data)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá, este bot aplica restrições automáticas aos novos membros do grupo com base nas configurações.")

bot.polling()
