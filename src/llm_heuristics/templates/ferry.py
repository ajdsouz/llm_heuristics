from heuristics.heuristic_base import Heuristic

class FerryHeuristic(Heuristic):
    """
    A domain-dependent heuristic for the ferry domain.

    # Summary
    This heuristic estimates the number of actions required to transport all cars to their goal locations by accounting for:
    - The current state of the ferry (empty or carrying a car) and its location.
    - The location of each car (on ground or on ferry).
    - The minimal actions needed to board, sail, and debark each car, including ferry movements to reach car locations.

    # Assumptions
    - The ferry can carry at most one car at a time (empty-ferry must be true to board).
    - The ferry can sail directly between any two distinct locations in one action.
    - Each car must be transported individually (one at a time).
    - The goal state requires all cars to be at their specified goal locations (on the ground).

    # Heuristic Initialization
    - Extracts goal locations for each car from the task's goal conditions.
    - Stores goal locations in a dictionary mapping car names to goal locations.

    # Step-By-Step Thinking for Computing Heuristic
    1. **Identify the car on the ferry (if any)**:
        - If the ferry is carrying a car, compute the cost to get that car to its goal:
          - If the ferry is already at the goal location: 1 action (debark).
          - Otherwise: 2 actions (sail to goal, then debark).
        - This cost is added to the total.

    2. **Determine ferry location after handling the car on the ferry**:
        - If a car was on the ferry, the ferry will be at that car's goal location after debarking.
        - If no car was on the ferry, the ferry remains at its current location (from the state).

    3. **Process each car not on the ferry and not at its goal**:
        - For each car not at its goal and not on the ferry:
          - Check if the ferry (after handling the car on the ferry) is already at the car's current location.
          - If not, add 1 action to move the ferry to the car's location.
          - Add 3 actions for boarding, sailing to the goal, and debarking.
        - Sum these costs for all such cars.

    4. **Return the total estimated actions**:
        - The heuristic value is the sum of costs from steps 1 and 3.
        - The heuristic is 0 for goal states (all cars at goals).

    Example: 
        Ferry starts at loc2, car1 at loc1 (goal loc2).
        - No car on ferry: Step 1 cost = 0.
        - Ferry location after Step 1 = loc2.
        - Car1: ferry (loc2) != car location (loc1) â†’ extra cost = 1.
        - Total cost = 1 + 3 = 4 (matches the minimal solution: sail loc2â†’loc1, board, sail loc1â†’loc2, debark).
    """

    def __init__(self, task):
        """Initialize the heuristic by extracting goal locations for each car."""
        self.goal_locations = {}
        for goal in task.goals:
            # Parse goal: "(at car1 loc2)" â†’ ['at', 'car1', 'loc2']
            parts = goal[1:-1].split()
            if parts[0] == "at" and len(parts) >= 3:
                car = parts[1]
                loc = parts[2]
                self.goal_locations[car] = loc

    def __call__(self, node):
        """Estimate the minimal number of actions to reach the goal state."""
        state = node.state

        # Step 1: Handle the car on the ferry (if any)
        on_ferry = []
        for fact in state:
            if fact.startswith("(on "):
                # Extract car name from "(on car1)"
                car = fact[4:-1].split()[0]  # Remove "(on " and trailing ')'
                on_ferry.append(car)
                break  # Only one car can be on the ferry

        total_actions = 0
        if on_ferry:
            car = on_ferry[0]
            if car in self.goal_locations:
                goal = self.goal_locations[car]
                # Find current ferry location
                ferry_loc = None
                for fact in state:
                    if fact.startswith("(at-ferry "):
                        ferry_loc = fact[10:-1]  # Remove "(at-ferry " and ')'
                        break
                if ferry_loc is None:
                    ferry_loc = "loc1"  # Fallback for invalid state
                # Cost to get car on ferry to goal
                if ferry_loc == goal:
                    total_actions += 1  # Debark only
                else:
                    total_actions += 2  # Sail to goal, then debark

        # Step 2: Determine ferry location after handling the car on the ferry
        if on_ferry:
            ferry_after = self.goal_locations[on_ferry[0]]
        else:
            ferry_after = None
            for fact in state:
                if fact.startswith("(at-ferry "):
                    ferry_after = fact[10:-1]
                    break
            if ferry_after is None:
                ferry_after = "loc1"  # Fallback

        # Step 3: Process each car not on ferry and not at goal
        for car, goal in self.goal_locations.items():
            # Skip if car is on ferry (already handled)
            if on_ferry and car == on_ferry[0]:
                continue
            # Check if car is already at goal (on ground)
            car_at_goal = False
            for fact in state:
                if fact.startswith(f"(at {car} "):
                    parts = fact[1:-1].split()
                    if len(parts) >= 3 and parts[2] == goal:
                        car_at_goal = True
                        break
            if car_at_goal:
                continue
            # Find current location of the car (on ground)
            current_loc = None
            for fact in state:
                if fact.startswith(f"(at {car} "):
                    parts = fact[1:-1].split()
                    if len(parts) >= 3:
                        current_loc = parts[2]
                        break
            if current_loc is None:
                continue  # Car not found (should not happen in valid state)
            # Add cost for ferry movement to car's location (if needed)
            extra = 1 if ferry_after != current_loc else 0
            total_actions += extra + 3  # Board (1) + Sail (1) + Debark (1)

        return total_actions