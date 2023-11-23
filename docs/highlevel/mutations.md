
# Mutations

Main interface:

<code>**class** [MutationsManager](#mutationsmanager)</code>

Types that are used by the debit cards manager:

<code>**class** [Action](#action)
**class** [Mutation](#mutation)
**class** [MutationList](#mutationlist)
**class** [MutationObject](#mutationobject)</code>

## MutationsManager
<code>**def _\_init__**(client: [ServiceClient](#serviceclient))</code><br>
<span class="docs">Creates a new mutations manager with the given service client.</span>

<code>**async def search**(iban: str, *, page_size: int = 20, page_token: str = None, text: str = None, amount_from: float = None, amount_to: float = None, book_date_from: datetime.datetime = None, book_date_to: datetime.datetime = None) -> [MutationList](#mutationlist)</code><br>
<span class="docs">Requests mutations for the given IBAN. Up to 20 mutations can be requested at once. In case more mutations are desired, the page token from the [MutationList](#mutationlist) can be used to obtain the next page. Various filters can be specified. Only the mutations of the past 18 months can be obtained.</span>

## Action
<code>name: str
user_action_indicator: str</code>

## Mutation
<code>amount: float
currency_iso_code: str
balance_after_mutation: float
debit_credit: str
indicator_digital_invoice: bool
payment_status: str
status_timestamp: datetime.datetime<br>
mutation_code: str
description_lines: list[str]
source_inquiry_number: str
transaction_timestamp: str<br>
account_type: str
account_number: str
counter_account_name: str
counter_account_type: str
counter_account_number: str<br>
transaction_date: datetime.datetime
value_date: datetime.datetime
book_date: datetime.datetime</code>

## MutationList
<code>clear_cache_indicator: bool
page_token: str
mutations: list[[MutationObject](#mutationobject)]</code>

## MutationObject
<code>actions: list[[Action](#action)]
mutation: [Mutation](#mutation)</code>
