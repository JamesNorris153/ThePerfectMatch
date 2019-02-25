# simple class to store applicant data
# will most likely require utility methods in the future
class applicant:
	def __init__(self, FName, LName, email, password):
		self.FName = FName
		self.LName = LName
		self.email = email
		self.password = password
