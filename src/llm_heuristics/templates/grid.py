from heuristics.heuristic_base import Heuristic

class GridHeuristic(Heuristic):
    """
    A domain-dependent heuristic for the grid domain.

    # Summary
    This heuristic estimates the number of actions required to move all keys to their goal locations.
    The heuristic assumes the robot can move freely between any two places (ignoring locked doors) and 
    computes the minimal movement cost by summing the shortest path distances for each key from the robot's 
    current location to the key's current location and then to the key's goal location. The robot's location 
    is updated after each key is placed at its goal.

    # Assumptions
    - The robot can carry only one key at a time, requiring sequential movement of keys.
    - All doors are assumed to be open for path calculation (ignoring unlock actions, which is an overestimate).
    - The graph of places (from static conn facts) is connected and undirected.
    - The goal state is reached when all keys are at their specified goal locations.

    # Heuristic Initialization
    - Precomputes all-pairs shortest path distances between places using the static conn graph.
    - Builds a mapping from goal conditions to key-goal location pairs.

    # Step-By-Step Thinking for Computing Heuristic
    1. **Precomputation**:
        - Extract all places from static facts (place ?p).
        - Build an undirected graph from conn facts (conn ?a ?b).
        - Compute shortest path distances between every pair of places using BFS.

    2. **State Processing**:
        - Identify the robot's current location from (at-robot ?x).
        - Map goal conditions to key-goal location pairs (from task.goals).

    3. **Key Movement Cost Calculation**:
        - For each key in the goal:
            a. Determine the key's current location:
                - If the robot is holding the key (holding ?key), current location = robot's location.
                - Else, find the key's location from (at ?key ?loc).
            b. Skip if the key is already at the goal location.
            c. Compute movement cost: 
                - Distance from current robot location to key's current location.
                - Distance from key's current location to key's goal location.
            d. Add the cost to the total and update the robot's current location to the key's goal.
        - Return the accumulated total cost.

    4. **Edge Handling**:
        - If a key is missing in the state (should not occur in solvable states), skip it.
        - The heuristic returns 0 for goal states (all keys at goals).
    """

    def __init__(self, task):
        """Initialize the heuristic by precomputing place graph and shortest paths."""
        self.goals = task.goals
        static_facts = task.static

        # Extract all places
        places = set()
        for fact in static_facts:
            if fact.startswith('(place '):
                parts = fact[1:-1].split()
                places.add(parts[1])
        
        # Build graph from conn facts
        graph = {place: [] for place in places}
        for fact in static_facts:
            if fact.startswith('(conn '):
                parts = fact[1:-1].split()
                if len(parts) >= 3:
                    a, b = parts[1], parts[2]
                    if a in graph and b in graph:
                        graph[a].append(b)
                        graph[b].append(a)
        
        # Compute all-pairs shortest paths using BFS
        distances = {}
        for place in places:
            dist = {place: 0}
            queue = [place]
            while queue:
                node = queue.pop(0)
                for neighbor in graph[node]:
                    if neighbor not in dist:
                        dist[neighbor] = dist[node] + 1
                        queue.append(neighbor)
            distances[place] = dist
        self.distances = distances

        # Build goal_key_map: key -> goal location
        self.goal_key_map = {}
        for goal in self.goals:
            parts = goal[1:-1].split()
            if parts[0] == 'at' and len(parts) >= 3:
                key = parts[1]
                goal_loc = parts[2]
                self.goal_key_map[key] = goal_loc

    def __call__(self, node):
        """Estimate the minimal number of actions to move all keys to their goals."""
        state = node.state
        robot_loc = None
        # Extract robot location
        for fact in state:
            if fact.startswith('(at-robot '):
                parts = fact[1:-1].split()
                robot_loc = parts[1]
                break
        if robot_loc is None:
            # Fallback: use the first place (should not happen)
            robot_loc = next(iter(self.distances.keys()))

        total_cost = 0
        current_loc = robot_loc

        for key, goal_loc in self.goal_key_map.items():
            # Determine current location of the key
            if f'(holding {key})' in state:
                current_key_loc = robot_loc
            else:
                current_key_loc = None
                for fact in state:
                    if fact.startswith(f'(at {key} '):
                        parts = fact[1:-1].split()
                        if len(parts) >= 3 and parts[1] == key:
                            current_key_loc = parts[2]
                            break
                if current_key_loc is None:
                    # Key not found (should not occur in solvable state), skip
                    continue

            # Skip if key is already at goal
            if current_key_loc == goal_loc:
                continue

            # Add movement cost: current_loc -> current_key_loc -> goal_loc
            d1 = self.distances[current_loc].get(current_key_loc, float('inf'))
            d2 = self.distances[current_key_loc].get(goal_loc, float('inf'))
            total_cost += d1 + d2

            # Update robot location to goal after placing the key
            current_loc = goal_loc

        return total_cost