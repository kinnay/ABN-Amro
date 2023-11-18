
import requests


class ServiceError(Exception):
	def __init__(self, response):
		self.response = response
		self.messages = response.json()["messages"]
	
	def __str__(self):
		return str(self.messages)


class ServiceClient:
	def __init__(self, settings):
		self.settings = settings

		self.session = requests.Session()

		self.account_number = None
		self.card_number = None
	
	def request(self, method, path, *, service_version=None, **kwargs):
		headers = {
			"User-Agent": self.settings.make_user_agent(self.account_number, self.card_number)
		}
		if service_version is not None:
			headers["x-aab-serviceversion"] = "v%i" %service_version

		response = self.session.request(method, self.settings.host + path, headers=headers, **kwargs)
		if not response.ok:
			if "application/json" in response.headers.get("Content-Type"):
				raise ServiceError(response)
			response.raise_for_status()
		return response.json()
	
	def get(self, path, *, service_version=None, params=None):
		return self.request("GET", path, service_version=service_version, params=params)
	
	def put(self, path, *, service_version=None, data=None):
		return self.request("PUT", path, service_version=service_version, json=data)

	def set_profile(self, account_number, card_number):
		self.account_number = account_number
		self.card_number = card_number


class AuthorizationService:
	def __init__(self, client):
		self.client = client

	def get_login_challenge(self, account_number, card_number, access_tool_usage, bound_device_index_number=None):
		params = {
			"accountNumber": account_number,
			"cardNumber": card_number,
			"accessToolUsage": access_tool_usage
		}
		if access_tool_usage in ["BOUNDDEVICE_USERPIN", "BOUNDDEVICE_TOUCHIDPIN"]:
			params["boundDeviceIndexNumber"] = bound_device_index_number
		
		return self.client.get("/session/loginchallenge", params=params, service_version=2)
	
	def send_login_response(
		self, account_number, card_number, challenge_handle, response, access_tool_usage,
		challenge_device_details, app_id, bound_device_index_number, is_jailbroken,
		is_bound, imei, telephone_no
	):
		data = {
			"accountNumber": account_number,
			"cardNumber": card_number,
			"challengeHandle": challenge_handle,
			"response": response,
			"accessToolUsage": access_tool_usage,
			"challengeDeviceDetails": challenge_device_details,
			"appId": app_id,
			"boundDeviceIndexNumber": bound_device_index_number or 0,
			"isJailbrokenRooted": is_jailbroken,
			"isBound": is_bound,
			"imei": imei,
			"telephoneNo": telephone_no
		}
		return self.client.put("/session/loginresponse", data=data, service_version=4)

	def get_session_handover_challenge(self, access_tool_usage):
		params = {
			"accessToolUsage": access_tool_usage
		}
		return self.client.get("/session/sessionhandoverchallenge", params=params)


class DebitCardsService:
	def __init__(self, client):
		self.client = client
	
	def get_debit_cards(self):
		return self.client.get("/debitcards")
	
	def get_debit_card(self, key):
		return self.client.get("/debitcards/%s" %key)


class MutationsService:
	def __init__(self, client):
		self.client = client
	
	def get_mutations(
		self, account, page_size=20, include_actions="BASIC", last_mutation_key=None,
		most_recent_mutation_key=None, search_text=None, amount_from=None, amount_to=None,
		cd_indicator_amount_from=None, cd_indicator_amount_to=None,
		book_date_from=None, book_date_to=None
	):
		params = {
			"pageSize": page_size,
			"includeActions": include_actions
		}
		if last_mutation_key is not None: params["lastMutationKey"] = last_mutation_key
		if most_recent_mutation_key is not None: params["mostRecentMutationKey"] = most_recent_mutation_key
		if search_text is not None: params["searchText"] = search_text
		if amount_from is not None: params["amountFrom"] = "%.2f" %amount_from
		if amount_to is not None: params["amountTo"] = "%.2f" %amount_to
		if cd_indicator_amount_from is not None: params["cdIndicatorAmountFrom"] = cd_indicator_amount_from
		if cd_indicator_amount_to is not None: params["cdIndicatorAmountTo"] = cd_indicator_amount_to
		if book_date_from != None: params["bookDateFrom"] = book_date_from.strftime("%Y/%m/%d")
		if book_date_to != None: params["bookDateTo"] = book_date_to.strftime("%Y/%m/%d")
		return self.client.get("/mutations/%s" %account, params=params, service_version=3)
