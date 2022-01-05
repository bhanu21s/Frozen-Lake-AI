# -*- coding: utf-8 -*-
"""Model_Based.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RV5pSscGUDJd3lMteuycMcTMEpoAmyMZ
"""
import numpy as np
"""
#Policy evaluation
"""

def policy_evaluation(env, policy, gamma, theta, max_iterations):
    value = np.zeros(env.n_states, dtype=float)

    # TODO:
    while max_iterations:
        max_iterations -= 1
        delta = 0
        for state in range(env.n_states):
            v = value[state]
            value[state] = sum([env.p(next_state, state, policy[state]) * (env.r(next_state, state, policy[state]) + gamma * value[next_state]) for next_state in range(env.n_states)])
            delta = max(delta, abs(v - value[state]))
        if delta < theta:
            break
    return value

"""#Policy improvementation

"""

def policy_improvement(env, value, gamma):
    policy = np.zeros(env.n_states, dtype=int)
    
    # TODO:
    for state in range(env.n_states):
        action_values = [sum([env.p(next_state, state, action) * (env.r(next_state, state, action) + gamma * value[next_state]) for next_state in range(env.n_states)]) for action in range(env.n_actions)]
        policy[state] = np.argmax(action_values)
            
    return policy

"""#Policy iteration"""

def policy_iteration(env, gamma, theta, max_iterations, policy=None):
    if policy is None:
        policy = np.zeros(env.n_states, dtype=int)
    else:
        policy = np.array(policy, dtype=int)
    
    # TODO:
    done = True
    while done:
        policy_pre = policy
        value = policy_evaluation(env, policy, gamma, theta, max_iterations)
        policy = policy_improvement(env, value, gamma)
        if np.array_equal(policy_pre, policy):
            done = False
    return policy, value

"""#Value iteration"""

def value_iteration(env, gamma, theta, max_iterations, value=None):
    if value is None:
        value = np.zeros(env.n_states)
    else:
        value = np.array(value, dtype=np.float)
    
    # TODO:
    while max_iterations:
        max_iterations -= 1
        delta = 0
        for state in range(env.n_states):
            v = value[state]
            action_values = [np.sum([env.p(next_state, state, action)*(env.r(next_state, state, action) + gamma*value[next_state]) for next_state in range(env.n_states)]) for action in range(env.n_actions)]
            value[state] = np.max(action_values)
            delta = max(delta, abs(v - value[state]))
        if delta < theta:
            break
    policy = np.zeros(env.n_states, dtype=int)
    for state in range(env.n_states):
        for next_state in range(env.n_states):
            action_values = [np.sum([env.p(next_state, state, action)*(env.r(next_state, state, action) + gamma*value[next_state]) for next_state in range(env.n_states)]) for action in range(env.n_actions)]
        policy[state] = np.argmax(action_values) 
    return policy, value