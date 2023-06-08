# -*- coding: utf-8 -*-`

# Copyright Inria Sophia Antipolis-Méditerranée 2022. All Rights Reserved.
# Author: Kacper Pluta <kacper.pluta@inria.fr>
# This file cannot be used without a written permission from the author(s).

# based on https://www.jamesfheath.com/2020/06/logging-in-python-while-multiprocessing.html and
# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes


import logging
import logging.handlers
import multiprocessing
from os import path
import sys
import traceback


def listener_configurer(log_name, log_file_path,
                        fmtr=logging.Formatter('%(asctime)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')):
    """ Configures and returns a log file based on 
    the given name

    Arguments:
        log_name (str): String of the log name to use
        log_file_path (str): String of the log file path

    Returns:
        logger: configured logging object
    """
    logger = logging.getLogger(log_name)

    fh = logging.FileHandler(path.join(log_file_path, f'{log_name}.log'), encoding='utf-8')
    fh.setFormatter(fmtr)
    logger.setLevel(logging.INFO)
    current_fh_names = [fh.__dict__.get('baseFilename', '') for fh in logger.handlers]
    if not fh.__dict__['baseFilename'] in current_fh_names:  # This prevents multiple logs to the same file
        logger.addHandler(fh)

    return logger


def listener_process(queue, configurer, log_name, log_file_path):
    """ Listener process is a target for a multiprocess process
    that runs and listens to a queue for logging events.

    Arguments:
        queue (multiprocessing.manager.Queue): queue to monitor
        configurer (func): configures loggers
        log_name (str): name of the log to use

    Returns:
        None
    """
    configurer(log_name, log_file_path)

    while True:
        try:
            record = queue.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)
        except Exception:
            print('Failure in listener_process', file=sys.stderr)
            traceback.print_last(limit=1, file=sys.stderr)
