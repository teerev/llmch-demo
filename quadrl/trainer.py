from __future__ import annotations

from quadrl.config import TrainConfig
from quadrl.env import QuadrupedEnv
from quadrl.policy import RandomPolicy


def train(config: TrainConfig) -> dict:
    """Run an environment-policy loop for a fixed number of steps.

    Returns:
        dict with keys:
            - 'episodes' (int): number of completed episodes
            - 'steps' (int): total environment steps taken (== config.total_steps)
            - 'total_reward' (float): sum of rewards over all steps
    """
    if int(config.total_steps) < 0:
        raise ValueError("config.total_steps must be >= 0")

    env = QuadrupedEnv(config)
    policy = RandomPolicy(config)

    total_reward = 0.0
    steps = 0
    episodes = 0

    # Start first episode
    obs = env.reset()

    while steps < int(config.total_steps):
        action = policy.act(obs)
        obs, reward, done, _info = env.step(action)

        total_reward += float(reward)
        steps += 1

        if done and steps < int(config.total_steps):
            episodes += 1
            obs = env.reset()

    # If we ended exactly on an episode boundary, count that episode as completed.
    if steps > 0 and (env.steps == 0 or env.steps >= int(config.max_episode_steps) or env.position >= env.target):
        # env.steps == 0 would only happen if total_steps == 0, handled below.
        if steps == int(config.total_steps) and env.steps != 0:
            episodes += 1

    if int(config.total_steps) == 0:
        episodes = 0

    return {
        "episodes": int(episodes),
        "steps": int(steps),
        "total_reward": float(total_reward),
    }
