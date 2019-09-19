import logging
import requests
import json
import re
import time
import threading
import os

from command_wrappers import Command, User, Chat, Message
from plugin_manager import PluginManager

class Bot:
	"""
	Singleton Bot class that acts as the controller for messages received and sent to Telegram.
	This file should be run when starting the bot currently.

	...

	Methods
	-------
	start()
		Starts the bot where it will check for updates received from Telegram and send replies based on Plugins and Messages.

	reload_plugins()
		Reloads all plugins managed in self.plugin_manager, incorporating new changes made

	enable_plugin(plugin_name)
		Enables a plugin with a specific name

	disable_plugin(plugin_name)
		Disables a plugin with a specific name

	plugin_help(plugin_name)
		Returns a string containing the help message from a Plugin's get_help method

	list_plugins()
		Returns a str listing all plugins

	get_updates(last_update)
		Gets message updates from Telegram based on those last received.

	send_message(id, message)
		Sends a message to Telegram.

	send_photo(id, message, file_name)
		Sends a photo to Telegram.
	"""

	def __init__(self, config):
		"""
		Sets up initial bot data and the PluginManager which loads inital plugins.
		...

		Parameters
		----------
		config: Config
			Configuration object containing data found within the bot's configuration file.
		"""

		self.logger = logging.getLogger('bot_log')
		self.directory = config.bot_dir
		self.base_url = "https://api.telegram.org/bot"+config.token+"/"
		self.sleep_interval = config.sleep_interval
		self.username = json.loads(requests.get(self.base_url + "getMe").text)["result"]["username"]
		self.plugin_manager = PluginManager(config, self)

		print(self.plugin_manager.list_commands())
		print(self.plugin_manager.list_listeners())

	def start(self, thread):
		"""
		Receives and sends messages to Telegram forever.
		Responses made by the bot are based on functionality contained within Plugins.
		"""

		last_update = 0

		while not thread.stopped():
			updates = self.get_updates(last_update)

			for update in updates["result"]:
				last_update = update["update_id"]

				if "message" in update:
					message = Message(update["message"])
					self.logger.info(str(last_update)+": "+message.sent_from.username)

					if message.is_command:
						self.logger.info("Command received, processing plugins")
						t = threading.Thread(target = self.plugin_manager.process_plugin, args = (self, message))
						t.setDaemon(True)
						t.start()
					else:
						t = threading.Thread(target = self.plugin_manager.process_message, args = (self, message))
						t.setDaemon(True)
						t.start()
		self.logger.warn("Ending telegram update loop due to thread manually being killed")

	def reload_plugins(self):
		"""
		Reloads all plugins managed in self.plugin_manager, incorporating new changes made
		"""

		self.plugin_manager.reload_plugins(self)
		return True

	def enable_plugin(self, plugin_name):
		"""
		Enables a plugin with a specific name
		"""

		self.logger.info("Attempting to enable plugin with name {}".format(plugin_name))
		return self.plugin_manager.enable_plugin(plugin_name)

	def disable_plugin(self, plugin_name):
		"""
		Disables a plugin with a specific name
		"""

		self.logger.info("Attempting to disable plugin with name {}".format(plugin_name))
		return self.plugin_manager.disable_plugin(plugin_name)

	def plugin_help(self, plugin_name):
		"""
		Returns a string containing the help message from a Plugin's get_help method
		"""

		self.logger.info("Requested help message from plugin with name {}".format(plugin_name))
		return self.plugin_manager.plugin_help(plugin_name)

	def list_plugins(self):
		"""
		Returns a str listing all plugins
		"""

		self.logger.info("Request recieved to list all plugins")
		return self.plugin_manager.list_plugins()

	def get_updates(self, last_update):
		"""
		Gets message updates from Telegram based on those last received.

		...

		Parameters
		----------
		last_update: json
			Data received from telegram dictating new messages that were send/visible to the bot.
		"""

		return json.loads(requests.get(self.base_url + 'getUpdates', params=dict(offset=(last_update+1))).text)

	def send_message(self, id, message):
		"""
		Sends a string message to a specific telegram chatroom containing the designated id.

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: str
			The message to be send to a chatroom.
		"""

		self.logger.info("Sending message ({}) to channel with id {}".format(message, id))
		return requests.get(self.base_url + 'sendMessage', params=dict(chat_id=id, text=message))

	def send_photo(self, id, caption, file_path):
		"""
		Sends a photo found with the designated filename with an optional caption string message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the photo to send to a Telegram chatroom
		"""

		path = {'photo': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending photo with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendPhoto', files=path, data=data)

	def send_audio(self, id, caption, file_path):
		"""
		Sends an audio file found at the given path with an optional caption message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the audio to send to a Telegram chatroom
		"""

		path = {'audio': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending audio with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendAudio', files=path, data=data)

	def send_document(self, id, caption, file_path):
		"""
		Sends a document file found at the given path with an optional caption message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the document to send to a Telegram chatroom
		"""

		path = {'document': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending document with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendDocument', files=path, data=data)

	def send_video(self, id, caption, file_path):
		"""
		Sends a video file found at the given path with an optional caption message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the video to send to a Telegram chatroom
		"""

		path = {'video': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending video with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendVideo', files=path, data=data)
	
	def send_animation(self, id, caption, file_path):
		"""
		Sends an animation file (gif) found at the given path with an optional caption message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the animation gif to send to a Telegram chatroom
		"""

		path = {'animation': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending animation with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendAnimation', files=path, data=data)

	def send_voice(self, id, caption, file_path):
		"""
		Sends a voice file (.ogg) found at the given path with an optional caption message to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		message: optional
			An optional string to send with an image as a caption

		file_path: str
			The file path of the voice (.ogg) to send to a Telegram chatroom
		"""

		path = {'voice': open(file_path, 'rb')}
		data = dict(chat_id=id, caption=caption)

		self.logger.info("Sending voice with caption ({}) with path ({}) to channel with id {}".format(caption, file_path, id))
		return requests.get(self.base_url + 'sendVoice', files=path, data=data)

	def send_location(self, id, latitude, longitude):
		"""
		Sends a location with a given latitude and longitude to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		latitude: float
			The latitude of the location to share

		longitude: float
			The longitude of the location to share
		"""

		data = dict(chat_id=id, latitude=latitude, longitude=longitude)

		self.logger.info("Sending location with latitude ({}) and longitude ({}) to channel with id {}".format(latitude, longitude, id))
		return requests.get(self.base_url + 'sendLocation', data=data)

	def send_poll(self, id, question, options):
		"""
		Sends an poll with a str question and a str array of options to a chatroom containing the designated id

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		question: str
			The question asked within the poll

		options: array of str
			An array of strings containing poll options
		"""

		data = dict(chat_id=id, question=question, options=options)

		self.logger.info("Sending poll with question ({}) to channel with id {}".format(question, id))
		return requests.get(self.base_url + 'sendPoll', data=data)

	def kick_chat_member(self, id, user_id, until_date):
		"""
		Kicks a user with user_id, from a channel with id, until a period of until_date seconds has passed
		The user is effectively banned until the period of time of elapsed
		If until_date exceeds more than 366 days or is less than 30 seconds, the ban is forever
		Note that the bot must be an admin within this chatroom

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		user_id: str
			The id of the user to be kicked/banned

		until_date: int
			The period of time in seconds the user is kicked for. If this value is greater than 366 days or less than 30 seconds
			the ban is forever and the user must be manually unbanned
		"""

		data = dict(chat_id=id, user_id=user_id, until_date=until_date)

		self.logger.info("Kicking user with id ({}) for ({}) seconds, from channel with id {}".format(user_id, until_date, id))
		return requests.get(self.base_url + 'kickChatMember', data=data)

	def unban_chat_member(self, id, user_id):
		"""
		Unbans a user with user_id, from a channel with id. Note that the bot must be an admin within this chatroom

		...

		Parameters
		----------
		id: str
			The id of the chatroom to unban a user from

		user_id: str
			The id of the user to be unbanned
		"""

		data = dict(chat_id=id, user_id=user_id)

		self.logger.info("Unbanning user with id ({}) from channel with id {}".format(user_id, id))
		return requests.get(self.base_url + 'unbanChatMember', data=data)

	def restrict_chat_member(self, id, user_id, permissions, until_date):
		"""
		Restricts a user with user_id, from a channel with id, until a period of until_date seconds has passed
		Restrictions are enacted through passing a ChatPermissions object, which can limit user actions such as chatting
		If until_date exceeds more than 366 days or is less than 30 seconds, the ban is forever
		Note that the bot must be an admin within this chatroom

		...

		Parameters
		----------
		id: str
			The id of the chatroom to send a message to.

		user_id: str
			The id of the user to be kicked/banned

		permissions: ChatPermissions
			An object containing restriction details that are enforced upon the specific user

		until_date: int
			The period of time in seconds the user is kicked for. If this value is greater than 366 days or less than 30 seconds
			the ban is forever and the user must be manually unbanned
		"""

		data = dict(chat_id=id, user_id=user_id, permissions=permissions, until_date=until_date)

		self.logger.info("Restricting user with id ({}) for ({}) seconds, from channel with id {}".format(user_id, until_date, id))
		return requests.get(self.base_url + 'restrictChatMember', data=data)
