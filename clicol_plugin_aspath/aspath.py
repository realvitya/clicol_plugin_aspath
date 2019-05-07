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

#import pudb

class ASPath:
    loadonstart = True
    db = dict()
    cmap = dict()
    setup = dict()
    unknownstr = "---"
    regex = ()

    def __init__(self, setup):
        #pudb.set_trace()
        (self.setup, self.cmap) = setup
        self.regex = re.compile(self.cmap['BOL']+r"( [\*>sdhirSmbfxact ]{3}.{58,60}| {21,})( (?:[0-9]+ *)+)( [ie?])([\r\n]*)$", re.M)
        if 'dbfile' in self.setup.keys():  #  Set custom dbfile
            dbfilename = self.setup['dbfile']
        else:
            dbfilename = "~/.clicol/plugin-aspath.db"
        if 'unknownstr' in self.setup.keys():  #  Set custom unknown string instead of ---
            self.unknownstr = self.setup['unknownstr']
        try:
            dbfile = open(os.path.expanduser(dbfilename),"r")
        except:
            return
        while True:
            try:
                line = dbfile.readline().split("\t")
                if len(line[0])>0:
                    if line[0][0] == "#":
                        # Ignore remarks
                        continue
                if len(line)<3:
                    break
                (AS,SITE,SITECODE) = (line[0], line[1], line[2])  #  First 3 value is interesting
                self.db[AS] = SITECODE.rstrip()
            except EOFError:
                break
            except ValueError:
                # Ignore bad input
                pass
            except:
                #pudb.set_trace()
                raise

        #pudb.set_trace()
        dbfile.close()

    def resolveas(self, aspath):
       aslist = ""
       for AS in aspath.group(3).split():
          if AS in self.db.keys():
             aslist = " ".join((aslist, self.db[AS]))
          else:
             aslist = " ".join((aslist, self.unknownstr))
       return "%s%s%s%s %s%s%s%s" % (aspath.group(1), aspath.group(2), aspath.group(3), aspath.group(4),
                              self.cmap['important_value'], aslist.lstrip(), self.cmap['default'], aspath.group(5))

    def preprocess(self, input):
       #pudb.set_trace()
       return self.regex.sub(self.resolveas,input)

    def test(self):
        return ("plugin.aspath", "\n preprocess:%s" % self.preprocess("""
 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ?
 *>                    10.123.234.154                         0 21302 13979 65120 64932 ?"""))

