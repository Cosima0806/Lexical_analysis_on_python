class NFANode:
	def __init__(self, isfinal = False, data = None):
		self.transfer = {}
		self.isfinal = isfinal
		self.data = data

	def add_transfer(self, char, v):
		if char not in self.transfer:
			self.transfer[char] = []
		self.transfer[char].append(v)

	def show_transfer(self, char):
		if char in self.transfer:
			for nxt in self.transfer[char]:
				print char, nxt.data

class NFA:
	def __init__(self, alphabet):
		self.alphabet = alphabet
		self.states = []
		self.name_state_dict = {}
		self.final_state = []
		self.S = self.create_node(False, 'S')
		

	def create_node(self, isfinal=False, name=None):
		node = NFANode(isfinal, name)
		self.states.append(node)
		if name:
			self.name_state_dict[name] = node
		return node

	def add_transfer(self, u, char, v):
		if (u not in self.states) or (char not in self.alphabet) or (v not in self.states):
			raise Exception('ERROR: illegal transfer')
		u.add_transfer(char, v)

	def get_state_by_name(self, name):
		"""
		when we need a state by a name, if it doesn't exist, we need to create it
		"""
		if name not in self.name_state_dict:
			self.name_state_dict[name] =None
			self.name_state_dict[name] = self.create_node(False, name)
		return self.name_state_dict[name]

	def show_transfer(self):
		for state in self.states:
			print '======%s======' %(state.data)
			for char in self.alphabet:
				state.show_transfer(char)


