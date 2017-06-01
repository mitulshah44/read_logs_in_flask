#!/usr/bin/env python
"""
Script is written to select log file
from list of logs and return "last 10 lines"
like "tail -f"
"""
__author__ = "Mitul Shah"
__version__ = "1.0.0"

import os
from flask import (render_template, jsonify, request)
import json
from collections import defaultdict
from config import app

modifiedTime = {}


def files_from_dir(dirPath, logfiles={}):
    """
    Return : list of files located in log folders
    fuction recall itself if subfolders contain file
    """
    root = dirPath.split('/')[-1]
    try:
        for child in os.listdir(dirPath):
            childPath = os.path.join(dirPath, child)
            if os.path.isdir(childPath):
                files_from_dir(childPath, logfiles)
            else:
                modifiedTime[childPath] = os.path.getctime(childPath)
                logfiles[root].append([childPath, child])
    except Exception as e:
        print(e)
    return logfiles


def get_logs():
    """
    function returns list of files located in specific directory
    """
    cwd = os.getcwd()
    logdir = os.path.join(cwd, 'logs')
    files = files_from_dir(logdir, defaultdict(list))
    return files


@app.route('/api/getcontent', methods=['POST'])
def get_content():
    """
    function behave like "tail -f"
    input: file path
    output: return line from file
    """
    results = {'modified': False, 'lines': []}
    modified = False
    try:
        fn = request.json['path']
        newfile = request.json['isNewFile']
        lastmodified = os.path.getctime(fn)

        # if user has changed file from dropdown, update modified time
        if fn in modifiedTime and newfile:
            modifiedTime[fn] = lastmodified

        # if file is modified, update modified time and chang flag true
        if fn in modifiedTime and modifiedTime[fn] < lastmodified:
            modifiedTime[fn] = lastmodified
            modified = True

        # allow to run code if modified or change file from dropdown
        if modified or newfile:
            with open(fn, "r") as f:
                f.seek (0, 2)
                fsize = f.tell()
                # print(fsize)
                if modified and not newfile:
                    f.seek (0, 0)
                    lines = f.readlines()
                else:
                    f.seek(max(fsize - 1024, 0), 0)
                    lines = f.readlines()
                    lines = lines[-10:]
                results['lines']= lines
                results['modified'] = True
    except Exception as e:
        print(e)

    return jsonify(results)

@app.route('/', methods=['GET'])
def main():
    """ Homepage to render data"""
    res = get_logs()
    return render_template('index.html', data=res)


if __name__ == "__main__":
    app.run()
