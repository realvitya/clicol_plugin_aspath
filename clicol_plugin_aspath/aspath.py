#!/usr/bin/env python
"""
 CLICOL plugin package for aspath resolution

 example output for sh ip bgp:
 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ? ATT ABC --- EFH
 *>                    10.123.234.154                         0 21302 13979 65120 64932 ? ATT ABC --- EFH
"""
from __future__ import print_function
from __future__ import unicode_literals
import re
import os

import pudb

class ASPath:
    loadonstart = True
    db = dict()
    regex = re.compile(r"^( [^0-9]{3} +(?:[0-9\.:]+/[0-9]+ +(?:[0-9\.:]+ +[0-9]+ +[0-9]+ +)|[0-9.]+ +)[0-9]+ +)((?:[0-9]+ )+)([ie?])([\r\n]*)$", re.M)

    def __init__(self):
        try:
            dbfile = open(os.path.expanduser("~/.clicol/plugin-aspath.db"),"r")
        except:
            return
        while True:
	    try:
            	line = dbfile.readline().split("\t")
                if len(line)<3:
                    break
            	(AS,SITE,SITECODE) = (line[0], line[1], line[2])  #  First 3 value is interesting
	    	self.db[AS] = SITECODE.rstrip()
	    except EOFError:
                break
            except ValueError:
                break
            except:
                raise

        dbfile.close()

    def resolveas(self, aspath):
       aslist = ""
       for AS in aspath.group(2).split():
          if AS in self.db.keys():
             aslist = " ".join((aslist, self.db[AS]))
          else:
             aslist = " ".join((aslist, "---"))
       return "%s%s%s%s%s" % (aspath.group(1), aspath.group(2), aspath.group(3),
                              aslist, aspath.group(4))

    def preprocess(self, input):
       return self.regex.sub(self.resolveas,input)

