
from abnamro import services
from abnamro.schema import *


class DebitCardId(Schema):
	account_number: StringField("accountNumber")
	card_number: StringField("cardNumber")
	iban: StringField("ibanNumber")


class Duration(Schema):
	start_date: DateTimeField("startDate", "%Y-%m-%d")
	end_date: DateTimeField("endDate", "%Y-%m-%d")
	type: StringField("type", choices=["PERMANENT", "TEMPORARY"])


class LimitObject(Schema):
	amount: IntegerField("amount")
	currency: StringField("currencyCode")


class Limit(Schema):
	duration: ObjectField("duration", Duration)
	limit: ObjectField("limit", LimitObject)


class GeoProfile(Schema):
	type: StringField("geoProfile", choices=["EUROPE", "WORLD"])
	duration: ObjectField("duration", Duration)


class ValidationData(Schema):
	maximum_atm_limit: ObjectField("maximumATMLimit", LimitObject)
	maximum_pos_limit: ObjectField("maximumPOSLimit", LimitObject)
	minimum_atm_limit: ObjectField("minimumATMLimit", LimitObject)
	minimum_pos_limit: ObjectField("minimumPOSLimit", LimitObject)
	valid_geo_profile_types: StringField("validGeoProfileTypes", choices=["EUROPE", "WORLD"], repeated=True)


class DebitCard(Schema):
	id: ObjectField("id", DebitCardId)
	status: StringField("cardStatus", choices=["ACTIVE", "INACTIVE", "BLOCKED", "EXPIRED"])
	product_code: StringField("productCode")
	product_name: StringField("productName")
	owner_name: StringField("cardOwnerName")
	atm_limit: ObjectField("atmLimit", Limit)
	pos_limit: ObjectField("posLimit", Limit)
	geo_profile: ObjectField("geoProfile", GeoProfile)
	future_atm_limit: ObjectField("futureAtmLimit", Limit)
	future_pos_limit: ObjectField("futurePosLimit", Limit)
	future_geo_profile: ObjectField("futureGeoProfile", GeoProfile)
	is_atm_limit_change_allowed: BooleanField("isATMLimitChangeAllowed")
	is_pos_limit_change_allowed: BooleanField("isPOSLimitChangeAllowed")
	is_geo_profile_change_allowed: BooleanField("isGeoProfileChangeAllowed")
	is_atm_limit_update_in_progress: BooleanField("isATMLimitUpdateInProgress")
	is_pos_limit_update_in_progress: BooleanField("isPOSLimitUpdateInProgress")
	is_geo_profile_update_in_progress: BooleanField("isGeoProfileUpdateInProgress")
	is_manage_limit_authorized: BooleanField("isManageLimitAuthorised")
	is_manage_geo_profile_authorized: BooleanField("isManageGeoProfileAuthorised")
	last_mutation_date: TimestampField("lastMutationDate")
	last_reissue_date: TimestampField("lastReissueDate")
	last_block_date: TimestampField("lastBlockDate")
	validation_data: ObjectField("validationData", ValidationData)


class DebitCardsManager:
	def __init__(self, client):
		self.service = services.DebitCardsService(client)
	
	async def list(self):
		response = await self.service.get_debit_cards()
		cards = response["debitcardList"]["debitcards"]
		return [DebitCard.create(card["debitcard"]) for card in cards]
	
	async def get(self, account_number, card_number):
		card = await self.service.get_debit_card("%i;%i" %(account_number, card_number))
		return DebitCard.create(card["debitcard"])
