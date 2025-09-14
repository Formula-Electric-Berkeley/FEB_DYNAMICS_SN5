import os

# Get the folder the script is in
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input files
input_files = {
    "Front": os.path.join(script_dir, "sample_geometry_front.TXT"), ## Takes two files 
    "Rear": os.path.join(script_dir, "sample_geometry_rear.TXT")
}

# Single combined output file
output_path = os.path.join(script_dir, "SN5_Global_Variables.txt")

# Function to make a variable name safe for SolidWorks
def make_safe_variable_name(label):
    label = label.strip().replace(" ", "_")
    label = ''.join(c for c in label if c.isalnum() or c == '_')
    if not label[0].isalpha():
        label = '_' + label
    return label

# Parse multiple input files and write SolidWorks global variables
def parse_and_write_solidworks_globals(input_files, output_file):
    coordinates = {}

    for prefix, input_file in input_files.items():
        with open(input_file, 'r') as f:
            for line in f:
                if 'X=' in line and 'Y=' in line and 'Z=' in line:
                    parts = line.split()
                    idx = parts[0]
                    x_val = float(parts[2])
                    y_val = float(parts[4])
                    z_val = float(parts[6])

                    # Get the label/description
                    desc_parts = parts[7:]
                    if desc_parts and len(desc_parts[-1]) == 1 and desc_parts[-1].isalpha():
                        desc_parts = desc_parts[:-1]
                    label = " ".join(desc_parts).strip()
                    if not label:
                        label = f"unnamed_point_{idx}"

                    # Prepend Front/Rear prefix and make safe
                    safe_label = make_safe_variable_name(f"{prefix}_{label}")
                    coordinates[safe_label] = {'x': x_val, 'y': y_val, 'z': z_val}

    # Write all variables to output file
    with open(output_file, 'w') as fout:
        for label in sorted(coordinates.keys()):
            vals = coordinates[label]
            fout.write(f"\"{label}_X\" = {vals['x']}mm\n")
            fout.write(f"\"{label}_Y\" = {vals['y']}mm\n")
            fout.write(f"\"{label}_Z\" = {vals['z']}mm\n")

try:
    parse_and_write_solidworks_globals(input_files, output_path)
    print("✅ Done! File created:", output_path)
except Exception as e:
    print("❌ Error occurred:", e)

input("\nPress Enter to close...")

##Practice changes to see if this will show up in GitHub

##Hopefully these show up on the practice branch.

#Alright lets hope this shows up in Vs Code

