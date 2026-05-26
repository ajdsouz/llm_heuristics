import argparse

from tarski.io import PDDLReader
from tarski.syntax import Atom


def atom_to_string(atom: Atom) -> str:
    """
    Convert a Tarski atom into a pyperplan-like string format.

    Example:
        on(a,b) -> "(on a b)"
    """
    symbol = atom.predicate.name
    terms = " ".join(str(t) for t in atom.subterms)
    return f"({symbol} {terms})" if terms else f"({symbol})"


def get_state_static(problem) -> tuple[frozenset, frozenset]:
    """
    Generate frozensets of dynamic state facts and static facts
    using Tarski.

    Dynamic predicates are those that appear in action effects.
    Static predicates never change.

    Returns:
        tuple[frozenset, frozenset]
    """

    # --- Initial facts ---
    initial_facts = set(problem.init.as_atoms())

    # --- Predicates modified by actions ---
    dynamic_predicates = set()

    for action in problem.actions.values():

        # Add effects
        for effect in action.effects:
            atom = effect.atom
            dynamic_predicates.add(atom.predicate)

    # --- Split facts ---
    state_facts = set()
    static_facts = set()

    for fact in initial_facts:
        if fact.predicate in dynamic_predicates:
            state_facts.add(fact)
        else:
            static_facts.add(fact)

    # --- Convert to strings ---
    state_strings = {
        atom_to_string(fact)
        for fact in state_facts
    }

    static_strings = {
        atom_to_string(fact)
        for fact in static_facts
    }

    return frozenset(state_strings), frozenset(static_strings)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--domain",
        type=str,
        help="Path to domain.pddl"
    )

    parser.add_argument(
        "--instance",
        type=str,
        help="Path to problem instance"
    )

    parser.add_argument(
        "--base_path",
        type=str,
        help="Output directory"
    )

    args = parser.parse_args()

    # --- Parse with Tarski ---
    reader = PDDLReader()

    problem = reader.read_problem(
        domain=args.domain,
        instance=args.instance
    )

    # --- Extract state/static ---
    state, static = get_state_static(problem)

    # --- Write outputs ---
    with open(f"{args.base_path}/example-state.out", "w") as f:
        f.write(str(state))

    with open(f"{args.base_path}/example-static.out", "w") as f:
        f.write(str(static))