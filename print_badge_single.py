#!/usr/bin/env python

import em
import subprocess
import tempfile

PRINTER = 'QL-1060N'
DEBUG_SVG = False
PRINT = True
# INPUT_SVG = '4x6example.svg' # DK-1241
INPUT_SVG = '2.4x3.9example.svg' # DK-1202
INPUT_SVG = '2.1x3.9example.svg' # DK-N5224


with open(INPUT_SVG, 'r') as fh:
    template = fh.read()

subs = {}
subs['fullname'] = 'Tully Foote has a very long name'
subs['affiliation'] = 'The Open Source Robotics Foundation which wraps and has unicode πρ.'

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
