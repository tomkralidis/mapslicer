#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: Cleaning the code, refactoring before 1.0 publishing

import os, sys

import wx

# Under Windows set the GDAL variables to local directories in the py2exe distribution
exepath = os.getcwd()
if hasattr(sys, "frozen") or sys.executable.find('MapTiler.app') != -1:
	exepath = os.path.dirname(sys.executable)

if sys.platform in ['win32','win64'] and os.path.exists(os.path.join( exepath, "gdaldata" )):
	os.environ['GDAL_DATA'] = os.path.join( exepath, "gdaldata" )
	os.environ['GDAL_DRIVER_PATH'] = os.path.join( exepath, "gdalplugins" )

# Mac can have GDAL.framework in the application bundle or in the /Library/Frameworks
if sys.platform == 'darwin':
	frameworkpath = exepath[:(exepath.find('MapTiler.app')+12)]+'/Contents/Frameworks'
	if not os.path.exists( os.path.join(frameworkpath, "GDAL.framework" )):
		frameworkpath = "/Library/Frameworks"
	os.environ['PROJ_LIB'] = os.path.join( frameworkpath, "PROJ.framework/Resources/proj/" )
	os.environ['GDAL_DATA'] = os.path.join( frameworkpath, "GDAL.framework/Resources/gdal/" )
	os.environ['GDAL_DRIVER_PATH'] = os.path.join( frameworkpath, "GDAL.framework/PlugIns/" )
	sys.path.insert(0, os.path.join( frameworkpath, "GDAL.framework/Versions/Current/Python/site-packages/" ))

# Other systems need correctly installed GDAL libraries

import maptiler
__version__ = maptiler.version

class MapTilerApp(wx.App):
	
	def OnInit(self):
		wx.InitAllImageHandlers()
		self.main_frame = maptiler.MainFrame(None, -1, "")
		self.SetTopWindow(self.main_frame)
		return True
		
	def MacOpenFile(self, filename):
		self.main_frame._add(filename)
		
	def Show(self):
		self.main_frame.Show()

if __name__ == "__main__":
	
	# TODO: GetText
	#import gettext
	#gettext.install("maptiler")

	# TODO: Parse command line arguments:
	# for both batch processing and initialization of the GUI

	#wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic",0)
	app = MapTilerApp(False)

	#spath = wx.StandardPaths.Get()
	#print spath.GetExecutablePath()
	
	try:
		from osgeo import gdal
	except ImportError:
		# TODO: Platform specific error messages - are part of the GUI...
		if sys.platform == 'darwin':
			wx.MessageBox("""GDAL 1.6 framework is not found in your system!\n
Please install GDAL framework from the website:
http://www.kyngchaos.com/software:frameworks""", "Error: GDAL Framework not found!", wx.ICON_ERROR)
			import webbrowser
			webbrowser.open_new("http://www.kyngchaos.com/software:frameworks#gdal")
			sys.exit(1)
		elif sys.platform in ['win32','win64']:
			wx.MessageBox("""GDAL 1.6 library is not found in your system!\n
If you used installer then please report this problem as issue at:
http://code.google.com/p/maptiler/issues""", "Error: GDAL library not found!", wx.ICON_ERROR)
			sys.exit(1)
		elif sys.platform == 'linux':
			wx.MessageBox("""GDAL 1.6 library is not found in your system!\n
Please install it as a package in your distribution or from the source code:
http://trac.osgeo.org/gdal/wiki/BuildHints""", "Error: GDAL library not found!", wx.ICON_ERROR)
			sys.exit(1)
		print "GDAL library not available - please install GDAL and it's python module!"

	wx.MessageBox("""This is a development version of MapTiler application.
It has known bugs and limits.\n
It is not for production use but for testing and preview!""", "MapTiler Alpha version (%s)" % __version__, wx.ICON_INFORMATION)
	app.Show()
	app.MainLoop()
