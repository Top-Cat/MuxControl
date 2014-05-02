#-------------------------------------------------------------------------------
# Name:        MuxControl
# Purpose:     Control software for various devices around YSTV
#
# Author:      Robert Walker
#
# Created:
# Copyright:   (c) Robert Walker 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------

import sys

sys.path.append('Devices/')

import logging

import wx
import wx.aui
import wx.lib.newevent
import wx.lib.scrolledpanel as scroll
import wx.gizmos as giz

import wxPythonExtra as wxx

import xml.etree.cElementTree as et

logging.basicConfig(filename = 'MuxControl.log', level = logging.DEBUG)


class WizPageDevice(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        sizer = wx.GridSizer(cols = 2)
        nameLabel = wx.StaticText(self, label = 'Device')
        name = wx.Choice(self)
        hostLabel = wx.StaticText(self, label = 'Host')
        host = wx.TextCtrl(self)
        portLabel = wx.StaticText(self, label = 'Port')
        port = wx.TextCtrl(self)
        sizer.AddMany([(nameLabel), (name), (hostLabel), (host),
                        (portLabel), (port)])
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)


class WizPageDeviceSetup(wxx.WizardPage):
    
    def onAdd(self, e):
        
        self.sizer.Insert(self.sizer.getIndex(e.GetEventObject()) - 1, WizPageDevice(self))
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
    
    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        devList = []
        self.sizer = wxx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label = 'Add the required devices')
        add = wx.Button(self, label = 'Add device')
        self.sizer.AddMany([(text), (add)])
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
        self.Bind(wx.EVT_BUTTON, self.onAdd, add)


class WizPageWelcome(wxx.WizardPage):
    
    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        text = wx.StaticText(self, label = 'Welcome!\r\nLooks like you haven\'t run this before')


class WizFirstTime(wxx.Wizard):
    
    def __init__(self, *args, **kwargs):
        wxx.Wizard.__init__(self, *args, **kwargs)
        self.addPage(WizPageWelcome(self))
        self.addPage(WizPageDeviceSetup(self))
        self.RunWizard(self.pages[0])



def main():
    
    availableDev = ['hub', 'mux', 'tarantula', 'txlight', 'tally']

    app = wx.App(False)
    
    logging.info('Starting')
    
    try:
        settings = et.parse('settings3.xml')
        logging.info('Found settings')
    except IOError:
        logging.info('No settings found, running setup wizard')
        WizFirstTime(None)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logging.error(e)
    logging.info('Exiting')
