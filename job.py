# simple class to store job data
# will most likely require utility methods in the future
class job:
	def __init__(self, name, description, deadline, location, position):
		self.name = name
		self.description = description
		self.deadline = deadline
		self.location = location
		self.position = position
