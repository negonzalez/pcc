#*******************************************************************************
# ALMA - Atacama Large Millimeter Array
# Copyright (c) ESO - European Southern Observatory, 2011
# (in the framework of the ALMA collaboration).
# All rights reserved.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#*******************************************************************************
#******************************************************************************
# ESO/DFS
#
# "@(#) $Id: PccSimpleFitsReader.py,v 1.2 2011/11/24 13:06:42 amanning Exp $"
#
# Who       When        What
# --------  ----------  -------------------------------------------------------
# jknudstr  09/12/2002  Created
#

"""
This module provides a very simple FITS reader, which parses a FITS file
line per line, and delivers back a list containing dictionaries (one per
extension - note, FITS extensions not yet supported) and having keywords as
keys. 
"""

import sys


#def splitLine(line):
#    """
#    """
#    idx = 0
#    while idx
#
#    return (key, val, com)


def getFitsHdrs(filename):
    """
    Get the FITS keywords of the header, and return a list, that contains
    dictionaries (one per header), with the keyword cards as dictionary
    keys, pointing to tuples with the values.

    NOTE: FITS Extensions are not yet supported -> There is only parsed
          until the first occurrence of the END keyword.

    filename:    Name of the FITS file to parse (string).

    Returns:     List with dictionaries (list/dictionary).
    """
    hdrList = []
    fo = open(filename, "r")
    blockSize = (10 * 2880)
    loop = 1
    hdrDic = {}
    while (loop):
        # Read in header contents in blocks of 10 * 2880 bytes.
        buf = fo.read(blockSize)
        if (buf == ""): break
        buf2 = ""
        
        # Parse the next block.
        idx = 0
        discard = 0
        bufSize = len(buf)
        while (idx < bufSize):
            newIdx = (idx + 80)
            if (newIdx > bufSize): newIdx = bufSize
            buf2 += buf[idx:newIdx] + "\n"
            idx = newIdx

        # Now split up each line.
        lines = buf2.split("\n")
        for line in lines:
            line = line.strip()
            if (line == ""): continue
            
            # Special handling of HISTORY and COMMENT.
            if ((line.find("HISTORY ") == 0) or
                (line.find("COMMENT ") == 0) or
                (line.find("ESO-LOG") == 0)):
                key = line[0:7]
                com = line[8:].strip()
                if (hdrDic.has_key(key)):
                    hdrDic[key].append([key, "", com])
                else:
                    hdrDic[key] = [[key, "", com]]
            elif (line.find("END") == 0):
                if (hdrDic.has_key("END")):
                    hdrDic["END"].append(["END", "", ""])
                else:
                    hdrDic["END"] = [["END", "", ""]]
                loop = 0
                break
            else:
                # Parse a normal FITS line or hierarchical FITS line.
                # SIMPLE  =                    T          / Standard FITS 
                # HIERARCH ESO DET CHIP1 NX    =         4096 / # of pixels
                # HIERARCH ESO CAT TST         = 'XX/YY/ZZ'   / Test
                # CHECKSUM= 'ZOZAgNX7ZNXAfNX7'  / ASCII 1's complement checksum 
                lineEls = line.split("=")
                key = lineEls[0].strip()

                ###############################################
                # Get value and comment.
                valCom = lineEls[1].strip()
                # Get value + command
                if (valCom[0] == "'"):
                    # Get string value + comment.
                    lineEls = valCom.split("'")
                    val = "'" + lineEls[1].strip() + "'"
                    if (len(lineEls) > 2):
                        idx = 0
                        lenComRaw = len(lineEls[2])
                        while ((idx < lenComRaw) and \
                               ((lineEls[2][idx] == " ") or
                                (lineEls[2][idx] == "/"))):
                            idx += 1
                        com = lineEls[2][idx:].strip()
                        # If there are more elements this means that
                        # there were 's in the comment field.
                        if (len(lineEls) > 3):
                            for el in lineEls[3:]:
                                com += "'" + el                        
                    else:
                        com = ""
                else:
                    # Get !string + comment.
                    lineEls = valCom.split("/")
                    val = lineEls[0].strip()
                    if (len(lineEls) > 1):
                        com = lineEls[1].strip()
                    else:
                        com = ""
                ###############################################

                if (hdrDic.has_key(key)):
                    hdrDic[key].append([key, val, com])
                else:
                    hdrDic[key] = [[key, val, com]]
    hdrList.append(hdrDic)
        
    return hdrList


if __name__ == '__main__':
    """
    Main routine to make a connection to the DB.
    """
    print getFitsHdrs(sys.argv[1])


#
# ___oOo___
