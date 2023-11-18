
# General API

The `abnamro` package provides both a [low-level API](/lowlevel), which lets you call server methods directly, and a [high-level API](/highlevel), which provides a basic abstraction and validation.

In general, you want to use the high-level API.

The remainder of this page documents classes that are not bound to a specific service.

<code>**class** [Settings](#settings)</code><br>
<span class="docs">Contains configuration for the service clients, such as the user agent.</span>

<code>**class** [ServiceClient](#serviceclient)</code><br>
<span class="docs">A client that can be used to send HTTP requests to the server. The service client also keeps track of the session cookie.</span>

<code>**class** [ServiceError](#serviceerror)(Exception)</code><br>
<span class="docs">Raised when the server returns an error message.</span>

## Global Constants
`APP_ID_ANDROID = "ANDROID_APP"`<br>
`APP_ID_IPHONE = "IPHONE_APP"`<br>
`APP_ID_SIMPLE_BANKING = "SIMPLE_BANKING"`

`ACCESS_EDENTIFIER1 = "EDENTIFIER1"`<br>
`ACCESS_EDENTIFIER2_UNCONNECTED = "EDENTIFIER2_UNCONNECTED"`<br>
`ACCESS_EDENTIFIER2_CONNECTED = "EDENTIFIER2_CONNECTED"`<br>
`ACCESS_SOFTTOKEN = "SOFTTOKEN"`<br>
`ACCESS_BOUNDDEVICE_USERPIN = "BOUNDDEVICE_USERPIN"`<br>
`ACCESS_BOUNDDEVICE_TOUCHIDPIN = "BOUNDDEVICE_TOUCHIDPIN"`<br>
`ACCESS_SESSIONHANDOVER = "SESSIONHANDOVER"`<br>
`ACCESS_OOBGENERIC = "OOBGENERIC"`

## Settings
The settings class holds various parameters, such as the kind of device that you are using. The defaults should work fine.

`host: str = "https://www.abnamro.nl"`<br>
`app_id: str = APP_ID_IPHONE`

The following fields are used for the user agent:

`app_name: str = "Bankieren"`<br>
`app_version: str = "12.44"`<br>
`brand_name: str = "Apple"`<br>
`model_name: str = "iPhone15,4"`<br>
`platform_name: str = "iOS"`<br>
`release_name: str = "17.1.1"`<br>
`installation_id: str = str(uuid.uuid4()).upper()`

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new settings object with the default values.</span>

## ServiceClient
<code>**def _\_init__**(settings: [Settings](#settings))</code><br>
<span class="docs">Creates a new service client with the given settings.</span>

## ServiceError
<code>response: requests.Response
messages: list[dict]</code>
