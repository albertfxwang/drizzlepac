#!/usr/bin/env python
"""
functions associated with HST instruments


"""

import sys
import pytools
import util
import acsdata
from pytools import fileutil

class imageObject(filename):
    """
    This returns an imageObject that contains all the
    necessary information to run the image file through
    any multidrizzle function. It is essentially a 
    PyFits object with extra attributes
    
    There will be generic keywords which are good for
    the entire image file, and some that might pertain
    only to the specific chip. Does it make sense to
    have an object with attributes which are general 
    and then dictionaries for each chip? Like a list
    of dictionaries maybe?
    
    or is it better to make a chip class? oo, maybe that,
    so imageObjects have chips
    
    """
    
    def __init__(self,filename):
        
        header=fileutil.getHeader(filename)

        #populate the global attributes
        self.instrument=header["INSTRUME"]
        self.exptime=header["EXPTIME"]
        self.nextend=header["NEXTEND"]
 
        #this is the number of science chips to be processed in the file
        self.numchips=countSCI(filename)
        
        #where chip 1 = SCI,1
        for chip in range(1,numchips,1):
            chipDictionary=getBasicInfo(filename,extension)
            
            #add chip object here
        
    
def getBasicInfo(filename,extension):
    """ 
        return a dictionary with basic instrument data taken from the header
   		of the input filename. This  will be passed around
        to the other functions and should contain enough information to run
        any of the functions that are in multidrizzle without continually
        accessing the header of the file. The actual data will not be passed around,
        file handling will be written inside all the functions.
        
    """
        
    
    
    #these fill in specific instrument information
    #instrData is returned as a dictionary of key vals
    if ("ACS" in instrument):
        instrData=getACSInfo(filename)
    if ("NICMOS" in instrument):
        instrData=getNICMOSInfo(filename)
    if ("WFC3" in instrument):
        instrData=getWFC3Info(filename)
    if("WFPC2" in instrument):
        instrData=getWFPC2Info(filename)
    if("STIS" in instrument):
        instrData=getSTISIInfo(filename)    

        
    #keywords which are common to all instruments
    genericKW=["INSTRUME","NAXIS1","NAXIS2","LTV1","LTV2"]
    
    for key in genericKW:
    	instrData[key]=priHeader[key]

    #Now add in other information we would like to keep track of for the
    #drizzling process
    
    instrData["filename"]=filename
    
        
    return instrData    
    
"""
def countSCI(filename):
    """
        count the number of SCI extensions in the file
    """
    imageHandle=fileutil.openImage(filename,memmap=0)
    
    _sciext="SCI"
    chips=fileutil.findExtname(imageHandle,extname=_sciext):
    
    imageHandle.close()
    return chips

"""    
class InputImage:
    '''The InputImage class is the base class for all of the various
       types of images
    '''

    def __init__(self, filename):
        self.filename = filename
        self.rootname = util.findrootname(filename)
        self.subtractedSky=0.0 #sky subtracted from all the chips for the instrument
        
        setInstrumentParameters(self)
        
        
        
    def setInstrumentParameters(self, instrpars, pri_header):
        """ 
        Sets the instrument parameters.
        """
        self.refplatescale=0.0
        self.instrumentName=None
        self.numberOfChips=1 #these are directly related to the number of science images in the file
        self.dataUnits="electrons" #set to the units the science data is in, as read from header
        
        pass
    
    def doUnitConversions(self):
        """
        Convert the sci extension pixels to electrons
        """
        pass
        
    def getInstrParameter(self, value, header, keyword):
        """ This method gets a instrument parameter from a
            pair of task parameters: a value, and a header keyword.

            The default behavior is:
              - if the value and header keyword are given, raise an exception.
              - if the value is given, use it.
              - if the value is blank and the header keyword is given, use
                the header keyword.
              - if both are blank, or if the header keyword is not
                found, return None.
        """
        if (value != None and value != '')  and (keyword != None and keyword.strip() != ''):
            exceptionMessage = "ERROR: Your input is ambiguous!  Please specify either a value or a keyword.\n  You specifed both " + str(value) + " and " + str(keyword) 
            raise ValueError, exceptionMessage
        elif value != None and value != '':
            return self._averageFromList(value)
        elif keyword != None and keyword.strip() != '':
            return self._averageFromHeader(header, keyword)
        else:
            return None

    def _averageFromHeader(self, header, keyword):
        """ Averages out values taken from header. The keywords where
            to read values from are passed as a comma-separated list.
        """
        _list = ''
        for _kw in keyword.split(','):
            if header.has_key(_kw):
                _list = _list + ',' + str(header[_kw])
            else:
                return None
        return self._averageFromList(_list)

    def _averageFromList(self, param):
        """ Averages out values passed as a comma-separated
            list, disregarding the zero-valued entries.
        """
        _result = 0.0
        _count = 0

        for _param in param.split(','):
            if _param != '' and float(_param) != 0.0:
                _result = _result + float(_param)
                _count  += 1

        if _count >= 1:
            _result = _result / _count
        return _result


               