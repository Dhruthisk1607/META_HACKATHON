import uuid
import os
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

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        self.cleaner = CSVDataCleanerAgent(file_path)
        
        return CleanerObservation(
            state=self.cleaner.get_state(),
            message="Episode started. Send cleaning actions.",
            done=False
        )

    def step(self, action: CleanerAction) -> CleanerObservation:
        if not self.cleaner:
            return CleanerObservation(
                state={},
                message="Error: Call reset first.",
                done=True
            )

        self.step_count += 1
        
        try:
            self.cleaner.take_action(action.action)
            current_state = self.cleaner.get_state()
            
            done = self.cleaner.is_clean() or self.step_count >= 25
            
            return CleanerObservation(
                state=current_state,
                message=f"Executed: {action.action}",
                done=done
            )
        except Exception as e:
            return CleanerObservation(
                state=self.cleaner.get_state() if self.cleaner else {},
                message=f"Error: {str(e)}",
                done=True
            )

    @property
    def state(self) -> CleanerState:
        return CleanerState(
            episode_id=self.episode_id,
            step_count=self.step_count
        )


if __name__ == "__main__":
    app = create_fastapi_app(
        env=CSVCleanerEnvironment,  
        action_cls=CleanerAction,
        observation_cls=CleanerObservation
    )

    print(" Running at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
