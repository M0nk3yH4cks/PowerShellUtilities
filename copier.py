import os
import sys
import shutil
from pathlib import Path
import mmap

def create_copies_optimized(source_path, dest_folder, num_copies):
    """
    Create multiple copies of a file with maximum performance.
    Uses memory mapping for large files and optimized copying for small files.
    """
    source_path = Path(source_path)
    dest_folder = Path(dest_folder)
    
    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    if not dest_folder.is_dir():
        raise NotADirectoryError(f"Destination folder not found: {dest_folder}")
    
    if num_copies <= 0:
        raise ValueError("Number of copies must be positive")
    
    file_size = source_path.stat().st_size
    
    # Use different strategies based on file size
    if file_size > 1024 * 1024:  # Files larger than 1MB
        _copy_large_file(source_path, dest_folder, num_copies)
    else:  # Small files - use shutil.copy2 for maximum efficiency
        _copy_small_files(source_path, dest_folder, num_copies)

def _copy_large_file(source_path, dest_folder, num_copies):
    """Handle large files using memory mapping for optimal performance"""
    source_name = source_path.name
    name, ext = os.path.splitext(source_name)
    
    # Open source file with memory mapping
    with open(source_path, 'rb') as src_file:
        with mmap.mmap(src_file.fileno(), 0, access=mmap.ACCESS_READ) as src_map:
            # Create all destination files concurrently
            dest_files = []
            dest_paths = []
            
            try:
                # Pre-create all destination files
                for i in range(num_copies):
                    dest_path = dest_folder / f"{name}_copy{i}{ext}"
                    dest_paths.append(dest_path)
                    dest_file = open(dest_path, 'wb')
                    dest_files.append(dest_file)
                
                # Write in chunks for memory efficiency
                chunk_size = 4 * 1024 * 1024  # 4MB chunks
                for i in range(0, len(src_map), chunk_size):
                    chunk = src_map[i:i + chunk_size]
                    for dest_file in dest_files:
                        dest_file.write(chunk)
                
            finally:
                # Close all destination files
                for dest_file in dest_files:
                    try:
                        dest_file.close()
                    except:
                        pass

def _copy_small_files(source_path, dest_folder, num_copies):
    """Handle small files using optimized shutil operations"""
    source_name = source_path.name
    name, ext = os.path.splitext(source_name)
    
    # For small files, shutil.copy2 is highly optimized
    for i in range(num_copies):
        dest_path = dest_folder / f"{name}_copy{i}{ext}"
        shutil.copy2(source_path, dest_path)

def create_copies_ultrafast(source_path, dest_folder, num_copies):
    """
    Ultra-fast method using os.sendfile (Linux) or optimized copying
    """
    source_path = Path(source_path)
    dest_folder = Path(dest_folder)
    
    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    if not dest_folder.is_dir():
        raise NotADirectoryError(f"Destination folder not found: {dest_folder}")
    
    if num_copies <= 0:
        raise ValueError("Number of copies must be positive")
    
    source_name = source_path.name
    name, ext = os.path.splitext(source_name)
    
    # Try to use sendfile for maximum performance on Linux
    if hasattr(os, 'sendfile') and sys.platform.startswith('linux'):
        _copy_with_sendfile(source_path, dest_folder, num_copies)
    else:
        # Fallback to optimized method
        _copy_parallel(source_path, dest_folder, num_copies)

def _copy_with_sendfile(source_path, dest_folder, num_copies):
    """Use os.sendfile for zero-copy operation (Linux only)"""
    source_name = source_path.name
    name, ext = os.path.splitext(source_name)
    
    with open(source_path, 'rb') as src_fd:
        src_fileno = src_fd.fileno()
        file_size = os.fstat(src_fileno).st_size
        
        dest_files = []
        try:
            # Open all destination files
            for i in range(num_copies):
                dest_path = dest_folder / f"{name}_copy{i}{ext}"
                dest_fd = open(dest_path, 'wb')
                dest_files.append((dest_fd, dest_fd.fileno()))
            
            # Use sendfile for zero-copy operation
            offset = 0
            chunk_size = 16 * 1024 * 1024  # 16MB chunks
            
            while offset < file_size:
                bytes_to_copy = min(chunk_size, file_size - offset)
                for _, dest_fileno in dest_files:
                    os.sendfile(dest_fileno, src_fileno, offset, bytes_to_copy)
                offset += bytes_to_copy
                
        finally:
            for dest_fd, _ in dest_files:
                try:
                    dest_fd.close()
                except:
                    pass

def _copy_parallel(source_path, dest_folder, num_copies):
    """Parallel copy using chunked reading"""
    source_name = source_path.name
    name, ext = os.path.splitext(source_name)
    file_size = source_path.stat().st_size
    
    # Determine optimal chunk size based on file size
    if file_size > 100 * 1024 * 1024:  # > 100MB
        chunk_size = 8 * 1024 * 1024  # 8MB
    elif file_size > 10 * 1024 * 1024:  # > 10MB
        chunk_size = 4 * 1024 * 1024   # 4MB
    else:
        chunk_size = 1024 * 1024       # 1MB
    
    with open(source_path, 'rb') as src_file:
        dest_files = []
        try:
            # Pre-open all destination files
            for i in range(num_copies):
                dest_path = dest_folder / f"{name}_copy{i}{ext}"
                dest_files.append(open(dest_path, 'wb'))
            
            # Copy in chunks
            while True:
                chunk = src_file.read(chunk_size)
                if not chunk:
                    break
                for dest_file in dest_files:
                    dest_file.write(chunk)
                    
        finally:
            for dest_file in dest_files:
                try:
                    dest_file.close()
                except:
                    pass

def main():
    if len(sys.argv) != 4:
        print("Usage: python fast_copy.py <source_file> <dest_folder> <num_copies>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    dest_folder = sys.argv[2]
    
    try:
        num_copies = int(sys.argv[3])
    except ValueError:
        print("Error: Number of copies must be an integer")
        sys.exit(1)
    
    try:
        # Use the ultra-fast method (will automatically fall back if needed)
        create_copies_ultrafast(source_file, dest_folder, num_copies)
        print(f"Successfully created {num_copies} copies of {source_file} in {dest_folder}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()