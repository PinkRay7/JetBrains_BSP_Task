import random

def program_a():
    while True:
        try:
            command = input().strip()
            if command == "Hi":
                print("Hi")
            elif command == "GetRandom":
                print(random.randint(1, 100))
            elif command == "Shutdown":
                print("Shutting down...")
                break
        except EOFError:
            break

if __name__ == "__main__":
    program_a()
