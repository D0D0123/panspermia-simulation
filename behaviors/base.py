"""
Base class for tick behaviors in the Panspermia Simulation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class TickBehavior(ABC):
    """Base class for all tick behaviors."""

    def __init__(self, config):
        """
        Initialize the behavior with a configuration.

        Args:
            config: SimulationConfig instance
        """
        self.config = config
        self.enabled = True
        self.stats = {}

    @abstractmethod
    def execute(self, grid, tick_number: int):
        """
        Execute this behavior for the current tick.

        Args:
            grid: Grid instance
            tick_number: Current tick number
        """
        pass

    def get_stats(self) -> Dict[str, Any]:
        """
        Return statistics collected by this behavior.

        Returns:
            Dictionary of statistics
        """
        return self.stats

    def reset_stats(self):
        """Reset statistics for this behavior."""
        self.stats = {}
