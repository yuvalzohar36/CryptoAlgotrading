import pandas as pd
import os


def sum_results(folder_path):
    files = []
    result_df = pd.DataFrame(columns=["Coin", "Indicator", "Credit"])
    for filename in os.listdir(folder_path):
        f = os.path.join(folder_path, filename)
        if os.path.isfile(f) and f.endswith('.csv'):
            files.append(f)
    for file in files:
        data = pd.read_csv(file)
        result_df = pd.concat([result_df, data], axis=0)
    res = result_df.groupby(by=['Coin', "Indicator"])["Credit"].sum()
    for i in range(len(res)):
        res[i] /= len(files)
    delete_files_in_directory(folder_path)
    return res


def delete_files_in_directory(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            # construct full file path
            file = os.path.join(directory_path, file_name)
            if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)

