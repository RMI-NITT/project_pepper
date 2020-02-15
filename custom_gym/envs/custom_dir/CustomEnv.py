import gym
class CustomEnv(gym.Env):
	def _init_(self):
		print('Environment initialized')
	def step(self):
		print('success')
	def reset(self):
		print('reset')