# simple class to store applicant data
# will most likely require utility methods in the future
class applicant:
	def __init__(self, first_name, last_name, email, password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
