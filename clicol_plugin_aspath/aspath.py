#!/usr/bin/env python
"""
 CLICOL plugin package for aspath resolution

 example output for sh ip bgp:
 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ? ATT ABC --- EFH
 *>                    10.123.234.154                         0 21302 13979 65120 64932 ? ATT ABC --- EFH
"""
from __future__ import print_function
from __future__ import unicode_literals
from builtins import input
from .asnconvert import asplain2asdot
import re
import os

class ASPath:
    loadonstart = True
    db = dict()
    cmap = dict()
    setup = dict()
    unknownstr = "---"
    regex = ()
    outtype = "append"
    forcedotformat = "yes"
    __ASPATH_KEY = "A"
    keybinds = (__ASPATH_KEY)

    def __init__(self, setup):
        (self.setup, self.cmap) = setup
        self.regex = re.compile(self.cmap['BOL']+r"( ?[\*>sdhirSmbfxact ]{2}.{58,60}| {21,})( (?:[1-9][0-9.]* *)+)( [ie?])([\r\n]*)$", re.M)
        if 'dbfile' in self.setup.keys():  #  Set custom dbfile
            dbfilename = self.setup['dbfile']
        else:
            dbfilename = "~/.clicol/plugin-aspath.db"
        if 'unknownstr' in self.setup.keys():  #  Set custom unknown string instead of ---
            self.unknownstr = self.setup['unknownstr']
        if 'forcedotformat' in self.setup.keys():  #  convert decimal format AS number to dotted format
            self.forcedotformat = self.setup['forcedotformat']
            #  accept only below values
            if self.forcedotformat in ("y", "Y", "yes","Yes","on","On","1"):
                self.forcedotformat = "yes"
        if 'outtype' in self.setup.keys():  #  Set output type (inline|append)
            if self.setup['outtype'] in ("inline", "append"):
                self.outtype = self.setup['outtype']
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
                raise

        dbfile.close()

    def resolveas(self, aspath):
        aslist = ""
        aslist_in = aspath.group(3)
        for AS in aslist_in.split():
            if self.forcedotformat == "yes" and (int(AS)>65535):
                AS_dotted = asplain2asdot(AS)
                aslist_in = aslist_in.replace(AS, AS_dotted)
                AS = AS_dotted
            if AS in self.db.keys():
                if self.outtype == "inline":
                    aslist += "%s(%s%s%s) " % (AS, self.cmap['important_value'], self.db[AS], self.cmap['default'])
                else:
                   aslist = " ".join((aslist, self.db[AS]))
            else:
                if self.outtype == "inline":
                    aslist += "%s " % AS
                else:
                    aslist = " ".join((aslist, self.unknownstr))
        if self.outtype == "inline":
            return "%s%s %s%s%s" % (aspath.group(1), aspath.group(2), aslist.rstrip(), aspath.group(4), aspath.group(5))
        else:
            return "%s%s%s%s %s%s%s%s" % (aspath.group(1), aspath.group(2), aslist_in, aspath.group(4),
                                      self.cmap['important_value'], aslist.lstrip(), self.cmap['default'], aspath.group(5))

    def plugin_preprocess(self, input, effects=[]):
        return self.regex.sub(self.resolveas,input)

    def plugin_command(self, cmd):
        if cmd == self.__ASPATH_KEY:
            aspath = str(input("\r" + " " * 100 + "\rASPATH: "))
            m = re.match("()()((?:[0-9]+)(?: [0-9]+)?)()()", aspath)
            if m:
                print("Resolved:" + self.resolveas(m).strip().encode().decode('unicode_escape'))

    def plugin_help(self, command):
        if command == self.__ASPATH_KEY:
            return " Resolve AS PATH"
        else:
            return ""

    def plugin_test(self):
        return ("plugin.aspath", "\n preprocess:%s" % self.plugin_preprocess("""
 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ?
 *>                    10.123.234.154                         0 21302 13979 65120 64932 ?"""))

