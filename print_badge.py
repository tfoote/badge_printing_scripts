#!/usr/bin/env python

import em
import subprocess
import tempfile

PRINTER = 'QL-1060N'
DEBUG_SVG = False
PRINT = True
# INPUT_SVG = '4x6example.svg' # DK-1241
# INPUT_SVG = '2.4x3.9example.svg' # DK-1202
INPUT_SVG = '2.1x3.9example.svg' # DK-N5224


def print_badge(name, affiliation):

    with open(INPUT_SVG, 'r') as fh:
        template = fh.read()

    subs = {}
    subs['fullname'] = name
    subs['affiliation'] = affiliation

    svgout = em.expand(template, subs)

    if DEBUG_SVG:
        print('='*80)
        print(svgout)
        print('='*80)

    svgfile = tempfile.NamedTemporaryFile(suffix='.svg')
    pdffile = tempfile.NamedTemporaryFile(suffix='.pdf')


    with open(svgfile.name, 'w') as fh:
        fh.write(svgout)
    cmd = ['inkscape', '-f', svgfile.name, '-A', pdffile.name]
    print("command is %s" % cmd)
    subprocess.check_call(cmd)

    cmd = ['lp', '-d', PRINTER, pdffile.name]
    print("command is %s" % cmd)
    if PRINT:
        subprocess.check_call(cmd)
    else:
        print("skipping printing due to PRINT being false")




import csv
import string

with open('participants.csv', 'rb') as csvfile:
    csvdom = csv.reader(csvfile, delimiter=',')

    counter = 0
    max_length = 0
    for row in csvdom:
        name, affiliation, _ = row
        # print(name)
        last, first = name.split(',')
        fullname = '%s %s' % (first, last)
        fullname = string.capwords(fullname)
        print ("name: %s ... affiliation %s" % (fullname, affiliation))
        # max_length = max(max_length, len(affiliation))
        # print(max_length)
        # if counter > 2:
        #     break
        counter += 1
        print_badge(fullname, affiliation)
