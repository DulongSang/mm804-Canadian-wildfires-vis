import argparse
import datetime
import os
from urllib.error import HTTPError
from urllib.request import urlopen

CWFIS_DOWNLOAD_HOTSPOTS_BASE_URL = "https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots"

def parse_args():
    parser = argparse.ArgumentParser(description="Download CWFIS hotspots data")
    parser.add_argument("from_date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("to_date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("output_dir", type=str, help="Output directory")
    return parser.parse_args()


def download_hotspots(from_date: datetime.date, to_date: datetime.date, output_dir: str):
    """
    example usage:
    download_hotspots(datetime.date(2024, 1, 1), datetime.date(2024, 2, 1), "hotspots")
    """

    cur_date = from_date

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # TODO: multithreading
    while cur_date <= to_date:
        filename = f"{cur_date.strftime('%Y%m%d')}.csv"

        try:
            content = urlopen(f"{CWFIS_DOWNLOAD_HOTSPOTS_BASE_URL}/{filename}").read().decode("utf-8")
        except HTTPError as e:
            print(f"Failed to download '{filename}': {e}")
            continue

        # handle extra spaces in the csv headers
        header, rows = content.split("\n", 1)
        header = ",".join(header.split(', '))
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(header + "\n")
            f.write(rows)
            print(f"Downloaded '{filename}'")
        
        cur_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    args = parse_args()
    from_date = datetime.datetime.strptime(args.from_date, "%Y-%m-%d").date()
    to_date = datetime.datetime.strptime(args.to_date, "%Y-%m-%d").date()

    download_hotspots(from_date, to_date, args.output_dir)
