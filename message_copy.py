import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
import time


def divide_number_into_parts(total, parts):

    # Calculate base value and remainder
    base = total // parts
    remainder = total % parts

    # Create the result array
    result = [base] * parts

    # Distribute the remainder
    for i in range(remainder):
        result[i] += 1

    # Remove zero values
    result = [x for x in result if x != 0]
    return result


def generate_starts(arr):
    result = []
    cumulative_sum = 0
    for element in arr:
        result.append(cumulative_sum)
        cumulative_sum += element
    return result


def create_copies(source_path, dest_folder, num_copies, start_num=0):
    if not os.path.isfile(source_path):
        raise ValueError("Source path must be a regular file")
    if not os.path.isdir(dest_folder):
        raise ValueError("Destination folder must be a directory")
    if num_copies <= 0:
        raise ValueError("Number of copies must be positive")

    dest_files = []
    base_name = os.path.basename(source_path)
    name, ext = os.path.splitext(base_name)

    try:
        # Read source once
        with open(source_path, 'r') as src:

            # Read content and assign to const
            source_content = src.read()

            # Write destination files relative to current thread
            for i in range(start_num, start_num+num_copies):
                write_content = source_content.replace("$MSGID$", str(uuid.uuid4()))
                dest_path = os.path.join(dest_folder, f"{name}_{i}{ext}")

                with open(dest_path, 'w') as f:
                    f.write(write_content)

    except Exception:
        # Cleanup on error (skip for speed; partial files may remain)
        for f in dest_files:
            try:
                f.close()
            except:
                pass
        raise
    finally:
        for f in dest_files:
            try:
                f.close()
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python message_copy.py <source_file> <dest_folder> <num_copies>")
        sys.exit(1)
    
    source = sys.argv[1]
    dest = sys.argv[2]
    try:
        num = int(sys.argv[3])
    except ValueError:
        print("Error: Number of copies must be an integer")
        sys.exit(1)

    # Start timing
    start_time = time.time()

    # Get the number of CPU cores
    num_cores = os.cpu_count()

    # Define the optimal number of threads (can be adjusted based on workload)
    optimal_threads = num_cores * 2

    num_parts = divide_number_into_parts(num, optimal_threads)
    num_starts = generate_starts(num_parts)
    print(f"Number of CPU cores: {num_cores}")
    print(f"Optimal number of threads: {optimal_threads}")


    with ThreadPoolExecutor(max_workers=optimal_threads) as executor:
        tasks = [executor.submit(create_copies(source, dest, num_parts[task_id], num_starts[task_id])) for task_id in range(len(num_parts))]

    # End timing
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.6f} seconds".format(execution_time))