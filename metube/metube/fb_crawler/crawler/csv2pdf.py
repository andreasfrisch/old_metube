#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import subprocess
import time
from metube.settings import PDF_OUTPUT_DIRECTORY

def csv2pdf(filepath):
	#Assert correct file type input
	(fname, _, type) = filepath.rpartition('.')
	if type != "csv":
		print("please input an .csv-file")
		return ''

	#Open input file for reading
	try:
		#print("Opening file: %s" % filepath)
		input_file = open(filepath, "r", buffering=1)
	except:
		#print("No such file found")
		return ''

	#Open output file for writing (replacing existing files)
	output_name = fname + ".tex"
	#print("Creating file: %s" %output_name)
	output_file = open(output_name, "w")

	#Generate tex-preamble
	preamble = "\\documentclass[a4paper,12pt]{article}\n"+ \
			"%\\usepackage[utf8x]{inputenc}\n"+ \
			"%\\usepackage{ucs}\n"+ \
			"\\usepackage[danish]{babel}\n"+ \
			"\\usepackage[T1]{fontenc}\n"+ \
			"\\usepackage{url}\n"+ \
			"%\\usepackage{colortbl}\n"+ \
			"%\\usepackage{pdfpages}\n"+ \
			"\\usepackage{longtable}\n"+ \
			"\\usepackage[margin=0.5cm]{geometry}\n"+ \
			"\\setlength{\parindent}{0in}\n"+ \
			"\\setlength{\parskip}{0.1in}\n"+ \
			"\\begin{document}\n"+ \
			"\\begin{longtable}{p{2cm} p{4cm} p{2cm} p{9cm} p{2cm}}\n"

	output_file.writelines(preamble)

	#Generate document
	for line in input_file:
		tokens = line \
			.replace('\n','') \
			.replace('$','POLSOCDOLLARESCAPE') \
			.replace('\\','$\\backslash$') \
			.replace('POLSOCDOLLARESCAPE','\$') \
			.replace('&','\&') \
			.replace('#','\#') \
			.replace('~','\~ ') \
			.replace('_','\_') \
			.replace('%','\%') \
			.replace('}','\}') \
			.replace('{','\{') \
			.replace('^','\string^') \
			.split(',')
		#Tokens:
		#	type, name, FB_id, time, date, likes, comments, [rest]
		type = tokens[0]
		name = tokens[1]
		facebook_id = tokens[2]
		time = tokens[3]
		date = tokens[4]
		likes = tokens[5]
		comments = tokens[6]
		message = ",".join(tokens[7:])
		if not type == 'comment':
			output_file.writelines(
					"\\textbf{%s} & \\textbf{%s} -- comments: %s & %s %s & %s & %s \\\\\n" % (
						type,
						name,
						comments, #name, comments
						time, date, #timestamp
						message,
						likes))  #likes [-1] is new line
		else:
			output_file.writelines(
					"%s & %s -- id: %s & %s %s & %s & %s \\\\\n" % (
						type,
						name,
						facebook_id, #name, id
						time, date, #timestamp
						message,
						likes))  #likes [-1] is new line

	output_file.writelines(
	"""
\end{longtable}
\end{document}
	""")

	input_file.close()
	output_file.close()

	subprocess.call(["xelatex", "-interaction=nonstopmode", "-output-directory=%s" % PDF_OUTPUT_DIRECTORY, output_name])
	
	return fname.split("/")[-1]+".pdf"

if __name__ == '__main__':
	csv2pdf(sys.argv[1])
