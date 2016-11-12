#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

################################################################################
from datetime import datetime
import urllib
import socket
import simplejson as json

################################################################################
# Globals
################################################################################
keyText = {"power":"Power Toggle",
"poweron":"Power On",
"poweroff":"Power Off",
"play":"Play",
"pause":"Pause",
"rew":"Rewind",
"replay":"Replay",
"stop":"Stop",
"advance":"Advance",
"ffwd":"Fast Forward",
"record":"Record",
"guide":"Guide",
"active":"Active",
"list":"List",
"exit":"Exit",
"back":"Back",
"menu":"Menu",
"info":"Info",
"up":"Up",
"down":"Down",
"left":"Left",
"right":"Right",
"select":"Select",
"red":"Red",
"green":"Green",
"yellow":"Yellow",
"blue":"Blue",
"chanup":"Channel/Page Up",
"chandown":"Channel/Page Down",
"prev":"Previous Channel",
"0":"0",
"1":"1",
"2":"2",
"3":"3",
"4":"4",
"5":"5",
"6":"6",
"7":"7",
"8":"8",
"9":"9",
"enter":"Enter",
"dash":"Dash",
"format":"Format"}

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	# Class properties
	########################################

	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs): 
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		# list of scripts that are currently running - gives us a chance to kill them if we need to
		# when the plugin is asked to quit and it also allows us to get the output from the script
		# to insert into the variable if it's configured that way
		self.runningScripts = list()
		self.debug = False
		socket.setdefaulttimeout(5.0)
	
	########################################
	def validateActionConfigUi(self, valuesDict, typeId, devId):
		self.debugLog(u"Validating action config for type: " + typeId)
		errorsDict = indigo.Dict()
		ipAddress = valuesDict['address']
		clientMAC = valuesDict['clientMAC']
		if clientMAC == "":
			clientMac = "0"
		if typeId == "setChannel":
			try:
				channelNumber = int(valuesDict['channelNumber'])
				if channelNumber < 1 or channelNumber > 9999:
					raise
				valuesDict['description'] = "DIRECTV Control: change to channel " + str(channelNumber)
			except:
				errorsDict['channelNumber'] = 'invalid channel number, must be between 1 and 9999'
			try:
				minorNumber = int(valuesDict['minorNumber'])
				if minorNumber < 0 or minorNumber > 99:
					if minorNumber != 65535:
						raise
			except:
				errorsDict['minorNumber'] = 'invalid minor number, must be between 0 and 999 or 65535 (default)'
		else:
			if 'keyToPress' not in valuesDict:
				errorsDict['keyToPress'] = 'you must select a key to press'
			else:
				valuesDict['description'] = "DIRECTV Control: Press key " + keyText[valuesDict['keyToPress']]
		if len(errorsDict) > 0:
			return (False, valuesDict, errorsDict)
		return (True, valuesDict)
			
	########################################
	def sendKeyPress(self, action):
		address = action.props.get('address',"")
		clientMAC = action.props.get('clientMAC', "0")
		key = action.props.get('keyToPress', "")
		self.debugLog(u"sendKeyPress called: send %s to %s client %s" % (key,address, clientMAC))
		if (address == "") or (key == ""):
			self.errorLog(u"Key Press action misconfigured, no key sent")
		else:
			try:
				f = urllib.urlopen("http://%s:8080/remote/processKey?key=%s&clientAddr=%s" % (address, key, clientMAC))
				reply = json.load(f)
				statusCode = int(reply['status']['code'])
				if statusCode != 200:
					self.errorLog(u"Send key press action failed with status code: %i message: %s (probably an incorrect key name: '%s')" % (statusCode,reply['status']['msg'],key))
			except:
				self.errorLog(u"Send key press action failed with a network error - check your DVR to make sure it's on")
		
	########################################
	def setChannel(self, action):
		address = action.props.get('address',"")
		clientMAC = action.props.get('clientMAC', "0")
		channel = action.props.get('channelNumber', "")
		minor = action.props.get('minorNumber', "65535")
		self.debugLog(u"setChannel called: send channel %s minor %s to %s client %s" % (channel,minor,address, clientMAC))
		if (address == "") or (channel == "") or (minor == ""):
			self.errorLog(u"Go To Channel action misconfigured")
		else:
			try:
				f = urllib.urlopen("http://%s:8080/tv/tune?major=%s&minor=%s&clientAddr=%s" % (address, channel, minor, clientMAC))
				reply = json.load(f)
				statusCode = int(reply['status']['code'])
				if statusCode != 200:
					self.errorLog(u"Go To Channel action failed with status code: %i message: %s" % (statusCode,reply['status']['msg']))
			except:
				self.errorLog(u"Go To Channel action failed with a network error - check your DVR to make sure it's on")
	
