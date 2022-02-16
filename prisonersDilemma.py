import random

#Defines the Prisoner's Dilemma game and several possible opponent strategies
class PrisonersDilemma:
	def __init__(self):
		self.default_action = "c"
		self.opponent_last_action = "c" # all implemented opponents start with cooperate by default
		self.game_name = "Test Game"
		self.action_list = ["c", "d"]
		self.payoff = {"cc": (3, 3),
					"dd": (1, 1),
					"cd": (0, 5),
					"dc": (5, 0)}
		self.player_count = 1

	#get_payoff: Returns the payoff for the given actions
	#
	#Parameter: p1_action - The action of the finite state machine
	#Parameter: p2_action - The action of the opponent
	def get_payoff(self, p1_action, p2_action):
		return self.payoff[p1_action + p2_action][0]

	#get_action: Returns the action of the opponent
	#
	#Parameter: opponent_num - Defines which opponent the FSM is playing against
	def get_action(self, opponent_num):
		if opponent_num == 0:
			return self.random_action()
		else:
			return self.random_action()
		# elif opponent_num == 1:
		# 	return self.always_defect()
		# elif opponent_num == 2:
		# 	return self.random_action()
		# elif opponent_num == 3:
		# 	return self.tit_for_tat(self.opponent_last_action)
		# elif opponent_num == 4:
		# 	return self.ms_copycat(self.opponent_last_action)

	#always_cooperate: An opponent strategy where cooperate is played every turn
	def always_cooperate(self):
		return "c"

	#always_defect: An opponent strategy where defect is played every turn
	def always_defect(self):
		return "d"

	#random_action: An opponent strategy where the action is chosen randomly. This choice can be weighted to favor cooperate or defect.
	def random_action(self): #Used for testing increasingly defecting opponents
		if random.uniform(0,1) > 0.5:
			return "c"
		else:
			return "d"

	#tit_for_tat: An opponent strategy that plays whatever action the FSM played last round. Plays cooperate on the first round.
	def tit_for_tat(self, opponent_last_action):
		return opponent_last_action

	#ms_copycat: An opponent strategy for mixed strategy copycat. Has an 80% chance to copy the FSM's last action.
	def ms_copycat(self, opponent_last_action):
		# mixed strategy favoring copy-cat with 80/20 or 20/80
		chance = random.uniform(0, 1)
		if opponent_last_action == "c":
			if chance <	.8:
				return "c"
			else:
				return "d"
		else:
			if chance < 0.8:
				return "d"
			else:
				return "c"
