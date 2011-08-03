## @package csnProjectRegistry
# Registry to store projects from other Modules (to avoid import-overhead). 
import csnProject
import inspect
import os.path
import sys

filenameGlobal = list()

def interpretModule(_moduleCode, _filename):
    # remember filename (because it won't appear in the call stack, there will be only "<string>")
    global filenameGlobal
    filenameGlobal.append(_filename)
    
    # execute the module code in a clean environment
    _globals = dict()
    _locals = dict()
    exec _moduleCode in _globals, _locals
    
    # remove the filename from filename stack
    filenameGlobal.pop()
    
    # return the local variables created by the executed module code
    return _locals

class ProjectRegistry:
    
    def __init__(self):
        self.__defs = dict()
        self.__tpDefs = dict()
    
    def getModule(self, _moduleName, _name, _interpret = True):
        if not (_moduleName, _name) in self.__defs:
            members = None
            if _interpret:
                for path in sys.path:
                    filename = os.path.join(path, "/".join(_moduleName.split("."))) + ".py"
                    if os.path.isfile(filename):
                        foundFilename = filename
                        break
                print "interpret %s" % foundFilename
                f = file(foundFilename, "r")
                code = f.read()
                f.close()
                members = interpretModule(code, foundFilename).items()
            else:
                print "import %s" % _moduleName
                __import__(_moduleName)
                module = sys.modules[_moduleName]
                members = inspect.getmembers(module)
            for memberName, memberValue in members:
                self.__defs[(_moduleName, memberName)] = memberValue
        return self.__defs[(_moduleName, _name)]
    
    def getThirdPartyModule(self, _subFolder, _moduleName, _name, _interpret = True):
        if not (_subFolder, _moduleName, _name) in self.__tpDefs:
            members = None
            if _interpret:
                modulePath = "/".join(_moduleName.split("."))
                for thirdPartyFolder in csnProject.globalCurrentContext.GetThirdPartyFolders():
                    filename = os.path.join(os.path.join(thirdPartyFolder, _subFolder), modulePath) + ".py"
                    if os.path.isfile(filename):
                        foundFilename = filename
                        break
                print "interpret %s" % foundFilename
                f = file(foundFilename, "r")
                code = f.read()
                f.close()
                members = interpretModule(code, foundFilename).items()
            else:
                for thirdPartyFolder in csnProject.globalCurrentContext.GetThirdPartyFolders():
                    sys.path.append( "%s/%s" % (thirdPartyFolder, _subFolder) )
                print "import %s" % _moduleName
                __import__(_moduleName)
                module = sys.modules[_moduleName]
                members = inspect.getmembers(module)
            for memberName, memberValue in members:
                self.__tpDefs[(_subFolder, _moduleName, memberName)] = memberValue
        return self.__tpDefs[(_subFolder, _moduleName, _name)]

