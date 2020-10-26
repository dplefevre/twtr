import configparser
import logging
import pathlib
import sys

from twitter_utilities import sort_by_datetime


if __name__ == "__main__":
    # Read config file
    config = configparser.ConfigParser()
    config.read("/Users/daniellefevre/PycharmProjects/tweet_analyzer/configuration.ini")
    configs = config["configs"]
    # Set up logging
    log_dir = configs["log_dir"]
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        root.addHandler(sh)
        fh = logging.FileHandler(f"{log_dir}/cleanup_old_data.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    data_dir = configs["data_dir"]

    data_path = pathlib.Path(data_dir)

    files = list(data_path.glob("*.json"))
    files.sort(key=sort_by_datetime)
    max_datetime = sort_by_datetime(files[-1])

    [pathlib.Path.unlink(file) for file in files
        if max_datetime.strftime("%Y%m%d%H%M%S") not in str(file)]
