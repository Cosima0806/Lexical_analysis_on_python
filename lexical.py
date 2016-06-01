#coding:utf-8
import re
from util import *
def readFinals(filename):
	final_list = []
	final_type_dict = {}
	final_pattern = re.compile( r'(?P<final>\S+):(?P<type>\w+)')
	matched = 0
	unmatched = False
	for line in open(filename):
		match = final_pattern.search(line[:-1])
		if match is None:
			unmatched = True
			print '%s cannot be recognized' %(line)
			continue
		else:
			matched += 1
			left = match.group('final')
			right = match.group('type')
			final_list.append(left)
			final_type_dict[left] = right
	print '%d final(s) recognized' %(matched)
	return final_list, final_type_dict

#readFinals('lex_final.txt')

def readProds(filename):
	productions = []
	matched = 0
	unmatched = False
	prod_pattern = re.compile(r'(?P<left>\S+)\s*=\s*((?P<epsilon>\$)|'
				'((?P<right>[^\s\"]+))?\s*\"(?P<terminate>.*)\")')
	for line in open(filename):
		if line[0] == '#':
			continue
		match = prod_pattern.search(line[:-1])
		if match is None:
			unmatched = True
			print '%s cannot be recognized' %(line)
			continue
		else:
			matched += 1
			production = match.groupdict()
			# if production['epsilon'] is not None:
			# 	production['epsilon'] = True
			productions.append(production)
	print '%d production(s) recognized' %(matched)
	return productions

#readProds('lex_prods.txt')

def buildNFA(final_list, productions):
	"""
	alphabet initial
	"""
	alphabet = []
	for i in range(ord(' '), ord('~') + 1):
		alphabet.append(chr(i))
	nfa = NFA(alphabet)

	"""
	final init
	"""
	for final in final_list:
		node = nfa.create_node(True, final)
		nfa.final_state.append(node)


	"""
	unterminates added
	transformation init
	"""
	for p in productions:
		left_state = nfa.get_state_by_name(p['left'])
		if p['right'] is None:
			cur_state = nfa.S
		else:
			cur_state = nfa.get_state_by_name(p['right'])

		for char in p['terminate'][:-1]:
			"""
			tmp states don't need a name
			"""
			tmp_state = nfa.create_node(False, char)
			nfa.add_transfer(cur_state, char, tmp_state)
			cur_state = tmp_state
		nfa.add_transfer(cur_state, p['terminate'][-1:], left_state)
	return nfa

def Scanner(filename):
	final_list, final_type_dict = readFinals('lex_finals.txt')
	productions = readProds('lex_prods.txt')
	nfa = buildNFA(final_list, productions)
	outfile = open('token_table.txt','w+')
	# for state in nfa.final_state:
	# 	print state.data
	# nfa.show_transfer()

	lineNo = 0
	token_table = []
	for line in open(filename):
		lineNo += 1
		token_table_line = []
		lex_error = False
		"""
		int a = 3;
		"""
		start = 0
		pos = 0
		while pos < len(line) and not lex_error:
			while pos < len(line) and (line[pos] == ' ' or line[pos] == '\t'):
					pos += 1
			start = pos
			cur_states = set()
			cur_states.add(nfa.S)
			while pos < len(line):
				# ignore space
				char = line[pos]
				new_states = set()
				for state in cur_states:
					if char in state.transfer:
						new_states = new_states.union(set(state.transfer[char]))
				if not new_states:
					break
				cur_states = new_states
				pos += 1
			"""
			line[pos] = ' '
			"""
			token = line[start:pos]
			lex_error = True
			tmp_table = []
			for state in cur_states:
				if state in nfa.final_state:
					lex_error = False
					tmp_table.append((state.data, token))

			for data, val in tmp_table:
				if data in final_list:
					token_table_line.append( (data, val) )
					break
		for data, val in token_table_line:
			outfile.write('%s\t%s\t%s\n' %(val, data, final_type_dict[data]))

if __name__ == '__main__':
	Scanner('source.txt')
	# for line in open('lex_prods.txt'):
	#  	print line