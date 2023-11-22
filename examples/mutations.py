
import abnamro


ACCOUNT_NUMBER = 562813888 # The part of the IBAN behind ABNA
CARD_NUMBER = 231 # The 3-digit number that is written on your card
PASSWORD = "XXXXX" # This is the pin code that you would type into the app


settings = abnamro.Settings()
client = abnamro.ServiceClient(settings)

authorization = abnamro.AuthorizationManager(client, settings)
accounts = abnamro.AccountsManager(client)
mutations = abnamro.MutationsManager(client)

print("Authorizing...")
authorization.login(ACCOUNT_NUMBER, CARD_NUMBER, PASSWORD)
print()

print("Accounts:")
product_groups = ["PAYMENT_ACCOUNTS", "SAVINGS_ACCOUNTS"]
contracts = accounts.list(product_groups=product_groups)
for contract in contracts:
	print("    Name:", contract.product.name)
	print("    IBAN:", contract.account_number)
	print("    Status:", contract.status)
	print("    Owner:", contract.customer.interpay_name)
	if contract.balance:
		print("    Balance:", contract.balance.amount)
	print("    ---")
print()

# Print mutations on the first account in the list
iban = contracts[0].account_number
page_token = None
print("Mutations on %s:" %iban)
for i in range(3):
	list = mutations.search(iban, page_token=page_token)
	for info in list.mutations:
		print("    Amount: %.2f" %info.mutation.amount)
		print("    Name:", info.mutation.counter_account_name)
		print("    Date:", info.mutation.transaction_date.strftime("%Y-%m-%d"))
		print("    ---")
	page_token = list.page_token
