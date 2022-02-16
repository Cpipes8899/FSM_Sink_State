from prisonersDilemma import PrisonersDilemma
from FSM import *
import random
import copy
import math

lower_num_games = 50
upper_num_games = 50
# number of rounds for each game for scoring for upcoming generation
num_rounds = random.randint(lower_num_games, upper_num_games) 



game = PrisonersDilemma()


#make_child: Create a child FSM from a parent FSM with a 25% chance of mutation
#
#Parameter: fsm - The parent finite state machine
def make_child(fsm):
	child_fsm = copy.deepcopy(fsm)

	child_fsm.fitness_score = 0
	child_fsm.payoff_list.clear()
	chance_to_mutate = .25
	for node in child_fsm.node_list:	
		chance = random.uniform(0, 1)
		if chance <= chance_to_mutate:
			chance = random.uniform(0, 1)
			if chance < 0.5:
				change_node_action(node)
			else:
				change_transition_destination(node)

	evaluate(child_fsm)
	return child_fsm

#change_tranition_destination: Change the action of a node. This is a mutation function.
#
#
#Parameter: node - The node to be changed
def change_node_action(node):
	choice = random.choice(game.action_list)
	while choice == node.action:
		choice = random.choice(game.action_list)
	node.action = choice

#change_tranition_destination: Change the destination of a node transition. This is a mutation function.
#
#
#Parameter: node - The node to be changed
def change_transition_destination(node):
	max_change = len(game.action_list) # maximum number of allowed changes
	for i in range(max_change):
		chance = random.uniform(0, 1)
		if chance <= (1/(i+1)):
			transition_action = random.choice(game.action_list) # random so as to not "favor" lower indexes
			# change the value for the above key in node's dictionary
			node.transition_dict[transition_action] = random.randint(1, FSM.number_of_nodes) - 1
		else: 
			break # breaks if "chance" doesn't make the cutoff -> favors low numbers of changes


#evaluate: Determine the fitness score of a finite state machine by
#		   playing against the opponent(s)
#
#Parameter: fsm - The finite state machine to be evaluated
def evaluate(fsm): 
	total_payoff = 0
	for i in range(game.player_count): 
		game.opponent_last_action = game.default_action
		fsm.reset()
		current_payoff = 0
		for j in range(num_rounds):
			# get player actions
			p1_action = fsm.get_action()
			p2_action = game.get_action(i)
			#player_actions = p1_action + p2_action
			current_payoff += game.get_payoff(p1_action, p2_action)
			# update information before next round
			fsm.update_state(p2_action)
			game.opponent_last_action = p1_action
		fsm.payoff_list.append(current_payoff)
		total_payoff += current_payoff
	
	fsm.fitness_score = total_payoff



num_fresh_populations = 5 #Reduced to 5 for demonstration. 1000 used for data collection.
total_num_sink_states = 0
std_dev_list = []
for q in range(num_fresh_populations): #Evolutionary learning main loop
	population = [] # list of all current individuals
	population_size = 50
	for x in range(population_size):
		population.append(FSM(game.action_list))	

	for member in population:
		evaluate(member)

	population.sort(key=lambda x: x.fitness_score, reverse=True)

	#Reset variables
	iterations = 0
	best_score = population[0].fitness_score
	rounds_since = 0
	while True: #Evolutionary learning inner loop
		if population[0].fitness_score > best_score:
			best_score = population[0].fitness_score
			rounds_since = 0
		else:
			rounds_since += 1

		if rounds_since >= 50:
			break #Stop evolutionary learning early if no improvement is being made

		# Create the next generation of the population
		next_generation = []
		for member in population:
			next_generation.append(make_child(member))
		population.extend(next_generation)
		population.sort(key=lambda x: x.fitness_score, reverse=True)
		population = population[0:population_size]
		if iterations > 500:
			break
		iterations += 1

	total_num_sink_states += population[0].get_num_sink_states()
	std_dev_list.append(population[0].get_num_sink_states())


#Calculating the standard deviation, variance, and standard error of the mean
mean_num_sink_states = total_num_sink_states/num_fresh_populations
sum_std_dev = 0
for num_sink_states in std_dev_list:
	diff_std_dev = (num_sink_states - mean_num_sink_states)
	pow_std_dev = pow(diff_std_dev, 2)
	sum_std_dev += pow_std_dev

#Variance
variance = sum_std_dev/num_fresh_populations
variance = round(variance, 4)

#Standard Deviation
std_deviation = math.sqrt(variance)
std_deviation = round(std_deviation, 4)

#Standard error of the mean
root_sample_size = math.sqrt(num_fresh_populations)
std_error_of_mean = std_deviation/root_sample_size
std_error_of_mean = round(std_error_of_mean, 4)

print("Average number of sink states:", (total_num_sink_states/num_fresh_populations))
print("Standard Deviation: ", (std_deviation))
print("Variance: ", (variance))
print("Standard Error of the Mean: ", (std_error_of_mean))
