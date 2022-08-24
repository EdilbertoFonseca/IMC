# -*- coding: UTF-8 -*-

# Calculate your body mass with this add-on.
#Author: Edilberto Fonseca.
# Creation date: 08/11/2022.

import globalPluginHandler
import addonHandler
from scriptHandler import script
import gui
import wx

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the tools menu.
		self.calcular = self.toolsMenu.Append(-1, _('&Calculate your BMI'))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_onIMC, self.calcular)

	@script(gesture='kb:Windows+alt+I', description=_('BMI, This add-on calculates the body mass.'))
	def script_onIMC(self, gesture):
		# Tradutors: Dialog title Body Apple Index Calculation.
		self.dlg = DialogIMC(gui.mainFrame, _('Calculation of the Body Apple Index.'))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

class DialogIMC(wx.Dialog):

	def __init__(self, parent, title):
		self.title = title
		super(DialogIMC, self).__init__(parent, title=title)
		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		campoSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		labelHeight = wx.StaticText(panel, label=_('Enter your height: '))
		self.textHeight = wx.TextCtrl(panel, -1)

		labelWeight = wx.StaticText(panel, label=_('Enter your weight: '))
		self.textWeight = wx.TextCtrl(panel, -1)

		self.buttonCalc = wx.Button(panel, label=_('&Calculate'))
		self.Bind(wx.EVT_BUTTON, self.onCalc, self.buttonCalc)

		self.buttonClean= wx.Button(panel, label=_('C&lean'))
		self.Bind(wx.EVT_BUTTON, self.onClean, self.buttonClean)

		self.buttonClose = wx.Button(panel, wx.ID_CANCEL, label=_('&Close'))
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CANCEL)

		campoSizer.Add(labelHeight, 0, wx.ALL|wx.EXPAND, 5)
		campoSizer.Add(self.textHeight, 0, wx.ALL|wx.EXPAND, 5)
		campoSizer.Add(labelWeight, 0, wx.ALL|wx.EXPAND, 5)
		campoSizer.Add(self.textWeight, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonCalc, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonClean, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonClose, 0, wx.ALL|wx.EXPAND, 5)

		boxSizer.Add(campoSizer)
		boxSizer.Add(buttonSizer, wx.CENTER)
		panel.SetSizer(boxSizer)

	def onCalc(self, event):
		try:
			height = float(self.textHeight.GetValue())
			weight = float(self.textWeight.GetValue())
			calc = weight/(height**2)
		except:
			# Translators: Message displayed when fields are not filled.
			wx.MessageBox(_('Fill in all fields!'), _('Atention'))
			self.textHeight.SetFocus()

		calcFormat = '{:.1f}'.format(calc)
		if calc < 18.5:
			msg = _('Your BMI is {}, you are underweight!').format(calcFormat)
		elif 18.5 <= calc < 25:
			msg = _('Your BMI is {}, you are of normal weight!').format(calcFormat)
		elif 25 <= calc < 30:
			msg = _('Your BMI is {}, you are overweight!').format(calcFormat)
		elif 30 <= calc < 40:
			msg = _('Your BMI is {}, you are obese!').format(calcFormat)
		else:
			msg = _('Your BMI is {}, you are severely obese!').format(calcFormat)
		self.resut_dialog(msg=msg)

	def resut_dialog(self, msg):
		dlg = wx.TextEntryDialog(self, _('Resut'), _('Message'))
		dlg.SetValue(msg)
		self.textHeight.SetFocus()
		if dlg.ShowModal() == wx.ID_OK:
			self.textHeight.Clear()
			self.textWeight.Clear()
			self.textHeight.SetFocus()
		dlg.Destroy()

	def onClean(self, event):
		self.textHeight.Clear()
		self.textWeight.Clear()
		self.textHeight.SetFocus()

	def onClose(self, event):
		"""Close dialog."""
		self.Destroy()

