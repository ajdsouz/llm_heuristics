from time import perf_counter
from dataclasses import dataclass

def timer(func):
    """
    A timer decorator to compute runtime of a function

    Args:
        func (_type_): A function whose runtime needs to be computed
    """
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        return result, (end - start)
    return wrapper


@dataclass
class HeuristicGenerationConfig:
    model_name: str
    domain: str
    instance1: str
    instance2: str
    temperature: float
    top_p: float
    generated_heuristic: str
    # runtime_dict: dict
    # TODO add reasoning, input and output token count. openai returns prompt and completion tokens
    heuristic_generation_runtime: float # should it be float?
    # TODO add model generation time and switch values
    input_token_count: int
    output_token_count: int

@dataclass
class PlanValidationConfig:
    temperature: float
    top_p: float
    prompt_instance1: str # path
    prompt_instance2: str # path
    evaluation_instance: str # path
    generated_heuristic: str # path / code what should be saved?
    val_runtime: float | str # how to set in case of timeout? 
    status: str


@dataclass
class DirectoryEvaluationConfig:
    model: str
    domain: str
    prompt_instance1: str
    prompt_instance2: str
    temperature: float
    top_p: float
    success: list[str]
    failure: list[str]
    timeout: list[str]
    no_solution: list[str]
