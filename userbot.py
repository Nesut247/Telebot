import os
from telethon import TelegramClient, events
import re

# Retrieve your API credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# Group IDs (replace these with the actual group IDs)
group_1_id = '1001804956848'
group_2_id = '1002362822092'

# Initialize the Telegram client
client = TelegramClient('userbot_session', api_id, api_hash)

# Listen for new messages in Group 1
@client.on(events.NewMessage(chats=group_1_id))
async def handler(event):
    message_text = event.message.message

    # Extract the contract address after "CA:"
    contract_match = re.search(r'CA:\s*(0x[a-fA-F0-9]{40})', message_text)
    
    if contract_match:
        contract_address = contract_match.group(1)

        # Send the /alpha/(contract) command to Group 2
        await client.send_message(group_2_id, f'/alpha/{contract_address}')

        # Send the contract address to Group 2 again to trigger the overview bot
        await client.send_message(group_2_id, contract_address)

        print(f"Forwarded contract {contract_address} from Group 1 to Group 2")

# Start the client and keep it running
client.start()
client.run_until_disconnected()
