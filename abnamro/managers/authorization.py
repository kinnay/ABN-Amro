
from abnamro import challenge, constants, services
from abnamro.schema import *


class Representative(Schema):
	represetative_class: StringField("class")
	reference: StringField("reference")


class Session(Schema):
	connection_type: StringField("connectionType")
	device_type: StringField("deviceType")
	last_logon_date: TimestampField("lastLogonDate")
	representative: ObjectField("representative", Representative)
	represented_customer: StringField("representedCustomer")
	selected_customer: StringField("selectedCustomer")


class AuthorizationManager:
	def __init__(self, client, settings):
		self.client = client
		self.settings = settings

		self.service = services.AuthorizationService(client)
	
	async def login(self, account_number, card_number, password):
		challenge_result = await self.service.get_login_challenge(account_number, card_number, constants.ACCESS_SOFTTOKEN)
		login_challenge = challenge_result["loginChallenge"]

		challenge_response = challenge.solve_login_challenge(bytes.fromhex(login_challenge["challenge"]), login_challenge["userId"], password)
		login_result = await self.service.send_login_response(
			account_number, card_number, login_challenge["challengeHandle"], challenge_response,
			constants.ACCESS_SOFTTOKEN, login_challenge["challengeDeviceDetails"], self.settings.app_id,
			0, False, False, "", ""
		)
		self.client.set_profile(account_number, card_number)
		return Session.create(login_result["session"])
