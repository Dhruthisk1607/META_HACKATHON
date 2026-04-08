from environment import app
from cleaner import CSVDataCleanerAgent

def main():
    agent = CSVDataCleanerAgent("messy_data.csv")

    while True:
        print("\nCurrent State:")
        state = agent.get_state()
        print(state)

        if agent.is_clean():
            print("\nData is clean!")
            break

        action = input("\nEnter action (e.g., fill nulls, remove duplicates, strip column Name): ")
        agent.take_action(action)

    agent.save("cleaned_data.csv")
    print("\nCleaned data saved as cleaned_data.csv")

if __name__ == "__main__":
    main()
