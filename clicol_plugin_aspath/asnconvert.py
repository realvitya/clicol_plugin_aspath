#!/usr/bin/env python

from __future__ import print_function
import re
import sys

def asdot2plain( asdot ):
    "This returns an ASPLAIN formated ASN given an ASDOT+ format"
    left,right = re.split('\.|:', asdot)
    ret = int(left) * 65536 + int(right)
    return ret


def asplain2asdot(asplain):
    """
    This returns an ASDOT+ formatted ASN given an ASPLAIN format, unless given a 16-bit ASN
    :param asplain: ASPLAIN formatted AS number
    :return: ASDOT+ formatted AS number
    """
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

