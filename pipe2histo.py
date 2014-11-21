#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Program which takes floats (integers) through a pipe and 
plots a histogram with bin size (<BINS>) into a specified outfile <OUTFILE>.png'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab
import sys
plt.style.use('ggplot')

def parse_stdin_for_histo():
	x = []
	for line in sys.stdin:
		if not line.strip():
			pass
		else:
			value = line.rstrip('\n')
			try:
				float(value)
			except:
				print "[WARN] - " + value + " is not a number"
			else:
				x.append(float(value))	
	return x

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
	if len(sys.argv) != 3:
		sys.exit("USAGE : ... | pipe2histo.py <BINS> <OUT>")
	bin = int(sys.argv[1])
	outfile = sys.argv[2]
	x = parse_stdin_for_histo()
	plot_histo(x, bin, outfile)