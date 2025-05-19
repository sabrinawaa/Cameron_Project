import os
import sys

def search_files_in_directory(directory):
    files_with_f1 = []
    for filename in os.listdir(directory):
        if filename.endswith(".out"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                if "f1:" in content:
                    files_with_f1.append(filename)
                    for line in content.splitlines():
                        if "f1:" in line:
                            print(line)
    return files_with_f1

def search_for_sig(directory, lower_bound, upper_bound):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".out"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    if "f1:" in line and "sig_x:" in line and "sig_y:" in line:
                        try:
                            # Extract all values from the line
                            parts = line.split(',')
                            f1 = float(parts[0].split(':')[1].strip())
                            f2 = float(parts[1].split(':')[1].strip())
                            f3 = float(parts[2].split(':')[1].strip())
                            f4 = float(parts[3].split(':')[1].strip().split('---')[0])
                            sig_x = float(parts[3].split('sig_x:')[1].strip().split(',')[0])
                            sig_y = float(parts[4].split('sig_y:')[1].strip())
                            
                            # Check if both sig_x and sig_y are within bounds
                            if (lower_bound <= sig_x <= upper_bound and 
                                lower_bound <= sig_y <= upper_bound):
                                results.append({
                                    'filename': filename,
                                    'f1': f1,
                                    'f2': f2,
                                    'f3': f3,
                                    'f4': f4,
                                    'sig_x': sig_x,
                                    'sig_y': sig_y
                                })
                        except (IndexError, ValueError) as e:
                            print(f"Error processing line in {filename}: {e}")
                            continue
    return results

def main():
    directory = "submit/scan_k1s/out/"

    if not os.path.isdir(directory):
        print(f"The specified path '{directory}' is not a directory.")
        sys.exit(1)

    # # Original functionality
    # print("Searching for files containing 'f1:'...")
    # files_with_f1 = search_files_in_directory(directory)

    # if files_with_f1:
    #     print("\nFiles containing 'f1:':")
    #     for filename in files_with_f1:
    #         print(filename)
    # else:
    #     print("No files containing 'f1:' found.")

    # New functionality
    print("\nSearching for files with sig_x and sig_y within range...")
    lower_bound = 2
    upper_bound = 4
    
    range_results = search_for_sig(directory, lower_bound, upper_bound)
    
    if range_results:
        print(f"\nFiles with both sig_x and sig_y between {lower_bound} and {upper_bound}:")
        for result in range_results:
            print(f"\nFile: {result['filename']}")
            print(f"f1: {result['f1']}, f2: {result['f2']}, f3: {result['f3']}, f4: {result['f4']}")
            print(f"sig_x: {result['sig_x']}, sig_y: {result['sig_y']}")
    else:
        print(f"\nNo files found with both sig_x and sig_y between {lower_bound} and {upper_bound}")

if __name__ == "__main__":
    main()