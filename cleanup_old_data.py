import logging
import pathlib
import sys

from twitter_utilities import sort_by_datetime


if __name__ == "__main__":
    # Set up logging
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        root.addHandler(sh)
        fh = logging.FileHandler(f"/Users/daniellefevre/PycharmProjects/tweet_analyzer/logs/download_tweets.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    data_folder = "/Users/daniellefevre/PycharmProjects/tweet_analyzer"

    data_path = pathlib.Path(data_folder)

    files = list(data_path.glob("*.json"))
    files.sort(key=sort_by_datetime)
    max_datetime = sort_by_datetime(files[-1])

    [pathlib.Path.unlink(file) for file in files
        if max_datetime.strftime("%Y%m%d%H%M%S") not in str(file)]
