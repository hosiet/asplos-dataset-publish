#!/usr/bin/python3

# Process data collected by getopengldata-native
# and generate a standard data format.

import re
import pandas as pd
from pathlib import Path


DATA_ROW_PATTERN = r'^DEBUG: [0-9]+.[0-9]+: [0-9]+ [0-9]+ [0-9]+ [0-9]+; [0-9]+ [0-9]+ [0-9]+ [0-9]+; [0-9]+ [0-9]+ [0-9]+ [0-9]+;$'
BASE_DIR = Path('..') / 'misc_usenix_dataprocessing'


def is_valid_filetexts(input_textlines: str):
    '''Determine whether the data read is valid'''
    real_data_lines = input_textlines[:-1]
    metadata_line = input_textlines[-1]
    for data_line in real_data_lines:
        if not re.match(DATA_ROW_PATTERN, data_line):
            return False, ('data_line', data_line)
    return True, tuple()


class ExperimentResult():
    '''
    Stores experiment result in two parts:
    (1) Timestamp and 12 PC counter readings.
    (2) Timestamp and the key pressed.
    '''
    def __init__(self, data_file_path, data_file_textlines):
        self.df_data = pd.DataFrame()
        self.df_press = pd.DataFrame()
        self.filepath = str()
        self.init_record(data_file_path, data_file_textlines)
        return

    def init_record(self, data_file_path, data_file_textlines):
        self.filepath = data_file_path
        # Now, convert textlines into pandas DataFrame
        # Handle last line first
        data_lines = data_file_textlines[:-1]
        last_line = data_file_textlines[-1]
        last_line_list = last_line.split(' ')
        if last_line_list[-1] == '\n':
            del last_line_list[-1]
        key_press_times = len(last_line_list) // 2
        assert key_press_times * 2 == len(last_line_list)
        press_time_list = last_line_list[:key_press_times]
        press_key_list = last_line_list[key_press_times:]
        for i in range(key_press_times):
            tmp_row = {'timestamp': press_time_list[i], 'key': press_key_list[i]}
            tmp_df = pd.DataFrame(tmp_row, index=[0])
            self.df_press = pd.concat([self.df_press, tmp_df], axis=0, ignore_index=True)
        # Then, handle data lines
        tmp_list = list()
        for data_line in data_lines:
            tmp_raw_dataline = data_line.split(':')[2]
            tmp1, tmp2, tmp3, _ = tmp_raw_dataline.split(';')
            PC1, PC2, PC3, PC4 = tmp1.strip().split(' ')
            PC5, PC6, PC7, PC8 = tmp2.strip().split(' ')
            PC9, PC10, PC11, PC12 = tmp3.strip().split(' ')
            tmp_list.append({
                'timestamp': str(data_line.split(':')[1].strip()),
                'PC1': PC1, 'PC2': PC2, 'PC3': PC3, 'PC4': PC4,
                'PC5': PC5, 'PC6': PC6, 'PC7': PC7, 'PC8': PC9,
                'PC9': PC9, 'PC10': PC10, 'PC11': PC11, 'PC12': PC12,
                })
        tmp_data_df = pd.DataFrame(tmp_list)
        self.df_data = pd.concat([self.df_data, tmp_data_df], axis=0, ignore_index=True)
        return

    def save_as_csv(self, destdir):
        '''Save current dataset into CSV files.'''
        timestamp_str = self.filepath.name.split('output_')[1].split('.txt')[0]
        assert re.match(r'^[0-9]+$', timestamp_str)
        target_dir_path = destdir / timestamp_str
        target_dir_path.mkdir(exist_ok=True)
        data_csv_file_path = target_dir_path / '{}_data.csv'.format(timestamp_str)
        keys_csv_file_path = target_dir_path / '{}_keys.csv'.format(timestamp_str)
        self.df_data.to_csv(data_csv_file_path, sep=' ', index=False)
        self.df_press.to_csv(keys_csv_file_path, sep=' ', index=False)
        return


if __name__ == '__main__':
    print('Hello world!')
    # Find all files, using rglob()
    possible_data_files = [x for x in BASE_DIR.rglob(r'output_*.txt')]
    print('INFO: Candidate files No.: {}'.format(len(possible_data_files)))
    for data_file in possible_data_files:
        data_file_textlines = None
        with open(data_file, 'r') as f:
            data_file_textlines = f.readlines()
        if not data_file_textlines:
            raise Exception('data_file read failed!')
        validation_result = is_valid_filetexts(data_file_textlines)
        if validation_result[0] is False:
            print('WARN: file {} is not valid ({}), skipping ...'.format(
                data_file.name, str(validation_result[1])))
            continue
        # Now with valid text, try to record it
        curr_data_record = ExperimentResult(data_file, data_file_textlines)
        curr_data_record.save_as_csv(destdir=Path('.') / 'pc_counter_dataset')
        print('.', end='')
