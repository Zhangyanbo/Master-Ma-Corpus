from datetime import datetime, timedelta
import json
import os
import re
import pandas as pd


def time_to_seconds(time_str):
    dt = datetime.strptime(time_str, '%H:%M:%S')
    td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    return int(td.total_seconds())

def preprocess_srt(srt_string):
    srt_string = srt_string.replace(' ', '').replace('\n\n', '\n')
    return srt_string

def split_srt(srt_string):
    pattern = r'^\d+\n'
    subtitles = re.split(pattern, srt_string, flags=re.MULTILINE)[1:]
    return subtitles

def parse_line(line):
    parts = line.split('\n')
    start_time = parts[0].split('-->')[0].split(',')[0]
    content = parts[1]
    return [time_to_seconds(start_time), content]

def parse_string(srt_string, comments=''):
    subtitles = split_srt(preprocess_srt(srt_string))
    result = []
    for subtitle in subtitles:
        result.append(parse_line(subtitle) + [comments])
    return result

def parse_file(file_path, meta_info='./source/source.json'):
    with open(meta_info, 'r') as f:
        meta = json.load(f)
    comments = meta[os.path.basename(file_path)]

    with open(file_path, 'r') as f:
        srt_string = f.read()
    return parse_string(srt_string, comments)

def find_srt_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.srt')]

if __name__ == '__main__':
    files = find_srt_files('./source')
    for file_path in files:
        parsed = parse_file(file_path)
        # save to csv use Pandas
        df = pd.DataFrame(parsed, columns=['time', 'content', 'comments'])
        file_name = os.path.basename(file_path).split('.')[0]
        df.to_csv('./data/{}.csv'.format(file_name), index=False)