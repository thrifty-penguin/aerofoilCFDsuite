import subprocess
import pandas as pd
import os

def run_xfoil(airfoil_file, output_file):
    # Create a temporary XFOIL input file
    input_filename = "xfoil_input.txt"
    with open(input_filename, 'w') as f:
        # Load the airfoil
        f.write(f"LOAD {airfoil_file}\n")
        f.write("PANE\n")  # Apply paneling to the airfoil

        # Set operation and Reynolds number
        f.write("OPER\n")  # Enter operation mode
        f.write("VISC\n")  # Enable viscous mode
        f.write("RE 500000\n")  # Set Reynolds number explicitly
        f.write("MACH 0.2\n")   # Set Mach number

        # Set angles of attack sweep
        f.write("ASEQ -5 15 1\n")  # Set angle of attack sweep from -5 to 15 degrees in steps of 1

        # Polar accumulation
        f.write("PACC\n")
        f.write(f"{output_file}\n\n")  # Specify polar output file
        f.write("PACC OFF\n")  # End polar accumulation

        # Exit XFOIL
        f.write("\nQUIT\n")

    # Run XFOIL with the input file
    try:
        with open(input_filename, 'r') as input_file:
            subprocess.run(["xfoil.exe"], stdin=input_file, shell=True, check=True)  # Use "xfoil.exe" if it's required
    except subprocess.CalledProcessError as e:
        print("XFOIL failed to run:", e)

    # Clean up input file
    os.remove(input_filename)

'''def parse_xfoil_output(output_file):
    # Check if output file exists to prevent FileNotFoundError
    if not os.path.isfile(output_file):
        print(f"Error: Output file {output_file} was not created. XFOIL may have failed.")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

    # Read the XFOIL polar file and parse it into a DataFrame
    columns = ["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"]
    data = []
    with open(output_file, 'r') as f:
        lines = f.readlines()
        for line in lines[12:]:  # Skip header lines
            values = line.split()
            if len(values) == 7:  # Ensure all fields are present
                data.append([float(v) for v in values])

    # Convert to pandas DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df'''

# Define airfoil and output file
airfoil_file = "NASA63A108.dat"  # Path to the airfoil file
output_file = "polar_output.txt"

# Run XFOIL analysis
run_xfoil(airfoil_file, output_file)

# Parse and save output if it exists
df = parse_xfoil_output(output_file)
if not df.empty:
    df.to_csv("xfoil_results.csv", index=False)
    print("Data saved to xfoil_results.csv")
else:
    print("No data saved due to XFOIL output error.")
