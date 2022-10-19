# import libraries
import numpy as np

np.random.seed(1)
dimension = 4
q_values = np.zeros((dimension, dimension, 4))

# define actions
# numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ["up", "right", "down", "left"]

# Create a 2D numpy array to hold the rewards for each state.

def oned_to_twod(int_val, board_dim=4):
    return (int_val - 1) // board_dim, (int_val - 1) % board_dim


def build_board(user_sequence, dimension=4):
    seq_lst = user_sequence.split(" ")
    goal_1, goal_2, forbidden, wall = list(map(int, seq_lst[:4]))
    mode = seq_lst[4]
    cell_q_to_print = None
    if len(seq_lst) > 5:
        cell_q_to_print = int(seq_lst[-1])

    rewards = np.full((dimension, dimension), -0.1)
    goal_1_i, goal_1_j = oned_to_twod(goal_1)
    rewards[goal_1_i, goal_1_j] = 100.0
    goal_2_i, goal_2_j = oned_to_twod(goal_2)
    rewards[goal_2_i, goal_2_j] = 100.0
    # no need to do anything for wall as the agent will never reach there.
    forbidden_i, forbidden_2_j = oned_to_twod(forbidden)
    rewards[forbidden_i, forbidden_2_j] = -100.0
    return (rewards, mode, cell_q_to_print, goal_1, goal_2, forbidden, wall)


# define a function that determines if the specified location is a terminal state
def is_terminal_state(rewards, current_row_index, current_column_index):
    # if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
    if rewards[current_row_index, current_column_index] == -0.1:
        return False
    else:
        return True

# define a function that will choose a random, non-terminal starting location
def get_starting_location():
    return (0, 1)


# define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action(current_row_index, current_column_index, epsilon):
    # if a randomly chosen value between 0 and 1 is less than epsilon,
    # then choose the most promising value from the Q-table for this state.
    if np.random.random() < epsilon:
        return np.argmax(q_values[current_row_index, current_column_index])
    else:  # choose a random action
        return np.random.randint(4)

# define a function that will get the next location based on the chosen action
def get_next_location(
    current_row_index, current_column_index, action_index, wall_index
):
    new_row_index = current_row_index
    new_column_index = current_column_index
    if actions[action_index] == "down" and current_row_index > 0:
        new_row_index -= 1
    elif actions[action_index] == "right" and current_column_index < dimension - 1:
        new_column_index += 1
    elif actions[action_index] == "up" and current_row_index < dimension - 1:
        new_row_index += 1
    elif actions[action_index] == "left" and current_column_index > 0:
        new_column_index -= 1

    if (new_row_index, new_column_index) == oned_to_twod(wall_index):
        return current_row_index, current_column_index
    return new_row_index, new_column_index


# define training parameters
epsilon = 0.5  # the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.1  # discount factor for future rewards
learning_rate = 0.3  # the rate at which the agent should learn
# run through 1000 training episodes
user_input = input("Enter sequence\n")
rewards, mode, cell_q_to_print, goal_1, goal_2, forbidden, wall_index = build_board(
    user_input
)
for episode in range(10000):
    # get the starting location for this episode
    row_index, column_index = get_starting_location()
    # continue taking actions (i.e., moving) until we reach a terminal state
    # (i.e., until we reach the item packaging area or crash into an item storage location)
    while not is_terminal_state(rewards, row_index, column_index):
        # choose which action to take (i.e., where to move next)
        action_index = get_next_action(row_index, column_index, epsilon)
        # perform the chosen action, and transition to the next state (i.e., move to the next location)
        old_row_index, old_column_index = (
            row_index,
            column_index,
        )  # store the old row and column indexes
        row_index, column_index = get_next_location(
            row_index,
            column_index,
            action_index,
            wall_index,
        )
        # receive the reward for moving to the new state, and calculate the temporal difference
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = (
            reward
            + (discount_factor * np.max(q_values[row_index, column_index]))
            - old_q_value
        )
        # update the Q-value for the previous state and action pair
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[old_row_index, old_column_index, action_index] = new_q_value

if mode == "q":
    q_v_i, q_v_j = oned_to_twod(cell_q_to_print)
    for i, a in enumerate(actions):
        print(a, " " * 4, round(q_values[q_v_i, q_v_j][i], 2))
else:
    for index in range(1, 17):
        if index in [goal_1, goal_2]:
            print(index, " " * 4, "goal")
        elif index == wall_index:
            print(index, " " * 4, "wall-square")
        elif index == forbidden:
            print(index, " " * 4, "forbid")
        else:
            i, j = oned_to_twod(index)
            print(index, " " * 4, actions[np.argmax(q_values[i, j])])
