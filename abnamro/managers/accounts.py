
from abnamro import services
from abnamro.schema import *


class Balance(Schema):
	amount: FloatField("amount")
	currency_code: StringField("currencyCode")


class Product(Schema):
	resouce_type: StringField("resourceType")
	id: IntegerField("id")
	building_block_id: IntegerField("buildingBlockId")
	name: StringField("name")
	product_group: StringField("productGroup")
	account_type: StringField("accountType")
	transfer_options: StringField("transferOptions", repeated=True)
	credit_account: BooleanField("creditAccount")


class Customer(Schema):
	appearance_type: StringField("appearanceType")
	bc_number: IntegerField("bcNumber")
	interpay_name: StringField("interpayName")


class Action(Schema):
	name: StringField("name")


class ParentContract(Schema):
	id: StringField("id")


class Contract(Schema):
	resource_type: StringField("resourceType")
	id: StringField("id")
	account_number: StringField("accountNumber")
	contract_number: StringField("contractNumber")
	chid: StringField("chid")
	concerning: StringField("concerning")
	is_blocked: BooleanField("isBlocked")
	status: StringField("status")
	balance: ObjectField("balance", Balance)
	product: ObjectField("product", Product)
	customer: ObjectField("customer", Customer)
	actions: ObjectField("actions", Action, repeated=True)
	sequence_number: IntegerField("sequenceNumber")
	parent_contract: ObjectField("parentContract", ParentContract)


class AccountsManager:
	def __init__(self, client):
		self.service = services.AccountsService(client)
	
	async def list(self, *, product_groups=None, product_building_blocks=None, include_actions=None,
		include_action_names=None, exclude_blocked=None, exclude_status=None,
		bc_number=None, contract_ids=None
	):
		response = await self.service.get_contracts(
			product_groups, product_building_blocks, include_actions,
			include_action_names, exclude_blocked, exclude_status,
			bc_number, contract_ids
		)
		return [Contract.create(contract["contract"]) for contract in response["contractList"]]
