
from abnamro import services
from abnamro.schema import *


class Action(Schema):
	name: StringField("name")
	user_action_indicator: StringField("userActionIndicator")


class Mutation(Schema):
	amount: FloatField("amount")
	currency_iso_code: StringField("currencyIsoCode")
	balance_after_mutation: FloatField("balanceAfterMutation")
	debit_credit: StringField("debitCredit", choices=["DEBIT", "CREDIT"])
	indicator_digital_invoice: BooleanField("indicatorDigitalInvoice")
	payment_status: StringField("paymentStatus", choices=["DEFAULT", "INITIAL", "APPROVED", "PENDING", "REJECTED"])
	status_timestamp: TimestampField("statusTimestamp")

	mutation_code: StringField("mutationCode")
	description_lines: StringField("descriptionLines", repeated=True)
	source_inquiry_number: StringField("sourceInquiryNumber")
	transaction_timestamp: StringField("transactionTimestamp")

	account_type: StringField("accountNumberType")
	account_number: StringField("accountNumber")
	counter_account_name: StringField("counterAccountName")
	counter_account_type: StringField("counterAccountType")
	counter_account_number: StringField("counterAccountNumber")

	transaction_date: TimestampField("transactionDate")
	value_date: TimestampField("valueDate")
	book_date: TimestampField("bookDate")


class MutationObject(Schema):
	actions: ObjectField("actions", Action, repeated=True)
	mutation: ObjectField("mutation", Mutation)


class MutationList(Schema):
	clear_cache_indicator: BooleanField("clearCacheIndicator")
	page_token: StringField("lastMutationKey")
	mutations: ObjectField("mutations", MutationObject, repeated=True)


class MutationsManager:
	def __init__(self, client):
		self.service = services.MutationsService(client)
	
	async def search(
		self, iban, *, page_size=20, page_token=None, text=None, amount_from=None,
		amount_to=None, book_date_from=None, book_date_to=None
	):
		cd_indicator_amount_from = None
		cd_indicator_amount_to = None

		if amount_from is not None:
			cd_indicator_amount_from = "CREDIT" if amount_from > 0 else "DEBIT"
			amount_from = abs(amount_from)
		
		if amount_to is not None:
			cd_indicator_amount_to = "CREDIT" if amount_to > 0 else "DEBIT"
			amount_to = abs(amount_to)

		response = await self.service.get_mutations(
			iban, page_size, "BASIC", page_token, None,
			text, amount_from, amount_to, cd_indicator_amount_from,
			cd_indicator_amount_to, book_date_from, book_date_to
		)
		return MutationList.create(response["mutationsList"])
