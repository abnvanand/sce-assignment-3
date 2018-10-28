import os
# TODO: RCA?? find why IDE gives an error but the script runs
from src.bash import run

if __name__ == "__main__":
    while True:

        print(os.getcwd(), "$", end=' ')
        try:
            command, *args = input().strip().split()
        except ValueError:
            # Gives ValueError: not enough values to unpack (expected at least 1, got 0)
            # when enter key is pressed without typing anything
            continue

        if command == "exit":
            break

        try:
            run(command, *args)
        except Exception as e:
            print(e)
