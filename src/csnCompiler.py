## @package csnCompiler
# Definition of the Compiler class. 
# \ingroup compiler

class Compiler:
    """ Abstract Compiler. """
    def __init__(self):
        # protected, accessed in sub classes
        self._configurationName = None
        
    def GetConfigurationName(self):
        return self._configurationName

    def SetConfigurationName(self, value):
        self._configurationName = value

