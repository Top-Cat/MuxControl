import wx
import wx.aui
import logging

from events import *

import panels
import dialogs

class MainWindow(wx.Frame):

    """
    The main window everything else runs in"""

    def onPageChanged(self, e):
        if type(e) == wx.PyEvent:
            newSelection = e.GetEventObject().GetPage(
                                            e.GetEventObject().GetSelection())
        elif type(e) == wx.aui.AuiNotebookEvent:
            newSelection = e
        menuBar = self.GetMenuBar()
        menuBar.EnableTop(1, True)
        try:
            newSelection = self.mainBook.GetPage(self.mainBook.GetSelection())
            for option in self.buttonMenu.GetMenuItems():
                try:
                    if option.GetText()[1:] in newSelection.GetMenuOptions():
                        option.Enable(True)
                    else:
                        option.Enable(False)
                except AttributeError:
                    menuBar.EnableTop(1, False)
        except ValueError:
            for option in self.buttonMenu.GetMenuItems():
                option.Enable(False)

    def onConnectionSettings(self, e):
        settings = dialogs.SettingDialog(self.mainBook)
        settings.ShowModal()

    def onExit(self, e):

        """
        Gracefully close everything down"""

        self.updateThread.abort()
        self.Destroy()

    def onLabelChange(self, e):

        """
        Change the labels on the buttons by some dialgue or something.
        Can then refer to them in the outputs by their label instead
        of name"""

        source = self.GetMenuBar().FindItemById(e.GetId()).GetText()
        labels = LabelWindow(parent = self.mainBook.GetPage(
                                        self.mainBook.GetSelection()),
                                source = source)

    def onTally(self, e):

        tallyDialog = TallyDialog(self.mainBook)
        tallyDialog.ShowModal()

    def __init__(self, devList, settings, *args, **kwargs):

        """
        Main window to hold everything else in.
        dict devList    =   all the devices with information
        dict panelList  =   all the panels with information
        dict settings   =   other settings"""

        wx.Frame.__init__(self, None, size = (960, 786),
                                    title = 'Mux Control')
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, '&Exit', ' Quit the program')
        self.buttonMenu = wx.Menu()
        inputLabels = self.buttonMenu.Append(-1, '&Inputs',
                                        ' Change the input labels')
        outputLabels = self.buttonMenu.Append(-1, '&Outputs',
                                        ' Change the output labels')
        details = self.buttonMenu.Append(-1, '&Details',
                                                ' View the device information')
        tally = self.buttonMenu.Append(-1, '&Tally', 'Set the Tally config')
        connectionMenu = wx.Menu()
        settingsMenu = connectionMenu.Append(-1, '&Settings',
                                        ' Change the connection settings')
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(self.buttonMenu, '&Buttons')
        menuBar.Append(connectionMenu, '&Connection')
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.mainBook = MainBook(self, devList, settings)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onLabelChange, inputLabels)
        self.Bind(wx.EVT_MENU, self.onLabelChange, outputLabels)
        self.Bind(wx.EVT_MENU, self.onConnectionSettings, settingsMenu)
        self.Bind(wx.EVT_MENU, self.onTally, tally)
        self.mainBook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                                                        self.onPageChanged)
        self.onPageChanged(None)

        logging.debug('Loaded main window')
        self.Show()
##        self.updateThread = UpdateThread(self)


class MainBook(wx.aui.AuiNotebook):
    """
    Book to hold the tabs in the main window"""

    def __getitem__(self, index):
        if index < self.GetPageCount():
            return self.GetPage(index)
        else:
            raise IndexError

    def getTabs(self):

        return self.tabs

    def onNextStarterPage(self, e):

        wizard = NewLiveShowWizard(None)


    def __init__(self, parent, devList, settings, *args, **kwargs):
        wx.aui.AuiNotebook.__init__(self, parent, style = (wx.aui.AUI_NB_TOP |
                        wx.aui.AUI_NB_TOP | wx.aui.AUI_NB_TAB_SPLIT |
                        wx.aui.AUI_NB_TAB_MOVE | wx.aui.AUI_NB_SCROLL_BUTTONS))
        self.tabs = [(panels.DirectorPanel(self), 'Director Panel'),
                    (panels.ButtonPanel(self, settings, name = 'HubPanel',
                                dev = devList.find_device('hub'),
                                in_ = 16, out = 16),
                    'Hub Control'),
                    (panels.TransmissionPanel(self,
                                            name = 'TransmissionPanel',
                                            dev = devList.find_device('trans')),
                    'Transmission Light'),
                    (panels.TarantulaPanel(self, devList.find_device('tarantula'),
                                            devList.find_device('trans'),
                                            name = 'TarantulaPanel'),
                    'Tarantula Control'),
                    (panels.GfxPanel(parent = self, name = 'GfxPanel',
                                        dev = devList.find_device('CasparCG')),
                    'Graphics'),
                    (panels.ButtonPanel(self, settings,
                                        name = 'VikPanel',
                                        dev = devList.find_device('vik'),
                                        in_ = 16, out = 16),
                    'V1616 Control'),
                    ]
        self.AddPage(wx.Panel(self), '')
        for tab in self.tabs:
            for tabSetting in settings['panels']:
                tabSetting = settings['panels'][tabSetting]
                if tab[1] == tabSetting['name']:
                    self.AddPage(tab[0], tab[1])
                    if tabSetting['enabled'] == 'False':
                        self.RemovePage(self.GetPageCount() -1)
                    break
        self.SetSelection(1)
        self.RemovePage(0)


sources = ['cam 1', 'cam 1', 'cam 3', 'cam 4']
outputs = ['DaVE 1', 'DaVE 2', 'DaVE 3', 'DaVE 4']

class Basic_Window(wx.Frame):

    """
    Window with a set of input buttons for each mixer input.
    Will hopefully make stuff easier to use in a broadcast"""

    def get_labels(self):

        return self.settings['inputs'], self.settings['outputs']

        """sources = []
        for source in self.settings['inputs']:
            sources.append(source['label'])
        sinks = []
        for sink in self.settings['outputs']:
            sinks.append(self.devList.find_device(self.settings['device'][0].lower()).get_output_labels()[sink['mixer']][1])
        return sources, sinks"""


    def on_link(self, e):

        """
        e = EVT_DEVICE_LINK

        Tell the device to do the linking"""

        dev = self.devList.find_device(e.dev)
        for link in e.map_:
            dev.setConnection(*link)
        self.source_selection.update_buttons(map_ = e.map_, reverse = True)

    def on_update(self, e):

        dev = self.devList.find_device(e.dev)
        dev.acquire()
        dev.update()
        dev.release()
        self.source_selection.update_buttons(map_ = dev.get_map())

    def __init__(self, devList, settings, *args, **kwargs):
        wx.Frame.__init__(self, None, *args, size = (800, 600), **kwargs)
        self.devList = devList
        self.settings = settings
        self.source_selection = panels.Source_Selection(self, *self.get_labels())
        self.Bind(EVT_DEVICE_UPDATE, self.on_update)
        self.Bind(EVT_DEVICE_LINK, self.on_link)
        self.Show()
