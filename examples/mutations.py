
import abnamro


ACCOUNT_NUMBER = 8731326943 # The part of the IBAN behind ABNA
CARD_NUMBER = 231 # The 3-digit number that is written on your card
PASSWORD = "XXXXX" # This is the pin code that you would type into the app


settings = abnamro.Settings()
client = abnamro.ServiceClient(settings)

authorization = abnamro.AuthorizationManager(client, settings)
debitcards = abnamro.DebitCardsManager(client)
mutations = abnamro.MutationsManager(client)

print("Authorizing...")
authorization.login(ACCOUNT_NUMBER, CARD_NUMBER, PASSWORD)
print()

print("Debit cards:")
print("---")
cards = debitcards.list()
for card in cards:
	print("IBAN:", card.id.iban)
	print("Card number:", card.id.card_number)
	print("Status:", card.status)
	print("Owner:", card.owner_name)
	print("Product:", card.product_name)
	print("---")
print()

# Print mutations on the first debit card
iban = cards[0].id.iban
last_mutation_key = None
print("%s:" %iban)
print("---")
for i in range(3):
	list = mutations.search(iban, last_mutation_key=last_mutation_key)
	for info in list.mutations:
		print("Amount: %.2f" %info.mutation.amount)
		print("Name:", info.mutation.counter_account_name)
		print("Date:", info.mutation.transaction_date.strftime("%Y-%m-%d"))
		print("---")
	last_mutation_key = list.last_mutation_key
