import wx
from wx.lib.docview import CommandProcessor, Command

def SetClipboardText(text):
    data_o = wx.TextDataObject()
    data_o.SetText(text)
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(data_o)
        wx.TheClipboard.Close()

def GetClipboardText():
    text_obj = wx.TextDataObject()
    rtext = ""
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        if wx.TheClipboard.GetData(text_obj):
            rtext = text_obj.GetText()
            wx.TheClipboard.Close()
    return rtext

class TextEditor(wx.Frame):
    def __init__(self, parent, title, size, *args, **kwargs):
        super(TextEditor, self).__init__(parent, title=title, size=size, *args, **kwargs)
        self.command_processor = CommandProcessor()
        # ========= MENU ===========================
        menuBar = wx.MenuBar()


        # --------- File Menu ----------------------
        fileMenu = wx.Menu()
        # newMenuItem = fileMenu.Append(wx.NewId(), "New", "New File")
        openMenuItem = fileMenu.Append(wx.ID_OPEN, "&Open...\tCTRL-O", "Open File")
        openMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN))
 
        # saveMenuItem = fileMenu.Append(wx.NewId(), "Save", "Save File")
        saveAsMenuItem = fileMenu.Append(wx.ID_SAVEAS, "Save As...", "Save File As...")
        saveAsMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS))

        # closeMenuItem = fileMenu.Append(wx.NewId(), "Close","Close file")
        quitMenuItem = fileMenu.Append(wx.ID_EXIT, "Quit","Quit the application")
        quitMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT))

        # --------- Edit Menu ----------------------
        editMenu = wx.Menu()
        copyMenuItem = editMenu.Append(wx.ID_COPY, "&Copy\tCTRL-C", "Copy")
        copyMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY))

        pasteMenuItem = editMenu.Append(wx.ID_PASTE, "&Paste\tCTRL-V", "Paste")
        pasteMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PASTE))

        cutMenuItem = editMenu.Append(wx.ID_CUT, "&Cut\tCTRL-X", "Cut")
        cutMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT))

        selectAllMenuItem = editMenu.Append(wx.ID_SELECTALL, "&Select All\tCTRL-A", "Select All")
        # selectAllMenuItem.SetBitmap(wx.ArtProvider.GetBitmap("gtk-select-all.png", wx.ART_SELECT))

        undoMenuItem = editMenu.Append(wx.ID_UNDO, "&Undo\tCTRL-Z", "Undo")
        undoMenuItem.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_UNDO))

        # --------- View Menu ----------------------
        viewMenu = wx.Menu()
        # darkMenuItem = viewMenu.Append(wx.NewId(), "Dark Mode", "Dark Mode")

        # --------- Help Menu ----------------------
        helpMenu = wx.Menu()
        helpMenuItem = helpMenu.Append(wx.ID_ABOUT, "About", "About")


        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(helpMenu, "&Help")

        self.Bind(wx.EVT_MENU, self.onQuit, quitMenuItem)
        # self.Bind(wx.EVT_MENU, self.onNew, newMenuItem)
        self.Bind(wx.EVT_MENU, self.onOpen, openMenuItem)
        # self.Bind(wx.EVT_MENU, self.onSave, saveMenuItem)
        self.Bind(wx.EVT_MENU, self.onSaveAs, saveAsMenuItem)
        self.Bind(wx.EVT_MENU, self.onQuit, quitMenuItem)



        self.Bind(wx.EVT_MENU, self.onCopy, copyMenuItem)  
        self.Bind(wx.EVT_MENU, self.onPaste, pasteMenuItem)   
        self.Bind(wx.EVT_MENU, self.onCut, cutMenuItem)
        self.Bind(wx.EVT_MENU, self.onSelectAll, selectAllMenuItem) 
        self.Bind(wx.EVT_MENU, self.onUndo, undoMenuItem)                

        self.SetMenuBar(menuBar)
        


        toolbar = self.CreateToolBar()
        openToolbarItem = toolbar.AddTool(wx.ID_OPEN, 'Open', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)))
        saveAsToolbarItem = toolbar.AddTool(wx.ID_SAVEAS, 'Save As', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS)))
        exitToolbarItem = toolbar.AddTool(wx.ID_EXIT, 'Quit', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT)))
        # toolbar.AddSeparator()
        copyToolbarItem = toolbar.AddTool(wx.ID_COPY, 'Copy', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY)))
        pasteToolbarItem = toolbar.AddTool(wx.ID_PASTE, 'Paste', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_PASTE)))
        cutToolbarItem = toolbar.AddTool(wx.ID_CUT, 'Cut', wx.Bitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT)))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.onOpen, openToolbarItem)
        # self.Bind(wx.EVT_TOOL, self.onOpen, exitToolbarItem)
        self.Bind(wx.EVT_TOOL, self.onSaveAs, exitToolbarItem)

        self.Bind(wx.EVT_TOOL, self.onCopy, copyToolbarItem)        
        self.Bind(wx.EVT_TOOL, self.onPaste, pasteToolbarItem)        
        self.Bind(wx.EVT_TOOL, self.onCut, cutToolbarItem)        
        # toolbar = self.CreateToolBar()
        # toolbar.AddTool(1, '', wx.Bitmap(wx.ART_FILE_OPEN))
        # toolbar.Realize()

        # ========= MAIN PANEL ===========================
        # panel = wx.Panel(self)
        # panel.SetBackgroundColour('#4f5049')

        # sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Text canvas - Where the writing is placed --
        self.tc = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER \
            |wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.BORDER_NONE)
        
        self.tc.Bind(wx.EVT_TEXT, self.onChange)  
        # self.tc.SetForegroundColour(wx.WHITE) # not working
        # self.tc.SetBackgroundColour((169,169,169))
        # self.tc.SetBackgroundColour((255,255,255))
        # sizer.Add(tc, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
        # panel.SetSizer(sizer)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Ready')


    # def onNew(self, event):
        # Isso ainda nao esta funcionando

        # panel = wx.Panel(self)
        # tc = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER \
        #     |wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.BORDER_NONE)
        # sizer.Add(tc, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
        # panel.SetSizer(sizer)
        # panel = 1


    def onExit(self, event):
       self.Close()

    # def onSave(self, event):
    #     # There is another way to save file with a method from txtCtrl 
    #     fh = open("result.txt", "w")
    #     fh.write(self.tc.GetValue())
    #     fh.close()
    #     event.Skip()

    def onSaveAs(self, event):
        with wx.FileDialog(self, "Save file", \
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    # self.doSaveData(file)
                    fh = open(pathname, "w")
                    fh.write(self.tc.GetValue())
                    fh.close()
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
        # event.Skip()

    def onOpen(self, event):
    # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open file", \
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    # self.doLoadDataOrWhatever(file)
                    fh = open(pathname,"r")
                    self.tc.SetValue(fh.read())
                    fh.close()
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def onQuit(self, e):
        self.Close()

    def onCopy(self, event):
        self.tc.GetStringSelection()

    def onPaste(self, event):
        self.tc.Paste()

    def onCut(self, event):
        self.tc.Cut()

    def onSelectAll(self, event):
        self.tc.SelectAll()

    def onUndo(self, event):
        print("undo")
        # self.tc.Undo()
        # self.command_processor.Undo()

    def onChange(self, event):
        print("change")
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = TextEditor(None, title='Editor de texto', size=(800,800))
        self.frame.Show();        
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()


# To Dos
    # 1 - 
    # 1.1 Add menus
    # New
    # Open ✓
    # Save
    # Save As ✓
    # Quit ✓
    # Confirm quit 
    # Check if the file was saved before quitting


    # 2 - 
    # 2.1 Add graphical menus
    # New
    # Open ✓
    # Save
    # Save As ✓
    # Quit
    # Copy ✓
    # Paste ✓
    # Cut ✓
    # Select All
    # Undo
    # Redo

    # 3 - 
    # 3.1 Change text canvas background color.
    # 3.2 Change text canvas font color.
    # 3.3 Text canvas is showing borders

    # 4 - Funcoes
    #     Copy -> ✓
    #     Paste -> ✓
    #     Cut -> ✓
    #     Select All -> ✓
    #     Undo
    #     Redo
    #     Find/Replace

    # 5 - Coloring special words
