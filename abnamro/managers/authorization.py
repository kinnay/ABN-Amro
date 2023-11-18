
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
	
	def login(self, account_number, card_number, password):
		challenge_result = self.service.get_login_challenge(account_number, card_number, constants.ACCESS_SOFTTOKEN)["loginChallenge"]
		challenge_response = challenge.solve_login_challenge(bytes.fromhex(challenge_result["challenge"]), challenge_result["userId"], password)
		login_result = self.service.send_login_response(
			account_number, card_number, challenge_result["challengeHandle"], challenge_response,
			constants.ACCESS_SOFTTOKEN, challenge_result["challengeDeviceDetails"], self.settings.app_id,
			0, False, False, "", ""
		)
		self.client.set_profile(account_number, card_number)
		return Session.create(login_result["session"])
