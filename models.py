from openenv.core.env_server import Action, Observation, State

class CleanerAction(Action):
    action: str

class CleanerObservation(Observation):
    state: dict
    message: str = ""
    done: bool = False

class CleanerState(State):
    episode_id: str = ""
    step_count: int = 0
