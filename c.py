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
        blocks = list(schematic["Blocks"])  # force decode
        width = int(schematic["Width"])
        height = int(schematic["Height"])
        length = int(schematic["Length"])

        if len(blocks) == 0:
            print(f"{file_path} has empty 'Blocks'")
        else:
            print(f"{file_path} - Size: {width}x{height}x{length}, Blocks: {len(blocks)}")
            print(f"First 10 block IDs: {blocks[:10]}")

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
                    index = y * length * width + z * width + x  # Correct schematic layout
                    block_id = int(blocks[index])

                    # Optional: filter out air blocks (ID = 0)
                    # if block_id == 0:
                    #     continue

                    # Debug: print a few sample lines
                    if len(all_data) < 10:
                        print(f"{schematic_type},{x},{y},{z},{block_id}")

                    all_data.append([schematic_type, x, y, z, block_id])

    save_to_csv(all_data)
    print("Exported to ai_blocks.csv")

if __name__ == "__main__":
    main()
