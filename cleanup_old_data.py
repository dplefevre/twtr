import datetime
import pathlib
import re


def sort_by_datetime(file_name):
    name = pathlib.PurePath(file_name).stem
    dt_string = name.split("_")[-1]
    dt = datetime.datetime.strptime(dt_string, "%Y%m%d%H%M%S")
    return dt


data_folder = "/Users/daniellefevre/PycharmProjects/tweet_analyzer"

data_path = pathlib.Path(data_folder)

files = list(data_path.glob("*.json"))
print(files)
files.sort(key=sort_by_datetime)
max_datetime = sort_by_datetime(files[-1])

[pathlib.Path.unlink(file) for file in files
    if max_datetime.strftime("%Y%m%d%H%M%S") not in str(file)]
