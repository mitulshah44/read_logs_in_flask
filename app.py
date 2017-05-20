#!/usr/bin/env python
"""
Script is written to select log file
from list of logs and return "last 10 lines"
like "tail -f"
"""
__author__ = "Mitul Shah"
__version__ = "1.0.0"

import os
from flask import (render_template,jsonify, request)
import json
from collections import defaultdict
from config import app



def files_from_dir(dirPath, logfiles={}):
	"""
	Return : list of files located in log folders
	fuction recall itself if subfolders contain file
	"""
	root = dirPath.split('/')[-1]
	try:
	    for child in os.listdir(dirPath):
			childPath = os.path.join(dirPath,child)
			if os.path.isdir(childPath):
			    files_from_dir(childPath, logfiles)
			else:
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
	files  = files_from_dir(logdir, defaultdict(list))
	return files


@app.route('/api/getcontent', methods=['POST'])
def get_content():
	"""
	function behave like "tail -f"
	input: file path
	output: return line from file
	"""
	lines = []
	try:
		fn = request.json['path']
		with open(fn, "r") as f:
			f.seek (0, 2)            
			fsize = f.tell() 
			# print(fsize)
			f.seek (max (fsize-1024, 0), 0) 
			lines = f.readlines() 
		lines = lines[-10:] 
	except Exception as e:
		print(e) 
	return jsonify(lines)
	
@app.route('/', methods=['GET'])
def main():
	""" Homepage to render data"""
	res = get_logs()
	return render_template('index.html', data=res)

	
if __name__ == "__main__":
    app.run()
