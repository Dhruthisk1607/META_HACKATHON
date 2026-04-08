import uuid
import uvicorn
from openenv.core.env_server import Environment, create_fastapi_app
from models import CleanerAction, CleanerObservation, CleanerState
from cleaner import CSVDataCleanerAgent


class CSVCleanerEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.cleaner = None
        self.episode_id = ""
        self.step_count = 0

    def reset(self, **kwargs) -> CleanerObservation:
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0

        file_path = kwargs.get("file_path", "messy_data.csv")
        self.cleaner = CSVDataCleanerAgent(file_path)

        state_data = self.cleaner.get_state()

        safe_data = {
            "rows": int(state_data.get("rows", 0)),
            "null_values": {k: int(v) for k, v in state_data.get("null_values", {}).items()},
            "duplicates": int(state_data.get("duplicates", 0))
        }

        return CleanerObservation(
            observation={
                "status": "ready",
                "data": safe_data
            },
            done=False
        )

    def step(self, action: CleanerAction) -> CleanerObservation:
        self.step_count += 1

        try:
            prev_state = self.cleaner.get_state()
            prev_nulls = sum(prev_state.get("null_values", {}).values() or [0])
            prev_dups = prev_state.get("duplicates", 0)

            self.cleaner.take_action(action.action)
            current_state = self.cleaner.get_state()

            current_nulls = sum(current_state.get("null_values", {}).values() or [0])
            current_dups = current_state.get("duplicates", 0)

            improvement = (prev_nulls - current_nulls) + (prev_dups - current_dups)

            if current_nulls == 0 and current_dups == 0:
                reward = 10.0
            elif improvement > 0:
                reward = improvement * 2.5
            else:
                reward = -0.8

            if self.step_count > 20:
                reward -= 1.5

            done = self.cleaner.is_clean() or self.step_count >= 30

            return CleanerObservation(
                observation={
                    "status": "updated",
                    "data": current_state
                },
                message=f"Action: {action.action} | Reward: {reward:.2f}",
                done=done
            )

        except Exception as e:
            return CleanerObservation(
                observation={
                    "status": "error",
                    "data": {}
                },
                message=f"Error: {str(e)}",
                done=True
            )

    @property
    def state(self) -> CleanerState:
        return CleanerState(
            episode_id=self.episode_id,
            step_count=self.step_count
        )



env = CSVCleanerEnvironment()

app = create_fastapi_app(
    env,
    CleanerAction,
    CleanerObservation
)


if __name__ == "__main__":
    print("CSV Data Cleaner Environment is running at http://127.0.0.1:8000")
    print("Open your browser → http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
