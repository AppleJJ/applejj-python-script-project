#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import csv

if len(sys.argv) - 1 < 3:
    print 'Usage: \n\tinsertColumn [inputCsvPath] [sourceCsvPath] [outputCsvPath]'
    sys.exit(1);
with open(sys.argv[1],'r') as csvinput:
    with open(sys.argv[2],'r') as source:
        with open(sys.argv[3], 'w') as csvoutput:
            reader = csv.reader(csvinput,dialect="excel-tab",quoting=csv.QUOTE_ALL)
            sourceReader = csv.reader(source,quoting=csv.QUOTE_ALL)
            writer = csv.writer(csvoutput, lineterminator='\n',dialect="excel-tab",quoting=csv.QUOTE_ALL)
            for row in reader:
                new = next(sourceReader)
                row.append(new[0])
                writer.writerow(row)
