'''Group the data'''
import pandas as pd
import os


def find_all_csv(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.csv') and f != 'merged.csv']

def load_csvs(paths):
    result = []
    for path in paths:
        result.append(pd.read_csv(path))
    return result

def concat_csv(path):
    csv_files = find_all_csv(path)
    result = load_csvs(csv_files)
    merged = pd.concat(result)

    # reset index
    merged.index = range(len(merged))
    return merged

if __name__ == '__main__':
    merged = concat_csv('./data/')
    merged.to_csv('./data/merged.csv', index=False)