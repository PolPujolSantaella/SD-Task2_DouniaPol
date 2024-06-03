import subprocess

def run_tests(test_script):
    try:
        result = subprocess.run(["python", test_script], capture_output=True, text=True)
        print(f"Logs for {test_script}:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error executing {test_script}: {result.stderr}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing {test_script}: {e}")
        return False

def main():
    centralized_success = run_tests("eval/centralized_system_tests.py")
    decentralized_success = run_tests("eval/decentralized_system_tests.py")

    if centralized_success and decentralized_success:
        print("All tests passed successfully.")
    else:
        print("Some tests failed.")

if __name__ == "__main__":
    main()
