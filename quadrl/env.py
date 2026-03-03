from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from quadrl.config import TrainConfig


class QuadrupedEnv:
    """Deterministic stub environment.

    State:
        - position: scalar float, starts at 0.0
        - target: config.target_distance

    Action:
        - action: float, added to position each step

    Reward:
        - -abs(target - position)

    Termination:
        - steps >= config.max_episode_steps OR position >= target
    """

    def __init__(self, config: TrainConfig):
        self.config = config
        self.target = float(config.target_distance)
        self.position = 0.0
        self.steps = 0

    def reset(self) -> Dict[str, float]:
        self.position = 0.0
        self.steps = 0
        return {"position": float(self.position), "target": float(self.target)}

    def step(self, action: float) -> Tuple[Dict[str, float], float, bool, Dict[str, float]]:
        self.steps += 1
        self.position += float(action)

        distance_to_target = float(self.target - self.position)
        reward = -abs(distance_to_target)

        done = (self.steps >= int(self.config.max_episode_steps)) or (self.position >= self.target)

        obs = {"position": float(self.position), "target": float(self.target)}
        info: Dict[str, float] = {
            "steps": float(self.steps),
            "distance_to_target": float(distance_to_target),
        }
        return obs, float(reward), bool(done), info
