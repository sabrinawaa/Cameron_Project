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

def search_for_sig(directory, lower_bound_sig, upper_bound_sig, lower_bound_p, upper_bound_p):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".out"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    if "f1:" in line and "sig_x:" in line and "sig_y:" in line and "sig_xp:" in line and "sig_yp:" in line:
                        try:
                            # Extract all values from the line
                            parts = line.split(',')
                            f1 = float(parts[0].split(':')[1].strip())
                            f2 = float(parts[1].split(':')[1].strip())
                            f3 = float(parts[2].split(':')[1].strip())
                            f4 = float(parts[3].split(':')[1].strip().split('---')[0])
                            sig_x = float(parts[3].split('sig_x:')[1].strip().split(',')[0])
                            sig_y = float(parts[4].split('sig_y:')[1].strip())
                            sig_xp = float(parts[5].split('sig_xp:')[1].strip())
                            sig_yp = float(parts[6].split('sig_yp:')[1].strip())
                            
                            # Check if all sigma values are within bounds
                            if (lower_bound_sig <= sig_x <= upper_bound_sig and 
                                lower_bound_sig <= sig_y <= upper_bound_sig and
                                lower_bound_p <= sig_xp <= upper_bound_p and
                                lower_bound_p <= sig_yp <= upper_bound_p):
                                results.append({
                                    'filename': filename,
                                    'f_values': (f1, f2, f3, f4),
                                    'sigma_values': (sig_x, sig_y, sig_xp, sig_yp)
                                })
                        except (IndexError, ValueError) as e:
                            print(f"Error processing line in {filename}: {e}")
                            continue
    return results

def main():
    directory = "submit/scan_k1s_10m/out/"

    if not os.path.isdir(directory):
        print(f"The specified path '{directory}' is not a directory.")
        sys.exit(1)

    # Original functionality
    # print("Searching for files containing 'f1:'...")
    # files_with_f1 = search_files_in_directory(directory)

    # if files_with_f1:
    #     print("\nFiles containing 'f1:':")
    #     for filename in files_with_f1:
    #         print(filename)
    # else:
    #     print("No files containing 'f1:' found.")

    # New functionality
    print("\nSearching for files with all sigma values within range...")
    lower_bound_sig, upper_bound_sig = 0,20
    lower_bound_p,upper_bound_p = 0,100000000
    
    range_results = search_for_sig(directory, lower_bound_sig, upper_bound_sig, lower_bound_p, upper_bound_p)
    
    if range_results:
        print(f"\nFiles with all sigma values between {lower_bound_sig} and {upper_bound_sig} and angles between {lower_bound_p} and {upper_bound_p}:")
        for result in range_results:
            print(f"\nFile: {result['filename']}")
            print(f"f1: {result['f_values'][0]}, f2: {result['f_values'][1]}, f3: {result['f_values'][2]}, f4: {result['f_values'][3]}")
            print(f"sig_x: {result['sigma_values'][0]}, sig_y: {result['sigma_values'][1]}")
            print(f"sig_xp: {result['sigma_values'][2]}, sig_yp: {result['sigma_values'][3]}")
    else:
        print(f"\nNo files found with all sigma values between {lower_bound_sig} and {upper_bound_sig} and angles between {lower_bound_p} and {upper_bound_p}")

if __name__ == "__main__":
    main()