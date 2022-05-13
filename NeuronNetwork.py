import gym
from stable_baselines3 import PPO
import os
import time
from environment import FlippyEnv
# from stable_baselines3.common.env_checker import  check_env

models_dir = f"models/5/"
logdir = f"logs/5/"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)

env = FlippyEnv()
env.reset()

# check_env(env)

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

model_path = "models/5/90000.zip"
model = PPO.load(model_path, env=env)

# TIMESTEPS = 10000
# iters = 0
# while True:
# 	iters += 1
# 	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
# 	model.save(f"{models_dir}/{TIMESTEPS*iters}")




episodes = 5

for ep in range(episodes):
	obs = env.reset()
	score = 0
	done = False
	while not done:
		action, _states = model.predict(obs)
		obs, rewards, done, info = env.step(action)
		env.render()
		score += rewards
	print(score)