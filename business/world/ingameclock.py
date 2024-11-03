class InGameClock:
    """Singleton class to manage in-game time.

    The InGameClock tracks the elapsed game time, allowing for consistent timing 
    across different components of the game. This class ensures that only one 
    instance exists throughout the game's lifecycle.

    Attributes:
        initial_time (float): The starting time for the game clock.
        __time_elapsed (float): The total time elapsed in the game since initialization.
    """

    _instance = None  # Private class attribute to hold the singleton instance

    def __new__(cls, initial_time: float = 0):
        """Create a new instance of InGameClock or return the existing instance.

        Args:
            cls: The class being instantiated.
            initial_time (float): The initial time to set for the clock (default is 0).

        Returns:
            InGameClock: The singleton instance of the clock.
        """
        if cls._instance is None:
            # Create a new instance if one does not already exist
            cls._instance = super(InGameClock, cls).__new__(cls)
            cls._instance.initial_time = initial_time
            cls._instance.__time_elapsed = initial_time  # Initialize elapsed time
        return cls._instance

    def update(self, delta_time: float):
        """Update the elapsed time by adding the time since the last frame.

        Args:
            delta_time (float): The time in seconds to add to the elapsed time.
        """
        self.__time_elapsed += delta_time

    @property
    def time_elapsed(self):
        """Get the total elapsed time in the game.

        Returns:
            float: The total time elapsed in milliseconds.
        """
        return self.__time_elapsed * 1000  # Convert elapsed time to milliseconds
