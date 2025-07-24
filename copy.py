import os
import sys

def create_copies(source_path, dest_folder, num_copies):
    if not os.path.isfile(source_path):
        raise ValueError("Source path must be a regular file")
    if not os.path.isdir(dest_folder):
        raise ValueError("Destination folder must be a directory")
    if num_copies <= 0:
        raise ValueError("Number of copies must be positive")

    source_size = os.path.getsize(source_path)
    chunk_size = 1024 * 1024  # 1MB buffer
    dest_files = []
    dest_paths = []
    base_name = os.path.basename(source_path)
    name, ext = os.path.splitext(base_name)

    try:
        # Pre-allocate and open destination files
        for i in range(num_copies):
            dest_path = os.path.join(dest_folder, f"{name}_copy{i}{ext}")
            with open(dest_path, 'wb') as f:
                f.truncate(source_size)  # Pre-allocate space
            dest_files.append(open(dest_path, 'r+b', buffering=0))
            dest_paths.append(dest_path)

        # Read source once, write chunks to all destinations
        with open(source_path, 'rb', buffering=chunk_size) as src:
            while (chunk := src.read(chunk_size)):
                for dest in dest_files:
                    os.write(dest.fileno(), chunk)
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
        print("Usage: python fast_copy.py <source_file> <dest_folder> <num_copies>")
        sys.exit(1)
    
    source = sys.argv[1]
    dest = sys.argv[2]
    try:
        num = int(sys.argv[3])
    except ValueError:
        print("Error: Number of copies must be an integer")
        sys.exit(1)
    
    create_copies(source, dest, num)