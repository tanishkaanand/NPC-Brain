import numpy as np
from States import ActionStates, Range, PersonalityIndex

class ActionGenerator:

    def __init__(self):
        # Initialize Q-table
        self.no_of_personality_states = 5    # OCEAN personality model
        self.no_of_ranges_of_personality_states = 3  # 3 ranges for each personality states (0-3, 4-7, 8-10)
        self.no_of_emotional_states = 10  # 10 emotional states
        self.no_of_action_states = 10  # 10 action states

        # initialize Q table
        # 5 ocean personality * 3 ranges (0-3,4-7,8-10) * 10 emotional states * 10 FROM action states * 10 TO action states
        self.Q = np.random.random((no_of_personality_states, no_of_ranges_of_personality_states, no_of_emotional_states, no_of_action_states, no_of_action_states))  # Initialize Q-table with zeros

        # Parameters
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

    def calculate_reward(personality_vector, current_action, next_action):
        reward = 0
        
        # Define all possible transitions and their associated rewards
        transitions = {
            # Unfavorable transitions
            (ActionStates.Patrolling, ActionStates.Attacking): -1,
            (ActionStates.Attacking, ActionStates.Fleeing): -1,
            (ActionStates.Celebrating, ActionStates.Resting): -1,
            (ActionStates.Helping, ActionStates.Attacking): -1,
            (ActionStates.Following, ActionStates.Fleeing): -1,
            # Favorable transitions
            (ActionStates.Interacting, ActionStates.Helping): 1,
            (ActionStates.Interacting, ActionStates.Celebrating): 1,
            (ActionStates.Fleeing, ActionStates.Resting): 1,
            (ActionStates.Fleeing, ActionStates.Interacting): 1,
            (ActionStates.Searching, ActionStates.Interacting): 1,
            (ActionStates.Searching, ActionStates.Patrolling): 1,
            (ActionStates.Attacking, ActionStates.Resting): 1,
            (ActionStates.Attacking, ActionStates.Interacting): 1,
            # Add more transitions as needed
        }

        # Check if the current and next actions correspond to a defined transition
        transition_key = (current_action, next_action)
        if transition_key in transitions:
            reward = transitions[transition_key]

        # print("Transition Reward = ", reward)

        # preferable action states for each personality
        personality_preferences = {
            PersonalityIndex.Openness: {
                Range.High: (ActionStates.Interacting, ActionStates.Celebrating),
                Range.Low: (ActionStates.Resting, ActionStates.Following, ActionStates.Patrolling),
            },
            PersonalityIndex.Conscientiousness: {
                Range.High: (ActionStates.Patrolling, ActionStates.Following, ActionStates.Helping),
                Range.Low: (ActionStates.Resting, ActionStates.Celebrating, ActionStates.Interacting),
            },
            PersonalityIndex.Extraversion: {
                Range.High: (ActionStates.Interacting, ActionStates.Celebrating, ActionStates.Following),
                Range.Low: (ActionStates.Resting, ActionStates.Searching, ActionStates.Patrolling),
            },
            PersonalityIndex.Agreeableness: {
                Range.High: (ActionStates.Helping, ActionStates.Interacting, ActionStates.Celebrating),
                Range.Low: (ActionStates.Attacking, ActionStates.Patrolling, ActionStates.Searching),
            },
            PersonalityIndex.Neuroticism: {
                Range.High: (ActionStates.Resting, ActionStates.Fleeing, ActionStates.Interacting),
                Range.Low: (ActionStates.Patrolling, ActionStates.Attacking, ActionStates.Celebrating),
            },
        }

        # Check if next_action is one of the preferred actions for each personality trait
        for trait, preferences in personality_preferences.items():
            if personality_vector[trait] in preferences:
                if next_action in preferences[personality_vector[trait]]:
                    reward += 1

        # print("Preference Reward = ", reward)
        
        # Normalize the total reward to the range [-1, 1]
        max_reward = max(reward for reward in transitions.values()) + len(personality_preferences)  # Add maximum additional reward
        min_reward = min(reward for reward in transitions.values())
        if max_reward != min_reward:
            normalized_reward = 2 * (reward - min_reward) / (max_reward - min_reward) - 1
        else:
            normalized_reward = 0  # Handle the case where all rewards are the same

        print("Normalised Reward = ", reward)

        return normalized_reward

    def action_generator(self, personality_vector, emotional_state_index, previous_action_state_index) :
        # Choose action based on epsilon-greedy policy
        if np.random.rand() < epsilon: 
            final_action_state_index = np.random.randint(self.no_of_action_states)  # Choose random action
        else:
            # initialize an array for 10 action states with value 1
            q_val_array = np.ones(10)

            for i in (0,4):     # 5 ocean personalities
                for j in (0,9) :    # 10 action states
                    # Q value of jTH action state = product of Q value of the jTH action state of each ocean personality
                    q_val_array[j] *= Q[i][(personality_vector[i]/3)-1][emotional_state_index][previous_action_state_index][j]
            
            # select action state with max q value
            final_action_state_index = np.argmax(q_val_array)  # gives the index of that action state
            print("Final action state index = ", final_action_state_index)

        return final_action_state_index

    def q_learning(self, personality_vector, current_state, next_state) :
        # Define current and next states
        # current_state = (emotional_state_index, action_state_index)
        # next_state = (next_emotional_state_index, next_action_state_index)

        # Execute action and observe reward         ### DIALOGUE GENERATION !!!!!
        reward = self.calculate_reward(current_state[1], next_state[1])

        # Update Q-value using Q-learning update rule
        # for dominant personality !!!!
        self.Q[current_state][final_action_state_index] = (1 - alpha) * self.Q[current_state][final_action_state_index] + alpha * (reward + gamma * np.max(self.Q[next_state]))
