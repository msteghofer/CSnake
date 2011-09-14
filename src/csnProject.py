## @package csnProject
# Definition of the Project handling related classes. 
import csnUtility
import csnDependencies
import csnProjectPaths
import csnInstall
import csnCompile
import csnTests
import inspect
import os.path
import types
import new
from csnUtility import MakeValidIdentifier
import re

globalCurrentContext = None

def Project(_name, _type, _sourceRootFolder = None, _categories = None):
    if _sourceRootFolder is None:
        _sourceRootFolder = csnUtility.NormalizePath(os.path.dirname(inspect.stack()[1][1]))
    return globalCurrentContext.CreateProject(_name, _type, _sourceRootFolder, _categories)

def Dll(_name, _sourceRootFolder = None, _categories = None):
    if _sourceRootFolder is None:
        _sourceRootFolder = csnUtility.NormalizePath(os.path.dirname(inspect.stack()[1][1]))
    return Project(_name, "dll", _sourceRootFolder, _categories)

def Library(_name, _sourceRootFolder = None, _categories = None):
    if _sourceRootFolder is None:
        _sourceRootFolder = csnUtility.NormalizePath(os.path.dirname(inspect.stack()[1][1]))
    return Project(_name, "library", _sourceRootFolder, _categories)

def Executable(_name, _sourceRootFolder = None, _categories = None):
    if _sourceRootFolder is None:
        _sourceRootFolder = csnUtility.NormalizePath(os.path.dirname(inspect.stack()[1][1]))
    return Project(_name, "executable", _sourceRootFolder, _categories)

class Rule:
    """ This class contains a build rule for e.g. Visual Studio, Make, etc """
    def __init__(self):
        self.workingDirectory = ""
        self.command = ""
        self.output = ""
        self.depends = ""

def ToProject(project):
    """
    Helper function that tests if its argument (project) is a function. If so, it returns the result of the function. 
    If not, it returns its argument (project). It is used to treat Project instances and functions returning a Project instance
    in the same way.
    """
    result = project
    if type(project) == types.FunctionType:
        result = project()
    return result

class GenericProject(object):
    """
    The constructors initialises these member variables:
    self.buildSubFolder -- Direct subfolder - within the build folder - for this project. Is either 'executable' or 'library'.
    self.installSubfolder -- Direct subfolder - within the install folder - for targets generated by this project.
    self.useBefore -- A list of projects. The use-file of this project must be included before the use-file of the projects in this list.
    self.configFilePath -- Path to the config file for the project.
    self.sources -- Sources to be compiled for this target.
    self.sourceGroups -- Dictionary (groupName -> sources) for sources that should be placed in a visual studio group.
    self.rules - CMake rules. See AddRule function.
    self.sourcesToBeMoced -- Sources for which a qt moc file must be generated.
    self.sourcesToBeUIed -- Sources for which qt's UI.exe must be run.
    self.filesToInstall -- Contains files to be installed in the build results folder. It has the structure filesToInstall[mode][installPath] = files.
    For example: if self.filesToInstall[\"Debug\"][\"data\"] = [\"c:/one.txt\", \"c:/two.txt\"], 
    then c:/one.txt and c:/two.txt must be installed in the data subfolder of the install folder when in debug mode.
    self.projects -- Set of related project instances. These projects have been added to self using AddProjects.
    self.projectsNonRequired -- Subset of self.projects. Contains projects that self doesn't depend on.
    The project does not add a dependency on any project in this list.      
    self.generateWin32Header -- Flag that says if a standard Win32Header.h must be generated
    self.precompiledHeader -- Name of the precompiled header file. If non-empty, and using Visual Studio (on Windows),
    then precompiled headers are used for this project.
    self.customCommands -- List of extra commands that must be run when configuring this project.
    self.properties -- Custom properties for the target that will use the command ADD_PROPERTY( TARGET PROPERTY <name> [value1 ... )
    """
    
    def __init__(self, _name, _type, _sourceRootFolder = None, _categories = None, _context = None):
        """
        _type -- Type of the project, should be \"executable\", \"library\", \"dll\" or \"third party\".
        _name -- Name of the project, e.g. \"SampleApp\".
        _sourceRootFolder -- Folder used for locating source files for this project. If None, then the folder name is derived from 
        the call stack. For example, if this class' constructor is called in a file d:/users/me/csnMyProject.py, then d:/users/me 
        will be set as the source root folder.
        """    
        self.context = _context
        self.name = _name
        self.type = _type
        if _sourceRootFolder is None:
            _sourceRootFolder = csnUtility.NormalizePath(os.path.dirname(inspect.stack()[1][1]))
        self.pathsManager = csnProjectPaths.Manager(self, _sourceRootFolder)

        # Get the thirdPartyBuildFolder index
        # WARNING: this is only valid for a thirdparty projects!!!
        self.thirdPartyIndex = 0
        count = 0
        for folder in self.context.GetThirdPartyFolders():
            if folder == os.path.dirname(_sourceRootFolder):
                self.thirdPartyIndex = count
                break
            count += 1
        
        self.installManager = csnInstall.Manager(self)
        self.rules = dict()
        self.customCommands = []
        self.categories = _categories
        if self.categories is None:
            self.categories = []
        self.dependenciesManager = csnDependencies.Manager(self)
        self.compileManager = csnCompile.Manager(self)
        self.installSubFolder = ""
        self.testsManager = csnTests.Manager(self)
        self.properties = []
        self.__postCMakeTasks = []

        # Function called before "ADD_LIBARRY"
        self.CMakeInsertBeforeTarget = new.instancemethod(SetCMakeInsertBeforeTarget, self)
        # Function called after "ADD_LIBARRY"
        self.CMakeInsertAfterTarget = new.instancemethod(SetCMakeInsertAfterTarget, self)
        # Function called at the beginning of the CMakeList
        self.CMakeInsertBeginning = new.instancemethod(SetCMakeInsertBeginning, self)
        

    def AddProjects(self, _projects, _dependency = True, _includeInSolution = True): 
        self.dependenciesManager.AddProjects(_projects, _dependency, _includeInSolution)

    def AddSources(self, _listOfSourceFiles, _moc = 0, _ui = 0, _sourceGroup = "", _checkExists = 1, _forceAdd = 0):
        self.compileManager.AddSources(_listOfSourceFiles, _moc, _ui, _sourceGroup, _checkExists, _forceAdd)
                   
    def RemoveSources(self, _listOfSourceFiles):
        self.compileManager.RemoveSources(_listOfSourceFiles)
                            
    def AddDefinitions(self, _listOfDefinitions, _private = 0, _WIN32 = 0, _NOT_WIN32 = 0 ):
        self.compileManager.AddDefinitions(_listOfDefinitions, _private, _WIN32, _NOT_WIN32)
        
    def AddFilesToInstall(self, _list, _location = None, _debugOnly = 0, _releaseOnly = 0, _WIN32 = 0, _NOT_WIN32 = 0):
        self.installManager.AddFilesToInstall(_list, _location, _debugOnly, _releaseOnly, _WIN32, _NOT_WIN32)
                
    def AddIncludeFolders(self, _listOfIncludeFolders, _WIN32 = 0, _NOT_WIN32 = 0):
        self.compileManager.AddIncludeFolders(_listOfIncludeFolders, _WIN32, _NOT_WIN32)
        
    def SetPrecompiledHeader(self, _precompiledHeader):
        self.compileManager.SetPrecompiledHeader(_precompiledHeader)
        
    def AddLibraryFolders(self, _listOfLibraryFolders, _WIN32 = 0, _NOT_WIN32 = 0):
        self.compileManager.AddLibraryFolders(_listOfLibraryFolders, _WIN32, _NOT_WIN32)
        
    def AddLibraries(self, _listOfLibraries, _WIN32 = 0, _NOT_WIN32 = 0, _debugOnly = 0, _releaseOnly = 0):
        self.compileManager.AddLibraries(_listOfLibraries, _WIN32, _NOT_WIN32, _debugOnly, _releaseOnly)
        
    def Glob(self, _path):
        return self.pathsManager.Glob(_path)
    
    def GetProjects(self, _recursive = 0, _onlyRequiredProjects = 0, _includeSelf = False, _onlyPublicDependencies = False, _onlyNonRequiredProjects = False):
        return self.dependenciesManager.GetProjects(_recursive, _onlyRequiredProjects, _includeSelf, _onlyPublicDependencies, _onlyNonRequiredProjects)
        
    def UseBefore(self, _otherProject):
        self.dependenciesManager.UseBefore(_otherProject)

    def AddRule(self, description, output, command, depends, workingDirectory = "."):
        """
        Adds a new rule to the self.rules dictionary, using description as the key.
        """
        rule = Rule()
        rule.output = output
        rule.command = command
        rule.depends = depends
        rule.workingDirectory = workingDirectory
        self.rules[description] = rule

    def AddCustomCommand(self, _command):
        self.customCommands.append(_command)

    def RunCustomCommands(self):
        for command in self.customCommands:
            command(self)
            
    def AddTests(self, _listOfTests, _cxxTestProject, _enableWxWidgets = 0, _dependencies = None, _pch = ""):
        self.testsManager.AddTests(_listOfTests, _cxxTestProject, _enableWxWidgets, _dependencies, _pch)

    def GetTestProject(self):
        return self.testsManager.testProject
        
    def GetBuildFolder(self):
        if self.type == "third party":
            return self.context.GetThirdPartyBuildFolderByIndex(self.thirdPartyIndex)
        else:
            return self.pathsManager.GetBuildFolder()

    def GetBuildResultsFolder(self, _configurationName = "${CMAKE_CFG_INTDIR}"):
        return self.pathsManager.GetBuildResultsFolder(_configurationName)

    def GetCMakeListsFilename(self):
        return "%s/%s" % (self.context.GetBuildFolder(), self.pathsManager.cmakeListsSubpath)

    def GetSources(self):
        return self.compileManager.sources
        
    def GetSourceRootFolder(self):
        return self.pathsManager.GetSourceRootFolder()

    def MatchesFilter(self):
        for pattern in self.context.GetFilter():
            for string in self.categories:
                if csnUtility.Matches(string, pattern):
                    return True
        return False
    
    testProject = property(GetTestProject)
    sourceRootFolder = property(GetSourceRootFolder)

    def Dump(self):
        dump = dict()
        for project in self.dependenciesManager.GetProjects(_recursive=True, _includeSelf=True):
            dump[project.name] = { \
                "compiler" : project.compileManager.Dump(), \
                "dependencies" : project.dependenciesManager.Dump(), \
                "install" : project.installManager.Dump(), \
                "paths" : project.pathsManager.Dump() \
            }
        return dump

    def AddProperties(self, _property):
        for property in _property:
            self.properties.append(property)

    def GetPostCMakeTasks(self):
        return self.__postCMakeTasks
    
    def AddPostCMakeTasks(self, tasks):
        for task in tasks:
            self.__postCMakeTasks.append(task)
            
    def CreateHeader(self, _filename = None, _variables = None, _variablePrefix = None):
        """ 
        Creates a header file with input vars for the given project.
    
        @param project The calling project.
        @param filename The header file name (will be created in the projects' build folder), defaults to "CISTIBToolkit.h".
        @param variables Dictionary of variable/value pairs.  
        """
        projectNameClean = re.sub(r"[^A-Za-z0-9]", "_", self.name)
        if not _filename: 
            _filename = "%s.h" % projectNameClean
        path = "%s/%s" % (self.GetBuildFolder(), _filename)
        headerFile = open(path, 'w')
        
        # header
        guard = MakeValidIdentifier(_identifier = _filename, _toUpper = True)
        headerFile.write("#ifndef %s\n" % guard)
        headerFile.write("#define %s\n" % guard)
        headerFile.write("\n")
        headerFile.write("// Automatically generated file, do not edit.\n")
        headerFile.write("\n")
        
        # default variables
        if not _variablePrefix:
            _variablePrefix = MakeValidIdentifier(_identifier = self.name, _toUpper = True)
        headerFile.write("#define %s_FOLDER \"%s/..\"\n" % (_variablePrefix, self.GetSourceRootFolder()))
        headerFile.write("#define %s_BUILD_FOLDER \"%s\"\n" % (_variablePrefix, self.GetBuildFolder()))
        
        # input variables
        if _variables:
            headerFile.write("\n")
            for (key, value) in _variables:
                headerFile.write("#define %s \"%s\"\n" % (key, value))
        
        headerFile.write("\n")
        headerFile.write("#endif // %s\n" % guard)
        headerFile.close()


def SetCMakeInsertBeforeTarget(self, _file):
    # Empty function
    return

def SetCMakeInsertAfterTarget(self, _file):
    # Empty function
    return

def SetCMakeInsertBeginning(self, _file):
    # Empty function
    return
