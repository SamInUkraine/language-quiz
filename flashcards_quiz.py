import csv
import json
import random
import os


def load_dataset():
    filename = input("Enter dataset filename or URL: ").strip()

    if filename.startswith("http"):
        import requests
        print("Downloading dataset...")
        response = requests.get(filename)
        if filename.endswith(".json"):
            data = json.loads(response.text)
        elif filename.endswith(".csv"):
            lines = response.text.splitlines()
            reader = csv.reader(lines)
            data = list(reader)
        else:
            print("Unsupported file type from URL.")
            return []
    else:
        if not os.path.exists(filename):
            print("File not found!")
            return []
        if filename.endswith(".json"):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif filename.endswith(".csv"):
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)
        else:
            print("Unsupported file type. Please use .json or .csv files.")
            return []

    if isinstance(data, dict):
        return [(k, v) for k, v in data.items()]
    elif isinstance(data, list):
        if len(data) > 0 and all(isinstance(x, str) for x in data[0]) is False:
            return data
        return [(row[0], row[1]) for row in data if len(row) >= 2]
    else:
        return []

def quiz_game(words):
    """Runs the flashcard quiz."""
    print("\n=== Flashcard Quiz ===")
    score = 0
    random.shuffle(words)

    for term, translation in words:
        answer = input(f"What is the translation of '{term}'? ").strip()

        if not answer:
            print("You didn't provide an answer. Skipping...")
            continue
        if translation.endswith("?") or translation.endswith("!") or translation.endswith(".") or translation.endswith(","):
            if answer.endswith("?") or answer.endswith("!") or answer.endswith(".") or answer.endswith(","):
                answer = answer[:-1]
                translation = translation[:-1]
        if translation.startswith("¿") or translation.startswith("¡"):
            if answer.startswith("¿",) or answer.startswith("¡"):
                answer = answer[1:]
                translation = translation[1:]
        if answer.lower() == translation.lower():
                print("✅ Correct!")
                score += 1
        else:
                print(f"❌ Wrong. Correct answer: {translation}")
        print(f"\nYour score: {score}/{len(words)}")

if __name__ == "__main__":
    words = load_dataset()
    if not words:
        print("No words loaded. Exiting.")
    else:
        quiz_game(words)
