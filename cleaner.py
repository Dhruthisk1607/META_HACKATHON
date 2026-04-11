print(" FILE IS RUNNING")

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
        print("RESET CALLED")

        self.episode_id = str(uuid.uuid4())
        self.step_count = 0

        try:
            file_path = kwargs.get("file_path", "messy_data.csv")
            self.cleaner = CSVDataCleanerAgent(file_path)

            state_data = self.cleaner.get_state()

            return CleanerObservation(
                observation={
                    "status": "ready",
                    "data": state_data
                },
                done=False
            )

        except Exception as e:
            print(" RESET ERROR:", e)
            return CleanerObservation(
                observation={"status": "error", "data": {}},
                message=str(e),
                done=True
            )

    def step(self, action: CleanerAction) -> CleanerObservation:
        print(" STEP CALLED:", action.action)

        try:
            self.step_count += 1

           
            self.cleaner.take_action(action.action)

            state = self.cleaner.get_state()
            done = self.cleaner.is_clean() or self.step_count >= 30

            return CleanerObservation(
                observation={
                    "status": "updated",
                    "data": state
                },
                message=f"Action: {action.action}",
                done=done
            )

        except Exception as e:
            print("❌ STEP ERROR:", e)
            return CleanerObservation(
                observation={"status": "error", "data": {}},
                message=str(e),
                done=True
            )

    @property
    def state(self) -> CleanerState:
        return CleanerState(
            episode_id=self.episode_id,
            step_count=self.step_count
        )



def create_env():
    return CSVCleanerEnvironment()



app = create_fastapi_app(
    create_env,
    CleanerAction,
    CleanerObservation
)



if __name__ == "__main__":
    print("\n STARTING SERVER...")
    print(" Open: http://127.0.0.1:8000/docs\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
