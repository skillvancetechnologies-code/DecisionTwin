# dt_genai/history_manager.py

import json
import os

HISTORY_FILE = "dt_genai/data/history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(HISTORY_FILE, "r") as file:

            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except json.JSONDecodeError:

        print("\nWarning: Corrupted history file.\n")
        return []

    except Exception as e:

        print(f"\nError loading history: {e}\n")
        return []


def save_analysis(record):

    history = load_history()

    history.append(record)

    try:

        with open(HISTORY_FILE, "w") as file:

            json.dump(history, file, indent=4)

    except Exception as e:

        print(f"\nError saving history: {e}\n")


def view_history():

    history = load_history()

    if not history:

        print("\nNo analysis history found.\n")
        return

    print("\n========== ANALYSIS HISTORY ==========\n")

    for index, item in enumerate(history, start=1):

        print(f"{index}. Scenario: {item.get('query', 'N/A')}")
        print(f"   Category: {item.get('category', 'N/A')}")
        print(f"   Decision Type: {item.get('decision_type', 'N/A')}")
        print(f"   Risk: {item.get('risk', 'N/A')}")
        print(f"   Probability: {item.get('probability', 'N/A')}")
        print(f"   Confidence: {item.get('confidence', 'N/A')}")
        print(f"   Recommendation: {item.get('recommendation', 'N/A')}")
        print()

    print("\n")