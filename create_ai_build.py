import os
import csv
from nbtlib import load

def get_schematic_files(root_dir="data"):
    schematic_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".schematic"):
                full_path = os.path.join(dirpath, file)
                schematic_type = dirpath.replace(root_dir, "").strip(os.sep).replace(os.sep, "_")
                schematic_type = schematic_type if schematic_type else "root"
                schematic_files.append((schematic_type, full_path))
    return schematic_files

def parse_schematic(file_path):
    try:
        schematic = load(file_path)
        blocks = schematic.root["Blocks"]
        width = schematic.root["Width"]
        height = schematic.root["Height"]
        length = schematic.root["Length"]
        return blocks, width, height, length
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return [], 0, 0, 0

def save_to_csv(data, output_file="ai_blocks.csv"):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["type", "x", "y", "z", "block"])
        for row in data:
            writer.writerow(row)

def main():
    all_data = []
    schematic_files = get_schematic_files()

    for schematic_type, file_path in schematic_files:
        blocks, width, height, length = parse_schematic(file_path)
        if not blocks:
            continue
        for y in range(height):
            for z in range(length):
                for x in range(width):
                    index = y * width * length + z * width + x
                    block_id = blocks[index]
                    all_data.append([schematic_type, x, y, z, block_id])

    save_to_csv(all_data)
    print("Exported to ai_blocks.csv")

if __name__ == "__main__":
    main()
