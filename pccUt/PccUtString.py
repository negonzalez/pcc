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
# "@(#) $Id: PccUtString.py,v 1.2 2011/11/24 13:06:42 amanning Exp $"
#
# Who       When        What
# --------  ----------  -------------------------------------------------------
# jknudstr  04/05/2000  Created
#

"""
Module providing string manipulating functions.
"""

import string


def trimString(rawString,
               trimChars):
    """
    Trims a string from both ends according to the list of characters
    given in the "trimChars" input parameter.
    
    rawString:     String to be trimmed.
    
    trimChars:     Characters to trim away from the ends of "rawString".
    
    Returns:       The trimmed string.
    """
    if (len(rawString) == 0):
        return ""
    idx1 = 0
    lenRawStr = (len(rawString) - 1)
    while ((string.find(trimChars, rawString[idx1]) != -1) and
           (idx1 < lenRawStr)):
        idx1 = (idx1 + 1)
    if (idx1 == lenRawStr) and (string.find(trimChars, rawString[idx1]) == -1):
        return rawString[idx1]
    elif (idx1 == lenRawStr):
        return ""
    idx2 = (len(rawString) - 1)
    while (string.find(trimChars, rawString[idx2]) != -1):
        idx2 = (idx2 - 1)
    trimmedString = rawString[idx1:(idx2 + 1)]

    return trimmedString


def lastChar(txt):
    """
    Return the last char of a string.

    txt:     Variable referring to the string.
    """
    return txt[len(txt) - 1]


#
# ___oOo___
