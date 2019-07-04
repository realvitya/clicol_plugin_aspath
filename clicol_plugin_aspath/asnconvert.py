#!/usr/bin/env python

import re
import sys

def asdot2plain( asdot ):
    "This returns an ASPLAIN formated ASN given an ASDOT+ format"
    left,right = re.split('\.|:', asdot)
    ret = int(left) * 65536 + int(right)
    return ret

def asplain2asdot( asplain ):
    "This returns an ASDOT+ formated ASN given an ASPLAIN format,"
    "unless given a 16-bit ASN"
    begin = int(asplain)
    current = begin
    new = current
    counter = 0
    while current > 65535:
        new = current - 65536;
        counter = counter + 1
        current = new
    if counter == 0:
        ret = str(new)
    else:
        ret = str(counter) + "." + str(new)
    return ret

def main():
    "Runs as a utility to convert between formats automatically"
    length = len(sys.argv)

    if length == 2:
        start = sys.argv[1]
        if '.' in start:
            # ASDOT+
            print asdot2plain( start )
        elif ':' in start:
            # ASDOT+
            print asdot2plain( start )
        else:
            # ASPLAIN
            print asplain2asdot( start )
    else:
        print "Usage:"
        print "  " + sys.argv[0] + " <asn>"
        print ""
        print "    <asn> - ASN to convert in ASPLAIN or ASDOT+ format"
        print ""
        print "Outputs ASPLAIN if given ASDOT+, and ASDOT+ if given ASPLAIN,"
        print "unless as 16-bit ASN, then no change"
        print ""

if __name__ == "__main__":
    main()
