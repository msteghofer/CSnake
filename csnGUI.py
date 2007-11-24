#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sat Sep 15 14:23:13 2007 from D:\Users\Maarten\Projects\Gimias\Prog\GIMIAS.cmake\GBuild\csnGUI.wxg

import wx
import csnGUIHandler
import pickle
import os.path
import sys

thisFolder = "%s" % (os.path.dirname(__file__))
thisFolder = thisFolder.replace("\\", "/")
recentFilesFilename = "%s/recentFiles" % thisFolder

class RedirectText:
    def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

    def write(self,string):
		self.out.WriteText(string)

class CSnakeGUIRecentFiles:
    def __init__(self):    
        self.source2BinaryFolder = dict()
        self.source2InstallFolder = dict()
        self.thirdPartySource2BinaryFolder = dict()
        self.projectFolder = ""
        self.rootFolder = ""
        self.thirdPartyRootFolder = ""
        self.instance = ""
    
class CSnakeGUIFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CSnakeGUIFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panelThirdParty = wx.Panel(self, -1)
        self.panelSource = wx.Panel(self, -1)
        self.panelProjectAndInstance = wx.Panel(self, -1)
        self.lblProjectPath = wx.StaticText(self.panelProjectAndInstance, -1, "Project Path\n")
        self.txtProjectPath = wx.TextCtrl(self.panelProjectAndInstance, -1, "")
        self.btnSelectProjectPath = wx.Button(self.panelProjectAndInstance, -1, "...")
        self.labelInstance = wx.StaticText(self.panelProjectAndInstance, -1, "Instance")
        self.txtInstance = wx.TextCtrl(self.panelProjectAndInstance, -1, "")
        self.label_1 = wx.StaticText(self.panelSource, -1, "Root Folder\n")
        self.txtRootFolder = wx.TextCtrl(self.panelSource, -1, "")
        self.btnSelectRootFolder = wx.Button(self.panelSource, -1, "...")
        self.label_1_copy = wx.StaticText(self.panelSource, -1, "Bin Folder\n")
        self.txtBinFolder = wx.TextCtrl(self.panelSource, -1, "")
        self.btnSelectBinFolder = wx.Button(self.panelSource, -1, "...")
        self.label_2 = wx.StaticText(self.panelSource, -1, "Install Folder\n")
        self.txtInstallFolder = wx.TextCtrl(self.panelSource, -1, "")
        self.btnSelectInstallFolder = wx.Button(self.panelSource, -1, "...")
        self.label_1_copy_1 = wx.StaticText(self.panelThirdParty, -1, "ThirdParty Root\n Folder")
        self.txtThirdPartyRootFolder = wx.TextCtrl(self.panelThirdParty, -1, "")
        self.btnSelectThirdPartyRootFolder = wx.Button(self.panelThirdParty, -1, "...")
        self.label_1_copy_copy = wx.StaticText(self.panelThirdParty, -1, "ThirdParty Bin Folder\n")
        self.txtThirdPartyBinFolder = wx.TextCtrl(self.panelThirdParty, -1, "")
        self.btnSelectThirdPartyBinFolder = wx.Button(self.panelThirdParty, -1, "...")
        self.textLog = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
        self.btnDoAction = wx.Button(self, -1, "Do -->")
        self.cmbAction = wx.ComboBox(self, -1, choices=["Create CMake files and run CMake", "Only create CMake files", "Install files to Bin Folder", "Configure ThirdParty Folder"], style=wx.CB_DROPDOWN)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.OnTypingProjectPath, self.txtProjectPath)
        self.Bind(wx.EVT_BUTTON, self.OnSelectProjectPath, self.btnSelectProjectPath)
        self.Bind(wx.EVT_TEXT, self.OnTypingRootFolder, self.txtInstance)
        self.Bind(wx.EVT_TEXT, self.OnTypingRootFolder, self.txtRootFolder)
        self.Bind(wx.EVT_BUTTON, self.OnSelectProjectRoot, self.btnSelectRootFolder)
        self.Bind(wx.EVT_BUTTON, self.OnSelectBinFolder, self.btnSelectBinFolder)
        self.Bind(wx.EVT_BUTTON, self.OnSelectInstallFolder, self.btnSelectInstallFolder)
        self.Bind(wx.EVT_TEXT, self.OnTypingThirdPartyRootFolder, self.txtThirdPartyRootFolder)
        self.Bind(wx.EVT_BUTTON, self.OnSelectProjectRoot, self.btnSelectThirdPartyRootFolder)
        self.Bind(wx.EVT_BUTTON, self.OnSelectBinFolder, self.btnSelectThirdPartyBinFolder)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDo, self.btnDoAction)
        # end wxGlade
        
        self.handler = csnGUIHandler.Handler()
        redir=RedirectText(self.textLog)
        sys.stdout=redir
        sys.stderr=redir
        print "Tip: it is convenient to have the Project Root and Bin Folder as subfolders of a common parent folder. For example,\n"
        print "Project Root = <somepath>/TextEditorProject/source, \n"
        print "Bin Folder = <somepath>/TextEditorProject/bin. \n"
        print "Project Folder = <somepath>/TextEditorProject/source/TextEditorGUI.\n"
        
        self.commandCounter = 0

    def __set_properties(self):
        # begin wxGlade: CSnakeGUIFrame.__set_properties
        self.SetTitle("CSnake GUI")
        self.SetSize((500, 459))
        self.txtProjectPath.SetMinSize((-1, -1))
        self.txtProjectPath.SetToolTipString("The folder containing the target (dll, lib or exe) you wish to build.")
        self.btnSelectProjectPath.SetMinSize((30, -1))
        self.txtInstance.SetMinSize((-1, -1))
        self.txtInstance.SetToolTipString("Optional field for the root of the source tree that contains the Project Folder. CSnake will search this source tree for other projects.")
        self.panelProjectAndInstance.SetBackgroundColour(wx.Colour(192, 191, 255))
        self.txtRootFolder.SetMinSize((-1, -1))
        self.txtRootFolder.SetToolTipString("Optional field for the root of the source tree that contains the Project Folder. CSnake will search this source tree for other projects.")
        self.btnSelectRootFolder.SetMinSize((30, -1))
        self.txtBinFolder.SetMinSize((-1, -1))
        self.txtBinFolder.SetToolTipString("This is the location where CSnake will generate the \"make files\".")
        self.btnSelectBinFolder.SetMinSize((30, -1))
        self.txtInstallFolder.SetMinSize((-1, -1))
        self.txtInstallFolder.SetToolTipString("This is the location where CSnake will generate the \"make files\".")
        self.btnSelectInstallFolder.SetMinSize((30, -1))
        self.txtThirdPartyRootFolder.SetMinSize((-1, -1))
        self.txtThirdPartyRootFolder.SetToolTipString("Optional field for the root of the source tree that contains the Project Folder. CSnake will search this source tree for other projects.")
        self.btnSelectThirdPartyRootFolder.SetMinSize((30, -1))
        self.txtThirdPartyBinFolder.SetMinSize((-1, -1))
        self.txtThirdPartyBinFolder.SetToolTipString("This is the location where CSnake will generate the \"make files\".")
        self.btnSelectThirdPartyBinFolder.SetMinSize((30, -1))
        self.panelThirdParty.SetBackgroundColour(wx.Colour(192, 191, 255))
        self.cmbAction.SetSelection(0)
        # end wxGlade
        self.recentFiles = CSnakeGUIRecentFiles()
        if os.path.exists( recentFilesFilename ):
            f = open(recentFilesFilename, 'r')
            self.recentFiles = pickle.load(f)
            f.close()
            self.txtProjectPath.SetValue(self.recentFiles.projectFolder)
            self.txtRootFolder.SetValue(self.recentFiles.rootFolder)
            self.txtThirdPartyRootFolder.SetValue(self.recentFiles.thirdPartyRootFolder)
            self.txtBinFolder.SetValue( self.recentFiles.source2BinaryFolder[self.txtRootFolder.GetValue()] )
            self.txtInstallFolder.SetValue( self.recentFiles.source2InstallFolder[self.txtRootFolder.GetValue()] )
            self.txtThirdPartyBinFolder.SetValue( self.recentFiles.thirdPartySource2BinaryFolder[self.txtThirdPartyRootFolder.GetValue()] )
            self.txtInstance.SetValue(self.recentFiles.instance)

    def __do_layout(self):
        # begin wxGlade: CSnakeGUIFrame.__do_layout
        boxSettings = wx.BoxSizer(wx.VERTICAL)
        boxBuildProject = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        boxThirdPartyBinFolder = wx.BoxSizer(wx.HORIZONTAL)
        boxThirdPartyRoot = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        boxBinFolder_copy = wx.BoxSizer(wx.HORIZONTAL)
        boxBinFolder = wx.BoxSizer(wx.HORIZONTAL)
        boxRootFolder = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        boxRootFolder_copy = wx.BoxSizer(wx.HORIZONTAL)
        boxProjectPath = wx.BoxSizer(wx.HORIZONTAL)
        boxProjectPath.Add(self.lblProjectPath, 0, wx.RIGHT, 5)
        boxProjectPath.Add(self.txtProjectPath, 2, wx.FIXED_MINSIZE, 0)
        boxProjectPath.Add(self.btnSelectProjectPath, 0, 0, 0)
        sizer_3.Add(boxProjectPath, 0, wx.EXPAND, 0)
        boxRootFolder_copy.Add(self.labelInstance, 0, wx.RIGHT, 5)
        boxRootFolder_copy.Add(self.txtInstance, 2, wx.FIXED_MINSIZE, 0)
        sizer_3.Add(boxRootFolder_copy, 1, wx.EXPAND, 0)
        self.panelProjectAndInstance.SetSizer(sizer_3)
        boxSettings.Add(self.panelProjectAndInstance, 0, wx.EXPAND, 0)
        boxRootFolder.Add(self.label_1, 0, wx.RIGHT, 5)
        boxRootFolder.Add(self.txtRootFolder, 2, wx.FIXED_MINSIZE, 0)
        boxRootFolder.Add(self.btnSelectRootFolder, 0, 0, 0)
        sizer_1.Add(boxRootFolder, 1, wx.EXPAND, 0)
        boxBinFolder.Add(self.label_1_copy, 0, wx.RIGHT, 5)
        boxBinFolder.Add(self.txtBinFolder, 2, wx.FIXED_MINSIZE, 0)
        boxBinFolder.Add(self.btnSelectBinFolder, 0, 0, 0)
        sizer_1.Add(boxBinFolder, 1, wx.EXPAND, 0)
        boxBinFolder_copy.Add(self.label_2, 0, wx.RIGHT, 5)
        boxBinFolder_copy.Add(self.txtInstallFolder, 2, wx.FIXED_MINSIZE, 0)
        boxBinFolder_copy.Add(self.btnSelectInstallFolder, 0, 0, 0)
        sizer_1.Add(boxBinFolder_copy, 1, wx.EXPAND, 0)
        self.panelSource.SetSizer(sizer_1)
        boxSettings.Add(self.panelSource, 0, wx.EXPAND, 0)
        boxThirdPartyRoot.Add(self.label_1_copy_1, 0, wx.RIGHT, 5)
        boxThirdPartyRoot.Add(self.txtThirdPartyRootFolder, 2, wx.FIXED_MINSIZE, 0)
        boxThirdPartyRoot.Add(self.btnSelectThirdPartyRootFolder, 0, 0, 0)
        sizer_2.Add(boxThirdPartyRoot, 1, wx.EXPAND, 0)
        boxThirdPartyBinFolder.Add(self.label_1_copy_copy, 0, wx.RIGHT, 5)
        boxThirdPartyBinFolder.Add(self.txtThirdPartyBinFolder, 2, wx.FIXED_MINSIZE, 0)
        boxThirdPartyBinFolder.Add(self.btnSelectThirdPartyBinFolder, 0, 0, 0)
        sizer_2.Add(boxThirdPartyBinFolder, 1, wx.EXPAND, 0)
        self.panelThirdParty.SetSizer(sizer_2)
        boxSettings.Add(self.panelThirdParty, 0, wx.EXPAND, 0)
        boxSettings.Add(self.textLog, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        boxBuildProject.Add(self.btnDoAction, 0, 0, 0)
        boxBuildProject.Add(self.cmbAction, 2, 0, 0)
        boxSettings.Add(boxBuildProject, 0, wx.EXPAND, 0)
        self.SetSizer(boxSettings)
        self.Layout()
        # end wxGlade

    def OnSelectProjectRoot(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        dlg = wx.DirDialog(None, "Select Project Root Folder")
        if dlg.ShowModal() == wx.ID_OK:
            txtProjectRoot.SetValue(dlg.GetPath())

    def OnSelectBinFolder(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        dlg = wx.DirDialog(None, "Select Binary Folder")
        if dlg.ShowModal() == wx.ID_OK:
            txtBinFolder.SetValue(dlg.GetPath())

    def OnStartNewProject(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        mapping = dict()
        mapping["Dll"] = "dll"
        mapping["Static library"] = "library"
        mapping["Executable"] = "executable"
    	csnGUIHandler.CreateCSnakeProject(self.txtProjectPath.GetValue(), self.txtProjectRoot.GetValue(), self.txtNewProjectName.GetValue(), mapping[self.cmbNewProjectType.GetValue()])

    def StoreRecentFilesData(self):
        self.recentFiles.source2BinaryFolder[ self.txtRootFolder.GetValue() ] = self.txtBinFolder.GetValue()
        self.recentFiles.source2InstallFolder[ self.txtRootFolder.GetValue() ] = self.txtInstallFolder.GetValue()
        self.recentFiles.thirdPartySource2BinaryFolder[ self.txtThirdPartyRootFolder.GetValue() ] = self.txtThirdPartyBinFolder.GetValue()
        self.recentFiles.projectFolder = self.txtProjectPath.GetValue()
        self.recentFiles.rootFolder = self.txtRootFolder.GetValue()
        self.recentFiles.thirdPartyRootFolder = self.txtThirdPartyRootFolder.GetValue()
        self.recentFiles.instance = self.txtInstance.GetValue()
        f = open(recentFilesFilename, 'w')
        pickle.dump(self.recentFiles, f)
        f.close()
    
    def OnTypingProjectPath(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        event.Skip()

    def OnTypingRootFolder(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        if self.recentFiles.source2BinaryFolder.has_key(self.txtRootFolder.GetValue()):
            self.txtBinFolder.SetValue( self.recentFiles.source2BinaryFolder[self.txtRootFolder.GetValue()] )
        if self.recentFiles.source2InstallFolder.has_key(self.txtRootFolder.GetValue()):
            self.txtInstallFolder.SetValue( self.recentFiles.source2InstallFolder[self.txtRootFolder.GetValue()] )

    def OnTypingThirdPartyRootFolder(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        if self.recentFiles.thirdPartySource2BinaryFolder.has_key(self.txtThirdPartyRootFolder.GetValue()):
            self.txtThirdPartyBinFolder.SetValue( self.recentFiles.thirdPartySource2BinaryFolder[self.txtThirdPartyRootFolder.GetValue()] )

    def OnSelectProjectPath(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        dlg = wx.FileDialog(None, "Select Python Project Module")
        if dlg.ShowModal() == wx.ID_OK:
            pass

    def OnButtonDo(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        print "\n--- Working, patience please... (command counter: %s) ---" % self.commandCounter
        self.StoreRecentFilesData()
        configureProject = self.cmbAction.GetValue() in ("Only create CMake files", "Create CMake files and run CMake")
        alsoRunCMake = self.cmbAction.GetValue() in ("Create CMake files and run CMake")
            
        if configureProject:
            self.handler.ConfigureProjectToBinFolder(
                self.txtProjectPath.GetValue().replace("\\", "/"), 
                self.txtInstance.GetValue(),
                self.txtRootFolder.GetValue().replace("\\", "/"),
                self.txtBinFolder.GetValue().replace("\\", "/"),
                self.txtInstallFolder.GetValue().replace("\\", "/"),
                self.txtThirdPartyRootFolder.GetValue().replace("\\", "/"),
                self.txtThirdPartyBinFolder.GetValue().replace("\\", "/"),
                alsoRunCMake)

        copyDlls = self.cmbAction.GetValue() in ("Install files to Bin Folder")
        if copyDlls:
            self.handler.InstallThirdPartyBinariesToBinFolder(
                self.txtProjectPath.GetValue().replace("\\", "/"), 
                self.txtInstance.GetValue(),
                self.txtRootFolder.GetValue().replace("\\", "/"),
                self.txtBinFolder.GetValue().replace("\\", "/"),
                self.txtThirdPartyRootFolder.GetValue().replace("\\", "/"),
                self.txtThirdPartyBinFolder.GetValue().replace("\\", "/"))
                
        configureThirdPartyFolder = self.cmbAction.GetValue() in ("Configure ThirdParty Folder")
        if( configureThirdPartyFolder ):
            self.handler.ConfigureThirdPartyFolder(
                self.txtThirdPartyRootFolder.GetValue().replace("\\", "/"),
                self.txtThirdPartyBinFolder.GetValue().replace("\\", "/"))

        print "--- Done (command counter: %s) ---" % self.commandCounter
        self.commandCounter += 1
                
    def OnSelectInstallFolder(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        dlg = wx.DirDialog(None, "Select Install Folder")
        if dlg.ShowModal() == wx.ID_OK:
            txtInstallFolder.SetValue(dlg.GetPath())

# end of class CSnakeGUIFrame


class CSnakeGUIApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frmCSnakeGUI = CSnakeGUIFrame(None, -1, "")
        self.SetTopWindow(frmCSnakeGUI)
        frmCSnakeGUI.Show()
        return 1

# end of class CSnakeGUIApp

if __name__ == "__main__":
    app = CSnakeGUIApp(0)
    app.MainLoop()
