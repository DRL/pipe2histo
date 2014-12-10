#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Program which takes floats (integers) through a pipe and 
plots a histogram with bin size (<BINS>) into a specified outfile <OUTFILE>.png'''

import numpy as np
#import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab
import sys

#mat.use('pdf')
plt.style.use('ggplot')

def parse_stdin_for_histo():
	x = []
	strings = {}
	for line in sys.stdin:
		if not line.strip():
			pass
		else:
			value = line.rstrip('\n')
			try:
				float(value)
			except:
				print "[WARN] - " + value + " is not a number"
				value = value.replace(" ", "_ ")
				strings[str(value)] = strings.get(str(value), 0) + 1
			else:
				x.append(float(value))	

	return x, strings

def plot_bar(string_dict, outfile):
	width = 0.30
	counts, strings = [], []
 
	for key in sorted(string_dict, key=string_dict.get, reverse=False):
		counts.append(string_dict[key])
		strings.append(key)
	index = np.arange(len(strings))
	plt.figure(1, figsize=(20,20), dpi=400)
	ax = plt.axes()
	bar = ax.barh(index, counts, width, facecolor='#f6b114')
	ax.set_xscale('log')
	ax.set_yticks(index+width/2)
	ax.set_yticklabels( strings, rotation='horizontal')
	ax.grid(True, which="major", lw=.5, linestyle='-')
	ax.set_xlim( min(counts)-0.5, max(counts) + int( 0.20 * max(counts) ) ) 
	#ax.set_ylim( 10, 1000 )
	ax.plot()
	pylab.savefig(outfile + "." + fig_format, format=fig_format)

def plot_histo(x, bin, outfile):
	axHist = plt.axes()
	axHist.grid(True, which="major", lw=.5, linestyle='-')
	axHist.set_xlim( min(x)-2, max(x)+2 )
	axHist.hist(x, bins = bin, histtype='bar', stacked=False, normed=False, lw = 1, facecolor='#f6b114')
	plt.plot()
	data = np.array(x)
	y, binEdges = np.histogram(data,bins=bin)
	axHist.set_ylim( min(y), max(y)+10 )
	bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
	pylab.plot(bincenters,y,'-', color='#004c00')
	pylab.savefig(outfile + "." + fig_format, format=fig_format)

if __name__ == '__main__':
	fig_format = 'png'
	if len(sys.argv) < 2:
		sys.exit("USAGE : ... | pipe2histo.py <OUT> [<BINS>]")
	outfile = sys.argv[1]
	bin = 10
	try:
		bin = int(sys.argv[2]) 
	except:
		pass

	x, strings = parse_stdin_for_histo()
	if strings:
		plot_bar(strings, outfile)
	if x:
		plot_histo(x, bin, outfile)