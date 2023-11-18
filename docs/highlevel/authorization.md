
# Authorization

Main interface:

<code>**class** [AuthorizationManager](#authorizationmanager)</code>

Types that are used by the authorization manager:

<code>**class** [Representative](#representative)
**class** [Session](#session)</code>

## AuthorizationManager
<code>**def _\_init__**(client: [ServiceClient](#serviceclient), settings: [Settings](#settings))</code><br>
<span class="docs">Creates a new authorization manager with the given service client and settings.</span>

<code>**def login**(account_number: int, card_number: int, password: str) -> [Session](#session)</code>
<span class="docs">Authorizes the session using the `SOFTTOKEN` access method.</span>

## Representative
<code>representative_class: str
reference: str</code>


## Session
<code>connection_type: str
device_type: str
last_logon_date: datetime.datetime
representative: [Representative](#representative)
represented_customer: str
selected_customer: str</code>