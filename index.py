import logging
import config
import time
from filter import IsAdminFilter
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter		
import utils



API_TOKEN = config.token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.filters_factory.bind(IsAdminFilter)
'''
#mute
@dp.message_handler(is_admin=True, chat_id=config.GROUP_ID, commands="mute")
async def cmd_readonly(message: types.Message):
	# Check if command is sent as reply to some message
	if not message.reply_to_message:
		await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
		return

	# Admins cannot be restricted
	user = await message.bot.get_chat_member(config.GROUP_ID, message.reply_to_message.from_user.id)
	if user.is_chat_admin():
		await message.reply("Невозможно ограничить администратора.")
		return

	words = message.text.split()
	restriction_time: int = 0
	if len(words) > 1:  # !mute with arg
		restriction_time = time().get_restriction_time(words[1])
		if not restriction_time:
		    await message.reply("Неправильный формат времени. Используйте число + символ h, m или d. Например, 4h")
		    return
	else:
		restriction_time = 86400 * 367

	await message.bot.restrict_chat_member(config.GROUP_ID,
				                           message.reply_to_message.from_user.id,
				                           types.ChatPermissions(),
				                           until_date=int(time()) + restriction_time
				                           )

	if len(words) > 1:
		await message.reply("Выдан мут на ({restriction_time})").format(restriction_time=words)
	else: await message.reply("Выдан мут.Для снятия мута напишите в личные сообщения боту модератору")
	    	
#unmute
@dp.message_handler(is_admin=True, chat_id=config.GROUP_ID, commands="unmute")
async def cmd_unreadonly(message: types.Message):
	# Check if command is sent as reply to some message
	if not message.reply_to_message:
		await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
		return

	# Admins cannot be restricted
	user = await message.bot.get_chat_member(config.GROUP_ID, message.reply_to_message.from_user.id)
	if user.is_chat_admin():
		await message.reply("Невозможно ограничить администратора.")
		return

	words = message.text.split()
	await message.bot.restrict_chat_member(config.GROUP_ID,
		                                   message.reply_to_message.from_user.id,
		                                   types.ChatPermissions(True))
	    
	await message.reply("Мут снят .Больше не шали так")

'''
#perk
@dp.message_handler(is_admin=False, chat_id=config.GROUP_ID, commands=["checkperms"])
async def cmd_checkperms(message: types.Message):

	# Check if command is sent as reply to some message
	if not message.reply_to_message:
		await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
		return

	# check if member is admin
	user = await message.bot.get_chat_member(config.GROUP_ID, message.reply_to_message.from_user.id)
	if user.is_chat_admin():
		await message.reply("✅ У админов нет никаких ограничений.")
		return


	msg = "Текущие права:\n"

	if(user.can_send_messages is None):
	    	# default chat perms
	    	chat = await message.bot.get_chat(message.chat.id)

	    	msg += "\nОтправлять сообщения: " + ("✅" if chat.permissions.can_send_messages else "❌")
	    	msg += "\nОтправлять медиа: " + ("✅" if chat.permissions.can_send_media_messages else "❌")
	    	msg += "\nОтправлять стикеры: " + ("✅" if chat.permissions.can_send_other_messages else "❌")
	else:
	    	# custom perms
	    	msg += "\nОтправлять сообщения: " + ("✅" if user.can_send_messages else "❌")
	    	msg += "\nОтправлять медиа: " + ("✅" if user.can_send_media_messages else "❌")
	    	msg += "\nОтправлять стикеры: " + ("✅" if user.can_send_other_messages else "❌")


	await message.reply(msg)
'''
#ban
@dp.message_handler(chat_id=config.GROUP_ID, commands=["ban"])
async def cmd_ban(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(config.GROUP_ID, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("😡 Админа нельзя банить!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)  # remove admin message
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Участник заблокирован.")

#unban
@dp.message_handler(chat_id=config.GROUP_ID, commands=["unban"])
async def cmd_unban(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("😡 Админа нельзя банить!")
        return

    await message.bot.delete_message(chat_id=config.GROUP_ID, message_id=message.message_id)  # remove admin message
    await message.bot.unban_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Участник разблокирован.")
    
    
#report
@dp.message_handler(chat_id=config.GROUP_ID, commands="report")
async def cmd_report(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на какое-либо сообщение!")
        return

    # Check if command is sent to own message
    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply("Нельзя репортить самого себя 🤪")
        return

    # Check if command is sent as reply to admin
    user = await message.bot.get_chat_member(chat_id=-1001554503017, user_id=message.reply_to_message.from_user.id)
    if user.is_chat_admin() and user.can_restrict_members:
        await message.reply("Админов репортишь? Ай-ай-ай 😈")
        return



    # Cannot report group posts
    if message.reply_to_message.from_user.id == 777000:
        await message.bot.delete_message(chat_id=-708933990, user_id=message.message_id)
        return

    # Check for report message (anything sent after /report command)
    msg_parts = message.text.split()
    report_message = None
    if len(msg_parts) > 1:
        report_message = message.text.replace("/report", "")
        report_message = report_message.replace("report", "")

    # Generate keyboard with some actions
    action_keyboard = types.InlineKeyboardMarkup()
    # Delete message by its id
    action_keyboard.add(types.InlineKeyboardButton(
        text="🗑 Удалить сообщение",
        callback_data=f"del_{message.reply_to_message.message_id}")
    )

    # Delete message by its id and ban user by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text="🗑 Удалить + ❌ бан навсегда",
        callback_data=f"delban_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    # Delete message by its id and mute user for 24 hours by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text="🗑 Удалить + 🙊 мут на день",
        callback_data=f"mute_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    # Delete message by its id and mute user for 7 days by their id
    action_keyboard.add(types.InlineKeyboardButton(
        text="🗑 Удалить + 🙊 мут на неделю",
        callback_data=f"mute2_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    # Do nothing, false alarm
    action_keyboard.add(types.InlineKeyboardButton(
        text="❎ Нарушений нет",
        callback_data=f"dismiss_{message.reply_to_message.message_id}_{message.reply_to_message.from_user.id}"
    ))

    # Do nothing, false alarm + mute reporter for one day
    action_keyboard.add(types.InlineKeyboardButton(
        text="❎ Нарушений нет (🙊 мут репортера на день)",
        callback_data=f"dismiss2_{message.message_id}_{message.from_user.id}"
    ))

    # Do nothing, false alarm + mute reporter for one week
    action_keyboard.add(types.InlineKeyboardButton(
        text="❎ Нарушений нет (🙊 мут репортера на неделю)",
        callback_data=f"dismiss3_{message.message_id}_{message.from_user.id}"
    ))

    # Do nothing, false alarm + ban reporter
    action_keyboard.add(types.InlineKeyboardButton(
        text="❎ Нарушений нет (❌ бан репортера)",
        callback_data=f"dismiss4_{message.message_id}_{message.from_user.id}"
    ))

    await message.reply_to_message.forward(config.reports)
    await message.bot.send_message(
        config.reports,
        utils.read(),
        reply_markup=action_keyboard)
    await message.reply("Report sent")
    
#kick    
@dp.message_handler(is_admin=False, commands=["kick"])
async def ban_user(message: types.Message):
	print("Command has read")
	if not message.reply_to_message:
		await message.answer("Мне нужные точные указания на жертву 😈")
		print("error")
		return
	
	await message.bot.delete_message(chat_id=config.GROUP_ID, message_id=message.message_id)	
	await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
	await message.reply_to_message.reply("Жертва убита и кикнута, красота😈")
	await message.reply_to_message.reply("А можно было и забанить...")
	print("work")
	
'''
#bot    
@dp.message_handler(commands=["bot"])
async def bot_calling(message: types.Message):
	print("Command has read")
	await message.reply("Здесь✅")
	print("work")

#new user    
@dp.message_handler(content_types=["new_chat_member"])
async def new_user(message: types.Message):
	await message.bot.delete_message(chat_id=config.GROUP_ID, message_id=message.message_id)
	await message.reply("Ням, свежое мясцо🥰")
	print("work")
    
    
#polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
