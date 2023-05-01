import telebot
import requests

# Create a bot instance and set the token
bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot! Use /download command to download content from specific channels.")

# Handler for /download command
@bot.message_handler(commands=['download'])
def download_content(message):
    # Check if user is authorized to use the bot
    if is_authorized(message.from_user.id):
        # Get the channel username
        channel_username = "YOUR_CHANNEL_USERNAME"
        # Get the content from the channel
        content = get_channel_content(channel_username)
        # Download the content
        for item in content:
            file_url = item['file_url']
            file_name = item['file_name']
            download_file(file_url, file_name)
        # Send a confirmation message
        bot.reply_to(message, "Content downloaded successfully!")
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

# Function to check if user is authorized
def is_authorized(user_id):
    # Implement your own logic to check if user is authorized
    # For example, you can store authorized user IDs in a database or a file
    # and check if the given user ID is present in the list
    authorized_users = [123456789, 987654321]
    return user_id in authorized_users

# Function to get content from a channel
def get_channel_content(channel_username):
    # Implement your own logic to get content from a channel
    # For example, you can use the Telegram API to get the channel messages
    # and filter the messages that contain files or media
    # You can also use third-party libraries like telethon or pyrogram for more advanced functionality
    # Here's an example of getting the latest 10 messages from the channel using Telegram API
    url = f"https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/getHistory?chat_id=@{channel_username}&limit=10"
    response = requests.get(url)
    data = response.json()
    messages = data['result']
    content = []
    for message in messages:
        if 'document' in message:
            file_id = message['document']['file_id']
            file_name = message['document']['file_name']
            file_url = f"https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/getFile?file_id={file_id}"
            content.append({'file_name': file_name, 'file_url': file_url})
        elif 'photo' in message:
            photo_sizes = message['photo']
            photo_url = photo_sizes[-1]['file_id']
            file_name = f"{photo_url}.jpg"
            file_url = f"https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/getFile?file_id={photo_url}"
            content.append({'file_name': file_name, 'file_url': file_url})
    return content

# Function to download a file
def download_file(url, file_name):
    response = requests.get(url)
    with open(file_name, "wb") as f:
        f.write(response.content)

# Start the bot
bot.polling()
