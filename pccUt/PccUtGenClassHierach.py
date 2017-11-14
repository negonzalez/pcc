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
#!/opsw/util/python/bin/python
#******************************************************************************
# ESO/DMD
#
# "@(#) $Id: PccUtGenClassHierach.py,v 1.2 2011/11/24 13:06:42 amanning Exp $"
#
# Who       When        What
# --------  ----------  -------------------------------------------------------
# jknudstr  08/07/2008  Created
#

"""
Various small utilities.
"""

import sys, os, glob, re


def lstHasVal(lst,
              val):
    """
    Check if a list contains a certain value. If yes, return index of this
    value otherwise return -1 if the list does not contain the value.

    Returns:    Index of value or -1 if list does not contain value (integer).
    """
    try:
        return lst.index(val)
    except:
        return -1


def srcFile2ModName(filename):
    """
    From a given source filename, generate a Python module name.

    Return:   Python module name (string).
    """
    return os.path.basename(filename).split(".")[0]
       

def genClassHier(fileList):
    """
    Generate the file hierarchie from a list of files.

    fileList:    File list (list/string).

    Returns:     Void.
    """
    ########################################################################
    # Step 1: Check for circular dependencies.
    ########################################################################
    
    # Build up a dictionary with the modules included for each source file.
    modDic = {}
    for file in fileList:
        fo = open(file)
        lines = fo.readlines()
        fo.close()

        # Loop over contents of file and find the dependencies.
        modName = srcFile2ModName(file)     
        modDic[modName] = []
        for line in lines:
            if ((line.find("import") == 0) and ((line.find("from") == -1))):
                modules = line.split("import")[1].split(",")
                for module in modules:
                    modDic[modName].append(module.strip())

    # Remove modules not considered by this analysis.
    for mod in modDic.keys():
        idx = 0
        while idx < len(modDic[mod]):
            if (lstHasVal(modDic.keys(), modDic[mod][idx]) == -1):
                modDic[mod].pop(idx)
            else:
                idx += 1

    # Go through the dictionary with the dependencies for each module
    # and indicate if circular dependencies are found.
    print "Circular references:"
    for mod in modDic.keys():
        modDic[mod].sort()
        for importMod in modDic[mod]:
            if (modDic.has_key(importMod)):
                idx = lstHasVal(modDic[importMod], mod)
                if (idx != -1):
                    modDic[importMod].pop(idx)
                    #del modDic[importMod][idx]
                    print "Python module: " + mod + " and: " +\
                          importMod + " make circular references to eachother"
            else:
                # Remove os, sys, ...  - ie. std. Python modules.
                idx = lstHasVal(modDic[mod], importMod)
                if (idx != -1):
                    modDic[mod].pop(idx)
                    #del modDic[mod][idx]

    ########################################################################
    # Step 2: Generate module hierarchie
    ########################################################################
    hierarchList1 = []
    for mod in modDic.keys():
        if (mod != "__init__"): hierarchList1.append([mod, modDic[mod]])
    hierarchList2 = []
    for modInfo in hierarchList1:
        modName = modInfo[0]
        idx = 0
        while idx < len(hierarchList2):
            if (lstHasVal(hierarchList2[idx][1], modName) != -1):
                break
            else:
                idx += 1
        if (idx == len(hierarchList2)):
            hierarchList2.insert(0, modInfo)
        else:
            hierarchList2.insert(idx, modInfo)
    hierarchList3 = []
    for modInfo in hierarchList2:
        if (len(modInfo[1]) == 0):
            hierarchList3.insert(0, modInfo)
        else:
            hierarchList3.append(modInfo)

    print "\nSource code file hierarchie:"
    for modInfo in hierarchList3:
        print "Module: " + modInfo[0] + " - Included modules: " +\
              re.sub("'", "", str(modInfo[1])[1:-1])
    

def correctUsage():
    """
    """
    print "Correct usage is:\n"
    print "PccGenClassHierach <python src files>\n\n"
    


if __name__ == '__main__':
    """
    Main function generating the class hierarchie.
    """
    if (len(sys.argv) < 2):
        correctUsage()
        sys.exit(1)

    fileList = []
    for pat in sys.argv[1:]:
        fileList += glob.glob(pat)
    genClassHier(fileList)


# --- oOo ---
