import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Combine all csv files in a directory")
    parser.add_argument("input_dir", type=str, help="Input directory")
    parser.add_argument("output_file", type=str, help="Output file path")
    return parser.parse_args()


def combine_csv(input_dir: str, output_file: str):
    """
    Combine all csv files in the input_dir into a single csv file
    """
    with open(output_file, "w") as out_f:
        filenames = sorted(filter(lambda x: x.endswith(".csv"), os.listdir(input_dir)))
        headers = None
        for filename in filenames:
            with open(os.path.join(input_dir, filename), "r") as in_f:
                h, rows = in_f.read().split("\n", 1)
                if headers is None:
                    headers = h
                    out_f.write(h + "\n")
                elif headers != h:
                    print(f"Warning: headers mismatch in '{filename}', skipping...")
                    continue
                out_f.write(rows)


if __name__ == "__main__":
    args = parse_args()
    combine_csv(args.input_dir, args.output_file)
