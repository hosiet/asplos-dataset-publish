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
        pc_var_type_spec = {
                'timestamp': str(),
                'PC1': str(),
                'PC2': str(),
                'PC3': str(),
                'PC4': str(),
                'PC5': str(),
                'PC6': str(),
                'PC7': str(),
                'PC8': str(),
                'PC9': str(),
                'PC10': str(),
                'PC11': str(),
                'PC12': str(),
                }
        metadata_var_type_spec = {'timestamp': str(), 'key': str()}
        self.df_data = pd.DataFrame(columns=[pc_var_type_spec])
        self.df_press = pd.DataFrame(columns=[metadata_var_type_spec])
        self.filepath = str()
        self.init_record(data_file_path, data_file_textlines)
        return

    def init_record(self, data_file_path, data_file_textlines):
        self.filepath = data_file_path
        # Now, convert textlines into pandas DataFrame
        # TODO: Finish me
        pass

def store_file_data(data_file_path, data_file_textlines):
    pass

if __name__ == '__main__':
    print('Hello world!')
    # Find all files, using rglob()
    possible_data_files = BASE_DIR.rglob(r'output_*.txt')
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
        curr_data_record = ExperimentResult(data_file_path, data_file_textlines)

        # Break here
        break
