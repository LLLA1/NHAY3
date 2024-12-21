from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User
from ZeMusic import app

async def extract_user(m: Message) -> User:
    """
    Extracts a User from a given Message.
    
    Args:
        m (Message): The message to extract the user from.
        
    Returns:
        User: The user extracted from the message.
    """
    # Check if the message is a reply
    if m.reply_to_message:
        return m.reply_to_message.from_user

    # Determine the message entities based on whether it s a command
    msg_entities = m.entities[1] if m.text.startswith("/") else m.entities[0]

    try:
        # Extract user based on the type of message entity
        if msg_entities.type == MessageEntityType.TEXT_MENTION:
            return await app.get_users(msg_entities.user.id)
        elif len(m.command) > 1:
            user_id = m.command[1]
            # Check if the user_id is a decimal number
            if user_id.isdecimal():
                return await app.get_users(int(user_id))
            else:
                return await app.get_users(user_id)

    except Exception as e:
        print(f"Error extracting user: {e}")
        return None  # Return None if there was an error

    return None  # Return None if no user could be extracted
