
import httpx


class ProxyError(Exception):
	def __init__(self, response, errors):
		self.response = response
		self.errors = errors
	
	def __str__(self):
		return str(self.errors)


class ServiceError(Exception):
	def __init__(self, response, messages):
		self.response = response
		self.messages = messages
	
	def __str__(self):
		return str(self.messages)


class ServiceClient:
	def __init__(self, settings):
		self.settings = settings

		self.session = httpx.AsyncClient()

		self.account_number = None
		self.card_number = None
	
	async def request(self, method, path, *, service_version=None, **kwargs):
		headers = {
			"User-Agent": self.settings.make_user_agent(self.account_number, self.card_number)
		}
		if service_version is not None:
			headers["x-aab-serviceversion"] = "v%i" %service_version

		response = await self.session.request(method, self.settings.host + path, headers=headers, **kwargs)
		if response.is_error:
			if "application/json" in response.headers.get("Content-Type", ""):
				data = response.json()
				if "messages" in data:
					raise ServiceError(response, data["messages"])
				if "errors" in data:
					raise ProxyError(response, data["errors"])
			response.raise_for_status()
		
		if "application/json" in response.headers.get("Content-Type", ""):
			return response.json()
	
	async def get(self, path, *, service_version=None, params=None):
		return await self.request("GET", path, service_version=service_version, params=params)
	
	async def put(self, path, *, service_version=None, data=None):
		return await self.request("PUT", path, service_version=service_version, json=data)
	
	async def delete(self, path):
		return await self.request("DELETE", path)

	def set_profile(self, account_number, card_number):
		self.account_number = account_number
		self.card_number = card_number


class AccountsService:
	def __init__(self, client):
		self.client = client
	
	async def get_contracts(
		self, product_groups=None, product_building_blocks=None, include_actions=None,
		include_action_names=None, exclude_blocked=None, exclude_status=None,
		bc_number=None, contract_ids=None
	):
		params = {}
		if product_groups is not None: params["productGroups"] = ",".join(product_groups)
		if product_building_blocks is not None: params["productBuildingBlocks"] = ",".join([str(i) for i in product_building_blocks])
		if include_actions is not None: params["includeActions"] = include_actions
		if include_action_names is not None: params["includeActionNames"] = ",".join(include_action_names)
		if exclude_blocked is not None: params["excludeBlocked"] = "true" if exclude_blocked else "false"
		if exclude_status is not None: params["excludeStatus"] = ",".join(exclude_status)
		if bc_number is not None: params["bcNumber"] = bc_number
		if contract_ids is not None: params["contractIds"] = ",".join(contract_ids)
		return await self.client.get("/contracts", params=params, service_version=2)


class AuthorizationService:
	def __init__(self, client):
		self.client = client
	
	async def get_session(self):
		return await self.client.get("/session")

	async def delete_session(self):
		await self.client.delete("/session")

	async def get_login_challenge(self, account_number, card_number, access_tool_usage, bound_device_index_number=None):
		params = {
			"accountNumber": account_number,
			"cardNumber": card_number,
			"accessToolUsage": access_tool_usage
		}
		if access_tool_usage in ["BOUNDDEVICE_USERPIN", "BOUNDDEVICE_TOUCHIDPIN"]:
			params["boundDeviceIndexNumber"] = bound_device_index_number
		
		return await self.client.get("/session/loginchallenge", params=params, service_version=2)
	
	async def send_login_response(
		self, account_number, card_number, challenge_handle, response, access_tool_usage,
		challenge_device_details, app_id, bound_device_index_number=None, is_jailbroken=None,
		is_bound=None, imei=None, telephone_no=None
	):
		data = {
			"accountNumber": account_number,
			"cardNumber": card_number,
			"challengeHandle": challenge_handle,
			"response": response,
			"accessToolUsage": access_tool_usage,
			"challengeDeviceDetails": challenge_device_details,
			"appId": app_id
		}
		if bound_device_index_number is not None: data["boundDeviceIndexNumber"] = bound_device_index_number
		if is_jailbroken is not None: data["isJailbroken"] = is_jailbroken
		if is_bound is not None: data["isBound"] = is_bound
		if imei is not None: data["imei"] = imei
		if telephone_no is not None: data["telephoneNo"] = telephone_no
		return await self.client.put("/session/loginresponse", data=data, service_version=4)

	async def get_session_handover_challenge(self, access_tool_usage):
		params = {
			"accessToolUsage": access_tool_usage
		}
		return await self.client.get("/session/sessionhandoverchallenge", params=params)


class DebitCardsService:
	def __init__(self, client):
		self.client = client
	
	async def get_debit_cards(self):
		return await self.client.get("/debitcards")
	
	async def get_debit_card(self, key):
		return await self.client.get("/debitcards/%s" %key)


class MutationsService:
	def __init__(self, client):
		self.client = client
	
	async def get_mutations(
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
		return await self.client.get("/mutations/%s" %account, params=params, service_version=3)
