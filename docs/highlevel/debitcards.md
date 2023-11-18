
# Debit Cards

Main interface:

<code>**class** [DebitCardsManager](#debitcardsmanager)</code>

Types that are used by the debit cards manager:

<code>**class** [DebitCard](#debitcard)
**class** [DebitCardId](#debitcardid)
**class** [Duration](#duration)
**class** [GeoProfile](#geoprofile)
**class** [Limit](#limit)
**class** [LimitObject](#limitobject)
**class** [ValidationData](#validationdata)</code>

## DebitCardsManager
<code>**def _\_init__**(client: [ServiceClient](#serviceclient))</code><br>
<span class="docs">Creates a new debit cards manager with the given service client.</span>

<code>**def list**() -> list[[DebitCard](#debitcard)]</code><br>
<span class="docs">Requests your list of debit cards.</span>

<code>**def get**(account_number: int, card_number: int) -> [DebitCard](#debitcard)</code><br>
<span class="docs">Requests a specific debit card.</span>

## DebitCard
<code>id: [DebitCardId](#debitcardid)
status: str
product_code: str
product_name: str
owner_name: str
atm_limit: [Limit](#limit)
pos_limit: [Limit](#limit)
geo_profile: [GeoProfile](#geoprofile)
future_atm_limit: [Limit](#limit)
future_pos_limit: [Limit](#limit)
future_geo_profile: [GeoProfile](#geoprofile)
is_atm_limit_change_allowed: bool
is_pos_limit_change_allowed: bool
is_geo_profile_change_allowed: bool
is_atm_limit_update_in_progress: bool
is_pos_limit_update_in_progress: bool
is_geo_profile_update_in_progress: bool
is_manage_limit_authorized: bool
is_manage_geo_profile_authorized: bool
last_mutation_date: datetime.datetime
last_reissue_date: datetime.datetime
last_block_date: datetime.datetime
validation_data: [ValidationData](#validationdata)</code>

## DebitCardId
<code>account_number: str
card_number: str
iban: str</code>

## Duration
<code>type: str
start_date: datetime.datetime
end_date: datetime.datetime</code>

## GeoProfile
<code>type: str
duration: [Duration](#duration)</code>

## Limit
<code>duration: [Duration](#duration)
limit: [LimitObject](#limitobject)</code>

## LimitObject
<code>amount: int
currency: str</code>

## ValidationData
<code>maximum_atm_limit: [LimitObject](#limitobject)
maximum_pos_limit: [LimitObject](#limitobject)
minimum_atm_limit: [LimitObject](#limitobject)
minimum_pos_limit: [LimitObject](#limitobject)
valid_geo_profile_types: list[str]</code>
