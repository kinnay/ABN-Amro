
from abnamro import constants

import uuid


USER_AGENT_FORMAT = "[%s]/[%s] [%s]/[%s] [%s]/[%s] [%s] [%s] [%s]"


class Settings:
	def __init__(self):
		self.host = "https://www.abnamro.nl"
		self.app_id = constants.APP_ID_IPHONE

		# User agent settings
		self.app_name = "Bankieren"
		self.app_version = "12.44"
		self.brand_name = "Apple"
		self.model_name = "iPhone15,4"
		self.platform_name = "iOS"
		self.release_name = "17.1.1"
		self.installation_id = str(uuid.uuid4()).upper()
	
	def make_user_agent(self, account_number=None, card_number=None):
		if account_number is None: account_number = ""
		if card_number is None: card_number = ""

		return USER_AGENT_FORMAT %(
			self.app_name, self.app_version, self.brand_name, self.model_name,
			self.platform_name, self.release_name, self.installation_id,
			account_number, card_number
		)
