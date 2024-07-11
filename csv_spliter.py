import os

import numpy as np
import pandas as pd

ROOT_PATH = r"V:\wd\ZJUT\release\CDEHP\indoor"


def split_data(path: str):
    csv_file = os.listdir(path)[0]
    data = np.array(pd.read_csv(os.path.join(path, csv_file), header=None))
    index_x = np.digitize(data[:, -1], np.arange(0, data[-1][-1], 8333)) - 1
    for x in set(index_x):
        data_tmp = data[index_x == x]
        np.save(os.path.join(path, str(x).rjust(6, "0")), data_tmp)


def main():
    for set_name in os.listdir(ROOT_PATH):
        set_path = os.path.join(ROOT_PATH, set_name)
        for video_name in os.listdir(set_path):
            csv_path = os.path.join(set_path, video_name, "event_point_cloud")
            split_data(csv_path)


if __name__ == '__main__':
    main()
