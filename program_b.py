import subprocess
import statistics
import os

def program_b(path):
    program_a = subprocess.Popen(["python3", path], 
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True)

    try:
        # 1. Send the Hi command to Program A and verify the correct response.
        program_a.stdin.write("Hi\n")
        program_a.stdin.flush()
        hi_response = program_a.stdout.readline().strip()
        
        if hi_response == "Hi":
            print("Program A responded as expected.")
        else:
            print("Program A did not respond as expected.")
            return  # Exit if the response is not as expected.

        # 2. Retrieve 100 random numbers by sending the GetRandom command to Program A 100 times.
        random_numbers = []
        for _ in range(100):
            program_a.stdin.write("GetRandom\n")
            program_a.stdin.flush()
            random_number = program_a.stdout.readline().strip()

            if random_number.isdigit():  # Ensure the output is a valid integer
                random_numbers.append(int(random_number))
            else:
                print("Received an invalid number from Program A:", random_number)
                return  # Exit if invalid output is received

        # 3. Send the Shutdown command to Program A to terminate it gracefully.
        program_a.stdin.write("Shutdown\n")
        program_a.stdin.flush()

        program_a.wait()

        error_output = program_a.stderr.read().strip()
        if error_output:
            print("Error output from Program A:", error_output)
            return  # Exit if there are errors

        if program_a.returncode == 0:
            print("Program A shut down successfully.")
        else:
            print(f"Program A terminated with return code: {program_a.returncode}")
            return  # Exit on unexpected return code

        # 4. Sort the list of retrieved random numbers and print the sorted list to the console.
        random_numbers.sort()
        print("Sorted numbers: ", random_numbers)

        # 5. Calculate and print the median and average of the numbers.
        if random_numbers:
            num_median = statistics.median(random_numbers)
            num_avg = sum(random_numbers) / len(random_numbers)
            print("Median: ", num_median, ", Average: ", num_avg)
        else:
            print("No valid random numbers retrieved.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if program_a.poll() is None:  # Check if the process is still running
            program_a.terminate()  # Terminate if it is still active

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    program_a_path = os.path.join(current_directory, "program_a.py")
    program_b(program_a_path)
