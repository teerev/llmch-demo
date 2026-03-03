from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainConfig:
    total_steps: int = 1000
    max_episode_steps: int = 200
    seed: int = 0
    target_distance: float = 10.0
    log_interval: int = 100
