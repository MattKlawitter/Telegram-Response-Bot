import re

class Command:
	"""
	Class containing information on the command receieved in a Telegram message.
	"""

	def __init__(self, message):
		"""
		Parameters
		----------
		message: Message
			Message object that contains property information on a Telegram message.

		Properties
		----------
		self.command: string
			Contains the command string received.

		self.mention: string
			Contains the nickname of another Telegram user embedded within the message.

		self.args: string
			string of all text following the command string.

		self.chat: string
			The chat id of the Telegram group from which the command string was sent from.

		self.user: string
			The nickname of the user who sent the command string.
		"""

		text = message.text[1:]
		args_index = text.index(" ") if " " in text else len(text)
		self.command = text[:args_index]

		text = text[args_index+1:]
		user_match = re.search("@(\w+)", text)
		
		self.mention = user_match.group(1) if user_match else ""
		self.args = text.strip()
		self.chat = message.chat
		self.user = message.sent_from


class User:
	"""
	Class containing information on the user who sent a message on Telegram
	"""

	def __init__(self, user):
		"""
		Parameters
		----------
		user: dictionary
			contains information on a Telegram user after they send a message seen by the bot
			includes the user id, their first name, and their username

		Properties
		----------
		self.id: string
			The user/chatroom id of a Telegram user

		self.first_name: string
			The first name of a Telegram user

		self.username: string
			The username a Telegram user has chosen (ex. @Nickname or Nickname)
		"""

		self.id = user["id"]
		self.is_bot = user["is_bot"]
		self.first_name = user["first_name"]
		self.last_name = user["last_name"]
		self.username = user["username"] if "username" in user else self.first_name
		self.language_code = user["language_code"]


class Chat:
	"""
	Class that contains information on the chat id and type from a message sent by a Telegram user.
	"""

	def __init__(self, chat):
		"""
		Parameters
		----------
		chat: dictionary
			dictionary object that contains the chat id and the chat type.

		Properties
		----------
		self.id: string
			The Telegram chat/channel id from which a message was received.

		self.type: string
			The Telegram chat type (ex. channel, chatroom, etc.)
		"""

		self.id = chat["id"]
		self.type = chat["type"]
		self.title = chat["title"]
		self.username = chat["username"]
		self.first_name = chat["first_name"]
		self.last_name = chat["last_name"]

		"""
		Still need to implement the following due to missing dependencies:
		photo
		description
		invite_link
		pinned_message
		permissions
		sticker_set_name
		can_set_sticker_set
		"""


class Message:
	"""
	Object that contains properties of Telegram message info
	"""

	def __init__(self, message):
		"""
		Parameters
		----------
		message: dictionary
			dictionary object that contains message information sent by telegram.

		Properties
		----------
		self.date: string
			String Date at which the message was sent.

		self.sent_from: string
			String Telegram user that sent the message.
		
		self.chat: Chat obj
			String chat/channel id from which the message was received.

		self.text: string
			String containing the message sent.

		self.is_command: Boolean
			Boolean determining if this contains the command prefix (default="/").

		self.command: Command
			Command object containing extensive information on the message and command string.
			Sent to the plugin that manages the designated command string should it exist.
		"""

		self.message_id = message["message_id"]
		self.sent_from = User(message["from"])
		self.date = message["date"]
		self.chat = Chat(message["chat"])
		self.forward_from = User(message["forward_from"])
		self.forward_from_chat = Chat(message["forward_from_chat"])
		self.forward_from_message_id = message["forward_from_message_id"]
		self.forward_signature = message["forward_signature"]
		self.forward_sender_name = message["forward_sender_name"]
		self.forward_date = message["forward_date"]
		self.reply_to_message = Message(message["reply_to_message"])
		self.edit_date = message["edit_date"]
		self.media_group_id = message["media_group_id"]
		self.author_signature = message["author_signature"]
		self.raw_text = message["text"]
		self.text = message["text"].strip() if "text" in message else ""
		"""
		Still need to implement the following due to further dependencies:
		entities
		caption_entities
		audio
		document
		animation
		game
		photo
		sticker
		video
		voice
		voice_note
		caption
		contact
		location
		venue
		poll
		new_chat_members
		left_chat_members
		new_chat_title
		new_chat_photo
		delete_chat_photo
		group_chat_created
		supergroup_chat_created
		channel_chat_created
		migrate_to_chat_id
		migrate_from_chat_id
		pinned_message
		invoice
		successful_payment
		connected_website
		passport_date
		reply_markup
		"""
		self.is_command = self.text.startswith("/")
        
		if self.is_command:
			self.command = Command(self)

class MessageEntity:
	def __init__(self, entity):
		self.type = entity["type"]
		self.offset = entity["offset"]
		self.length = entity["length"]
		self.url = entity["url"]
		self.user = User(entity["user"])


class PhotoSize:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.width = file["width"]
		self.height = file["height"]
		self.file_size = file["file_size"]

class Audio:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.duration = file["duration"]
		self.performer = file["performer"]
		self.title = file["title"]
		self.mime_type = file["mime_type"]
		self.file_size = file["file_size"]
		self.thumb = PhotoSize(file["thumb"])

class Document:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.thumb = PhotoSize(file["thumb"])
		self.file_name = file["file_name"]
		self.mime_type = file["mime_type"]
		self.file_size = file["file_size"]

class Video:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.width = file["width"]
		self.height = file["height"]
		self.duration = file["duration"]
		self.thumb = PhotoSize(file["thumb"])
		self.mime_type = file["mime_type"]
		self.file_size = file["file_size"]

class Animation:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.width = file["width"]
		self.height = file["height"]
		self.duration = file["duration"]
		self.thumb = PhotoSize(file["thumb"])
		self.file_name = file["file_name"]
		self.mime_type = file["mime_type"]
		self.file_size = file["file_size"]

class Voice:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.duration = file["duration"]
		self.mime_type = file["mime_type"]
		self.file_size = file["file_size"]

class VideoNote:
	def __init__(self, file):
		self.file_id = file["file_id"]
		self.length = file["length"]
		self.duration = file["duration"]
		self.thumb = PhotoSize(file["thumb"])
		self.file_size = file["file_size"]

class Contact:
	def __init__(self, contact):
		self.phone_number = contact["phone_number"]
		self.first_name = contact["first_name"]
		self.last_name = contact["last_name"]
		self.user_id = contact["user_id"]
		self.vcard = contact["vcard"]

class Location:
	def __init__(self, location):
		self.longitude = location["longitude"]
		self.latitude = location["latitude"]

class Venue:
	def __init__(self, venue):
		self.location = Location(venue["location"])
		self.title = venue["title"]
		self.address = venue["address"]
		self.foursquare_id = venue["foursquare_id"]
		self.foursquare_type = venue["foursquare_type"]

class PollOption:
	def __init__(self, option):
		self.text = option["text"]
		self.voter_count = option["voter_count"]

class Poll:
	def __init__(self, poll):
		self.id = poll["id"]
		self.question = poll["question"]
		self.options = []
		for option in poll["options"]:
			self.options.append(PollOption(option))
		self.is_closed = poll["is_closed"]

"""
Continue on from UserProfilePhotos
"""
