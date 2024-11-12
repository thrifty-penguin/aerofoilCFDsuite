import subprocess
import pandas as pd
import os

def run_xfoil(aerofoil, output_file):
    input_filename = "xfoil_input.txt"
    with open(input_filename, 'w') as f:
        f.write(f"LOAD {aerofoil}\n")
        f.write("PANE\n")
        f.write("OPER\n")
        f.write("Iter\n")
        f.write('100\n')
        f.write("VISC\n")
        f.write("500000\n")
        f.write("MACH\n")
        f.write('0.2\n')
        f.write('PACC\n')
        f.write(f"{output_file}\n")
        f.write("\n")
        f.write("ASEQ -5 15 1\n") 
        f.write("PACC OFF\n")
        f.write("\nQUIT\n")
    try:
        with open(input_filename, 'r') as input_file:
            subprocess.run([r"C:\Program Files\XFOIL\xfoil.exe"], stdin=input_file, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("XFOIL failed to run:", e)
    os.remove(input_filename)

aerofoil = 'Airfoil_Coordinates/a18sm.dat'
quest=aerofoil.lstrip('Airfoil_Coordinate')
tion=quest.rstrip('.dat')
output_file = f"{tion}.txt"
run_xfoil(aerofoil, output_file)