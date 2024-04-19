import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import Config  # Import your config file

# Initialize the bot
app = Client(
    "terabox_bot",
    api_id=Config.API_ID,  # Your API ID from my.telegram.org
    api_hash=Config.API_HASH,  # Your API Hash from my.telegram.org
    bot_token=Config.BOT_TOKEN,  # Your bot's token from BotFather
)

# Force subscription function
async def force_subscribe(client: Client, message: Message):
    try:
        # Create an invite link to the updates channel
        invite_link = await client.create_chat_invite_link(
            chat_id=Config.UPDATES_CHANNEL
        )
    except FloodWait as e:
        # Handle FloodWait error
        await asyncio.sleep(e.x)
        invite_link = await client.create_chat_invite_link(
            chat_id=Config.UPDATES_CHANNEL
        )
    except Exception as e:
        # Log other exceptions
        print(f"Error creating invite link: {e}")
        return False

    try:
        # Check if the user is subscribed
        user = await client.get_chat_member(Config.UPDATES_CHANNEL, message.from_user.id)
        if user.status in [enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.CREATOR]:
            return True
        elif user.status == enums.ChatMemberStatus.KICKED:
            await message.reply("You are banned from the updates channel. Please contact the admin.")
            return False
    except UserNotParticipant:
        # Prompt the user to join the channel
        await message.reply(
            "Please join the updates channel to use this bot.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Channel", url=invite_link.invite_link)],
                    [InlineKeyboardButton("Refresh", callback_data="refresh_fsub")]
                ]
            )
        )
        return False
    except Exception as e:
        # Log any other exceptions
        print(f"Error checking subscription: {e}")
        return False
    return True

# Start command handler
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply(
        f"Hello {message.from_user.first_name}!\n\nI can download files from Terabox for you.\n\nPlease join our updates channel to use this bot.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Join @Film_Nest", url="https://t.me/Film_Nest")],
                [InlineKeyboardButton("Report Bug", url="https://t.me/Armanidrisi_bot")]
            ]
        )
    )

# Message handler
@app.on_message(filters.text)
async def handle_message(client: Client, message: Message):
    # Force subscription check
    if not await force_subscribe(client, message):
        return  # Exit if the user is not subscribed

    # User is subscribed, process the message
    message_text = message.text
    if "terabox.com" in message_text or "teraboxapp.com" in message_text:
        # Process the Terabox link
        await message.reply("Processing your request...")
        # Add your Terabox link processing logic here
    else:
        await message.reply("Please send a valid Terabox link.")

# Main function to run the bot
if __name__ == "__main__":
    app.run()
