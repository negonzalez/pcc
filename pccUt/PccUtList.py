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
# "@(#) $Id: PccUtList.py,v 1.2 2011/11/24 13:06:42 amanning Exp $"
#
# Who       When        What
# --------  ----------  -------------------------------------------------------
# jknudstr  14/11/2000  Created
#

"""
Module providing class PccUtList which is used to navigate lists
using an internal list pointer.
"""

class PccUtList:
    """
    The PCC List Object is used to manage a list of objects, whereby
    a pointer (index) is used to navigate in the list. The initial
    value of the list index is -1.
    """

    def __init__(self):
        """
        Constructor method initializing the class variables.
        """
        self.clear()
        

    def clear(self):
        """
        Clear the contents of the PCC List Object.

        Returns:       Reference to object itself.
        """
        self.__index = -1
        self.__list = []
        return self


    def loadFileInList(self,
                       fileName):
        """
        Loads a file into an internal list, whereby each line break
        is used as delimiter.

        fileName:      Name of file to load.

        Returns:       Reference to object itself.
        """
        fd = open(fileName)
        self.__list = fd.readlines()
        fd.close()
        return self


    def addElement(self,
                   el):
        """
        Append an element to the list.

        Returns:      Reference to object itself.
        """
        self.__list.append(el)
        return self


    def getNextEl(self):
        """
        Increment the internal list pointer and returns the element.

        Returns:       The sequential next element.
        """
        self.__index = self.__index + 1
        return self.__list[self.__index]


    def getPrevEl(self):
        """
        Decrement the internal list pointer and return the element.

        Returns:       The previous list element.
        """
        self.__index = self.__index - 1
        return self.__list[self.__index]


    def getCurEl(self):
        """
        Return the current element (pointed at by the list index).

        Returns:       The list element pointed at.        
        """
        return self.__list[self.__index]
        

    def getIndex(self):
        """
        Return the list index.

        Returns:      List index.
        """
        return self.__index
    
    def noOfEls(self):
        """
        Returns the number of elements contained in the list.

        Returns:      Number of elements in the list.
        """
        return len(self.__list)


    def remainingEls(self):
        """
        Returns the number of elements in the list following the
        present position of the list pointer.

        Returns:      Number of remaining elements in the list.
        """
        if (self.__index == -1):
            return self.noOfEls()
        else:
            return (self.noOfEls() - self.__index - 1)

        
#
# ___oOo___
