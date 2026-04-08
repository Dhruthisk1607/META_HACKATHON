from environment import CSVCleanerEnvironment
from models import CleanerAction

def run():
    env = CSVCleanerEnvironment()

    # Reset environment
    obs = env.reset(file_path="messy_data.csv")
    print("Initial Observation:", obs)

    done = False

    # Example actions (you can change)
    actions = [
        "fill nulls",
        "remove duplicates"
    ]

    for act in actions:
        if done:
            break

        action = CleanerAction(action=act)
        obs = env.step(action)

        print("\nAction:", act)
        print("Observation:", obs)

        done = obs.done

    return obs


if __name__ == "__main__":
    run()
