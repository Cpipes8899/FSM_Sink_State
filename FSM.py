import random

#Defines a Finite State Machine, which is a collection of nodes/states and transitions.
#
#FSMs have a fitness score that reflects how well it plays the Prisoner's Dilemma game.
class FSM:
	number_of_nodes = 18 # this value was found from a related paper
	def __init__(self, game_action_list, node_list=None):
		self.node_list = []
		if node_list == None:
			self.generate_nodes(game_action_list)
		else:
			self.node_list = node_list
		self.fitness_score = 0
		self.current_state = 0 # index in the nodelist that represents the current state
		self.payoff_list = []

	#generate_nodes: Used to randomly generate nodes for a new FSM.
	#
	#Parameter: game_action_list - A list of possible actions for the game. In this case, cooperate and defect.
	def generate_nodes(self, game_action_list):
		for x in range(FSM.number_of_nodes):
			self.node_list.append(Node(game_action_list))

	#get_action: Retruns the action of the current state from the node list.
	def get_action(self):
		return self.node_list[self.current_state].action

	#update_state: Update the FSMs current state based on what action the opponent played.
	def update_state(self, opponent_action):
		self.current_state = self.node_list[self.current_state].transition_dict[opponent_action]

	#reset: Reset the current state.
	def reset(self):
		self.current_state = 0

	#get_num_sink_states: Returns the number of sink states in a FSM.
	def get_num_sink_states(self): 
		num_sink_states = 0
		for x in range(FSM.number_of_nodes):
			if self.node_list[x].transition_dict["c"] == x and self.node_list[x].transition_dict["d"] == x:
				num_sink_states += 1
		return num_sink_states

#Defines a Node, which holds the action and transition information.
class Node:
	def __init__(self, game_action_list, action=None, transition_dict=None):
		if action == None:
			self.action = random.choice(game_action_list)
		else:
			self.action = action
		if transition_dict == None:
			self.transition_dict = self.generate_intial_dict(game_action_list) # intial value for transitions is random
		else:
			self.transition_dict = transition_dict
		
	#generate_initial_dict: Initializes the transition dictionary with random transitions.
	#
	#Parameter: game_action_list - A list of possible actions for the game. In this case, cooperate and defect.
	def generate_intial_dict(self, game_action_list):
		transition_dict = {}
		for action in game_action_list:
			transition_dict[action] = random.randint(1, FSM.number_of_nodes) - 1
		return transition_dict

