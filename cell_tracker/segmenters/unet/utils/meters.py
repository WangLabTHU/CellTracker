
# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import os
import csv


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


""" 
    Export data to csv format. Creates new file if doesn't exist,
    otherwise update it.
    Args:
        header (list): headers of the column
        value (list): values of correspoding column
        file_path: file name with path
"""


def export_history(header, value, file_path):

    file_existence = os.path.isfile(file_path)

    # If there is no file make file
    if file_existence == False:
        file = open(file_path, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(value)
    # If there is file overwrite
    else:
        file = open(file_path, 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(value)
    # Close file when it is done with writing
    file.close()
