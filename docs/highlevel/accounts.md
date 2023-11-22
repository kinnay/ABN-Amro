
# Accounts

Main interface:

<code>**class** [AccountsManager](#accountsmanager)</code>

Types that are used by the accounts manager:

<code>**class** [Action](#action)
**class** [Balance](#balance)
**class** [Contract](#contract)
**class** [Customer](#customer)
**class** [ParentContract](#parentcontract)
**class** [Product](#product)</code>

## AccountsManager
<code>**def _\_init__**(client: [ServiceClient](#serviceclient))</code><br>
<span class="docs">Creates a new accounts manager with the given service client.</span>

<code>**def list**(*,
	product_groups: list[str] = None,
	product_building_blocks: list[int],
	include_actions: str = None,
	include_action_names: list[str] = None,
	exclude_blocked: bool = None,
	exclude_status: list[str] = None,
	bc_number: int = None,
	contract_ids: list[str] = None
) -> list[[Contract](#contract)]</code><br>
<span class="docs">Requests your list of contracts. By default, all contracts are returned, but various filters can be specified.</span>

## Action
<code>name: str</code>

## Balance
<code>amount: float
currency_code: str</code>

## Contract
<code>resource_type: str
id: str
account_number: str
contract_number: str
chid: str
concerning: str
is_blocked: bool
status: str
balance: [Balance](#balance)
product: [Product](#product)
customer: [Customer](#customer)
actions: list[[Action](#action)]
sequence_number: int
parent_contract: [ParentContract](#parentcontract)</code>

## Customer
<code>appearance_type: str
bc_number: int
interpay_name: str</code>

## ParentContract
<code>id: str</code>

## Product
<code>resource_type: str
id: int
building_block_id: int
name: str
product_group: str
account_type: str
transfer_options: list[str]
credit_account: bool</code>
