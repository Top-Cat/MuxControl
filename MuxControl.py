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

class WizPageDeviceSetup(wxx.WizardPage):
    
    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)


class WizPageWelcome(wxx.WizardPage):
    
    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        text = wx.StaticText(self, label = 'Welcome!\r\nLooks like you haven\'t run this before')
        


class FirstTime(wxx.Wizard):
    
    def __init__(self, *args, **kwargs):
        wxx.Wizard.__init__(self, *args, **kwargs)
        self.addPage(WizPageWelcome(self))
        self.RunWizard(self.pages[0])



def main():

    app = wx.App(False)
    
    logging.info('Starting')
    
    try:
        settings = et.parse('settings3.xml')
        logging.info('Found settings')
    except IOError:
        logging.info('No settings found, running setup wizard')
        FirstTime(None)


if __name__ == '__main__':
    main()
