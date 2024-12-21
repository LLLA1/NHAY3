import asyncio
from datetime import datetime
from pyrogram.enums import ChatType

import config
from ZeMusic import app
from ZeMusic.core.call import Mody, autoend
from ZeMusic.utils.database import get_client, is_active_chat

async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while True:
            await asyncio.sleep(1500)  # الانتظار لمدة 1500 ثانية
            
            from ZeMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                
                try:
                    async for dialog in client.get_dialogs():
                        chat = dialog.chat
                        
                        # التحقق من نوع المحادثة
                        if chat.type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
                            # استبعاد المحادثات المخصصة
                            if chat.id not in {config.LOGGER_ID, -1001426097254, -1001583360745}:
                                # التحقق مما إذا كانت المحادثة غير نشطة
                                if not await is_active_chat(chat.id):
                                    try:
                                        await client.leave_chat(chat.id)
                                        left += 1
                                        # إذا تم مغادرة 20 محادثة، نخرج من الحلقة
                                        if left >= 20:
                                            break
                                    except Exception as e:
                                        print(f"Error leaving chat {chat.id}: {e}")
                except Exception as e:
                    print(f"Error retrieving dialogs for assistant {num}: {e}")

# إنشاء مهمة غير متزامنة لتشغيل الدالة auto_leave
asyncio.create_task(auto_leave())
