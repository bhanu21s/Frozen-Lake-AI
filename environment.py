# -*- coding: utf-8 -*-
"""Environment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t3HerxMVyhHKfEXHwmbUHGhuIAj01CUc
"""

import numpy as np
import contextlib

"""# Configures numpy print options"""

@contextlib.contextmanager
def _printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    try:
        yield
    finally: 
        np.set_printoptions(**original)

"""#EnvironmentModel"""

class EnvironmentModel:
    def __init__(self, n_states, n_actions, seed=None):
        self.n_states = n_states
        self.n_actions = n_actions
        
        self.random_state = np.random.RandomState(seed)
        
    def p(self, next_state, state, action):
        raise NotImplementedError()
    
    def r(self, next_state, state, action):
        raise NotImplementedError()
        
    def draw(self, state, action):
        p = [self.p(ns, state, action) for ns in range(self.n_states)]
        next_state = self.random_state.choice(self.n_states, p=p)
        reward = self.r(next_state, state, action)
        
        return next_state, reward

"""#Environment"""

class Environment(EnvironmentModel):
    def __init__(self, n_states, n_actions, max_steps, pi, seed=None):
        EnvironmentModel.__init__(self, n_states, n_actions, seed)
        
        self.max_steps = max_steps
        
        self.pi = pi
        if self.pi is None:
            self.pi = np.full(n_states, 1./n_states)
        
    def reset(self):
        self.n_steps = 0
        self.state = self.random_state.choice(self.n_states, p=self.pi)
        
        return self.state
        
    def step(self, action):
        if action < 0 or action >= self.n_actions:
            raise Exception('Invalid action.')
        
        self.n_steps += 1
        done = (self.n_steps >= self.max_steps)
        
        self.state, reward = self.draw(self.state, action)
        
        return self.state, reward, done
    
    def render(self, policy=None, value=None):
        raise NotImplementedError()

"""#Frozen Lake environment"""

class FrozenLake(Environment):
    def __init__(self, lake, slip, max_steps, seed=None):
        """
        lake: A matrix that represents the lake. For example:
         lake =  [['&', '.', '.', '.'],
                  ['.', '#', '.', '#'],
                  ['.', '.', '.', '#'],
                  ['#', '.', '.', '$']]
        slip: The probability that the agent will slip
        max_steps: The maximum number of time steps in an episode
        seed: A seed to control the random number generator (optional)
        """
        # start (&), frozen (.), hole (#), goal ($)
        self.lake = np.array(lake)
        self.lake_flat = self.lake.reshape(-1)
        
        self.slip = slip
        
        n_states = self.lake.size + 1
        n_actions = 4
        
        pi = np.zeros(n_states, dtype=float)
        pi[np.where(self.lake_flat == '&')[0]] = 1.0
        
        self.absorbing_state = n_states - 1
        #TODO
        self.n_states = n_states
        self.n_actions = n_actions
        self.random_state = np.random.RandomState(seed)
        self.pi = pi
        self.max_steps = max_steps
        holes = np.where(self.lake_flat == "#")[0]
        self.goal = np.where(self.lake_flat == "$")
        self.actions= [ -len(self.lake[0]) , -1 , len(self.lake[0]), 1]
        self.tp = np.zeros((n_states, n_states, n_actions))
        for state in range(n_states):
            for action, op in enumerate(self.actions):
                nxt = state + op
                if action == 0 and state < n_states - 2  and state not in holes: #for valid action "up"
                    if nxt >=0:
                        next_state = nxt
                    else: 
                        next_state = state
                
                if action == 1 and state not in holes and state < n_states - 2: #for valid action "left"
                    if  nxt >= 0 and state % len(self.lake[0]) !=0:
                        next_state = nxt
                    else:
                        next_state = state
                if action == 2 and state < n_states - 2  and state not in holes: #for valid action "down"
                    if nxt < n_states - 1:
                        next_state = nxt
                    else: 
                        next_state = state
                if action == 3 and state not in holes and state < n_states - 2: #for valid action "right"
                    if  nxt >= 0 and (state + 1) % len(self.lake[0]) !=0:
                        next_state = nxt
                    else:
                        next_state = state 
                if state == self.absorbing_state or state in holes or state in self.goal:
                    self.tp[self.absorbing_state, state, action] = 1  
                else:      
                    self.tp[next_state, state, action] += 1 - self.slip
                    for i in range(n_actions):
                        self.tp[next_state, state, i] += (self.slip/n_actions)
        
        
    def step(self, action):
        state, reward, done = Environment.step(self, action)
        
        done = (state == self.absorbing_state) or done
        
        return state, reward, done
        
    def p(self, next_state, state, action):
        # TODO:
        return self.tp[next_state, state, action]
    
    def r(self, next_state, state, action):
        # TODO:
        if state in self.goal:
            return 1
        else:
            return 0 
   
    def render(self, policy=None, value=None):
        if policy is None:
            lake = np.array(self.lake_flat)
            
            if self.state < self.absorbing_state:
                lake[self.state] = '@'
                
            print(lake.reshape(self.lake.shape))
        else:
            # UTF-8 arrows look nicer, but cannot be used in LaTeX
            # https://www.w3schools.com/charsets/ref_utf_arrows.asp
            actions = ['^', '<', '_', '>']
            
            print('Lake:')
            print(self.lake)
        
            print('Policy:')
            policy = np.array([actions[a] for a in policy[:-1]])
            print(policy.reshape(self.lake.shape))
            
            print('Value:')
            with _printoptions(precision=3, suppress=True):
                print(value[:-1].reshape(self.lake.shape))

"""#Human interface"""

def play(env):
    actions = ['w', 'a', 's', 'd']
    
    state = env.reset()
    env.render()
    
    done = False
    while not done:
        c = input('\nMove: ')
        if c not in actions:
            raise Exception('Invalid action')
            
        state, r, done = env.step(actions.index(c))
        
        env.render()
        print('Reward: {0}.'.format(r))