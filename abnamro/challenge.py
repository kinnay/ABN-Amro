
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from abnamro import streams


def parse_fields(data):
	fields = {}
	stream = streams.StreamIn(data, ">")
	while not stream.eof():
		type = stream.u8()
		size = stream.u16()
		fields[type] = stream.read(size)
	return fields

def serialize_fields(fields):
	stream = streams.StreamOut(">")
	for key, value in fields.items():
		stream.u8(key)
		stream.u16(len(value))
		stream.write(value)
	return stream.get()

def solve_login_challenge(challenge, username, password):
	fields = parse_fields(challenge)
	data = serialize_fields({
		1: b"1",
		2: fields[2],
		3: fields[3],
		8: username.encode(),
		9: password.encode(),
		0: b""
	})
	key = RSA.construct((int.from_bytes(fields[4], "big"), int.from_bytes(fields[5], "big")))
	cipher = PKCS1_v1_5.new(key)
	return cipher.encrypt(data).hex()
