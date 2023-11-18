
import datetime
import inspect


class ValidationError(Exception):
	pass


class Field:
	def __init__(self, name, *, required=False, repeated=False):
		self.name = name
		self.required = required
		self.repeated = repeated
	
	def encode(self, value): return value
	def parse(self, value): return value


class BooleanField(Field):
	def parse(self, value):
		if not isinstance(value, bool):
			raise ValidationError("Expected a boolean, got %s" %type(value))
		return value


class IntegerField(Field):
	def parse(self, value):
		if not isinstance(value, int):
			raise ValidationError("Expected an integer, got %s" %type(value))
		return value


class FloatField(Field):
	def parse(self, value):
		if not isinstance(value, float):
			raise ValidationError("Expected a float, got %s" %type(value))
		return value


class StringField(Field):
	def __init__(self, name, *, choices=None, **kwargs):
		super().__init__(name, **kwargs)
		self.choices = choices
	
	def parse(self, value):
		if not isinstance(value, str):
			raise ValidationError("Expected a string, got %s" %type(value))
		if self.choices is not None and value not in self.choices:
			raise ValidationError("Received unexpected enum value '%s'" %value)
		return value


class DateTimeField(Field):
	def __init__(self, name, format, **kwargs):
		super().__init__(name, **kwargs)
		self.format = format
	
	def encode(self, value):
		return value.strftime(self.format)
	
	def parse(self, value):
		if not isinstance(value, str):
			raise ValidationError("Expected a string, got %s" %type(value))
		return datetime.datetime.strptime(value, self.format)


class TimestampField(Field):
	def encode(self, value):
		try:
			return int(value.timestamp() * 1000)
		except ValueError:
			return -62135773200000
	
	def parse(self, value):
		if not isinstance(value, int):
			raise ValidationError("Expected an integer, got %s" %type(value))
		
		try:
			return datetime.datetime.fromtimestamp(value / 1000)
		except ValueError:
			return datetime.datetime.min


class ObjectField(Field):
	def __init__(self, name, schema, **kwargs):
		super().__init__(name, **kwargs)
		self.schema = schema
	
	def encode(self, value):
		return value.encode()
	
	def parse(self, value):
		if not isinstance(value, dict):
			raise ValidationError("Expected a dict, got %s" %type(value))
		return self.schema.create(value)


class Schema:
	def __init__(self):
		self.reset()
	
	def __repr__(self):
		fields = []
		for name, field in inspect.get_annotations(self.__class__).items():
				fields.append("%s=%r" %(field.name, getattr(self, name)))
		return "%s(%s)" %(self.__class__.__name__, ", ".join(fields))
	
	def reset(self):
		for name, field in inspect.get_annotations(self.__class__).items():
			setattr(self, name, None)
	
	def parse(self, data):
		annotations = inspect.get_annotations(self.__class__)

		for name, field in annotations.items():
			setattr(self, name, self.parse_value(field, data.get(field.name)))
		
		names = [field.name for field in annotations.values()]
		for field in data:
			if field not in names:
				raise ValidationError("Received unexpected field '%s'" %field)
	
	def parse_value(self, field, value, is_nested=False):
		if value is None:
			if field.required:
				raise ValidationData("Received null value on required field '%s'" %field.name)
			return value
		
		if field.repeated and not is_nested:
			if not isinstance(value, list):
				raise ValidationError("Expected a list, got %s" %type(value))
			return [self.parse_value(field, element, True) for element in value]
		
		return field.parse(value)

	def encode(self):
		data = {}
		for name, field in inspect.get_annotations(self.__class__).items():
			value = getattr(self, name)
			if value is not None:
				value = field.encode()
			data[field.name] = value
		return data
	
	@classmethod
	def create(cls, data):
		inst = cls()
		inst.parse(data)
		return inst
