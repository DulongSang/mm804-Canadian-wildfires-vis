import os

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
