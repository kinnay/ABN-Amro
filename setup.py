
import setuptools

long_description = \
	"This is an unofficial Python package that implements the ABN AMRO API."

setuptools.setup(
	name = "abnamro",
	version = "1.0.0",
	description = "Unofficial ABN AMRO client",
	long_description = long_description,
	author = "Yannik Marchand",
	author_email = "ymarchand@me.com",
	url = "https://github.com/kinnay/ABN-Amro",
	packages = ["abnamro"],
	install_requires = [
		"pycryptodome",
		"requests"
	]
)
