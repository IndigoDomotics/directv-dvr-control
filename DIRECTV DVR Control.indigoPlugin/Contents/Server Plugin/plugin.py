#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
"""
Plugin to control DirecTV Receivers and DVRs

Copyright (c) 2024, Perceptive Automation, LLC. All rights reserved.
http://www.indigodomo.com
"""
################################################################################
import requests
import socket  # TODO: is socket needed anymore?

try:
    import indigo
except ImportError:
    pass

################################################################################
# Globals
################################################################################
keyText = {
    "power": "Power Toggle",
    "poweron": "Power On",
    "poweroff": "Power Off",
    "play": "Play",
    "pause": "Pause",
    "rew": "Rewind",
    "replay": "Replay",
    "stop": "Stop",
    "advance": "Advance",
    "ffwd": "Fast Forward",
    "record": "Record",
    "guide": "Guide",
    "active": "Active",
    "list": "List",
    "exit": "Exit",
    "back": "Back",
    "menu": "Menu",
    "info": "Info",
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "select": "Select",
    "red": "Red",
    "green": "Green",
    "yellow": "Yellow",
    "blue": "Blue",
    "chanup": "Channel/Page Up",
    "chandown": "Channel/Page Down",
    "prev": "Previous Channel",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "enter": "Enter",
    "dash": "Dash",
    "format": "Format"
}

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    # Class properties
    ########################################

    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        # list of scripts that are currently running - gives us a chance to kill them if we need to when the plugin is
        # asked to quit, and it also allows us to get the output from the script to insert into the variable if it's
        # configured that way
        # self.runningScripts = []  # TODO: this doesn't seem to be used anywhere.
        self.debug = False
        socket.setdefaulttimeout(5.0)

    ########################################
    def validate_action_config_ui(self, values_dict: indigo.Dict, type_id: str, dev_id: int):
        self.debugLog(f"Validating action config for type: {type_id}")
        errors_dict: indigo.Dict = indigo.Dict()
        ip_address: str = values_dict['address']
        client_mac: str = values_dict['clientMAC']
        if client_mac == "":
            client_mac = "0"
        if type_id == "setChannel":
            try:
                channel_number = int(values_dict['channelNumber'])
                if channel_number < 1 or channel_number > 9999:
                    raise Exception
                values_dict['description'] = f"DIRECTV Control: change to channel {channel_number}"
            except:
                errors_dict['channelNumber'] = 'invalid channel number, must be between 1 and 9999'
            try:
                minor_number = int(values_dict['minorNumber'])
                if minor_number < 0 or minor_number > 99:
                    if minor_number != 65535:
                        raise Exception
            except:
                errors_dict['minorNumber'] = 'invalid minor number, must be between 0 and 999 or 65535 (default)'
        else:
            if 'keyToPress' not in values_dict:
                errors_dict['keyToPress'] = 'you must select a key to press'
            else:
                values_dict['description'] = f"DIRECTV Control: Press key {keyText[values_dict['keyToPress']]}"
        if len(errors_dict) > 0:
            return (False, values_dict, errors_dict)
        return (True, values_dict)

    ########################################
    def sendKeyPress(self, action):
        address: str    = action.props.get('address', "")
        client_mac: str = action.props.get('clientMAC', "0")
        key: str        = action.props.get('keyToPress', "")
        self.debugLog(f"sendKeyPress called: send {key} to {address} client {client_mac}")
        if (address == "") or (key == ""):
            self.errorLog("Key Press action misconfigured, no key sent")
        else:
            try:
                url = f"http://{address}:8080/remote/processKey?key={key}&clientAddr={client_mac}"
                f = requests.get(url, timeout=5)
                reply = f.json()
                status_code = int(reply['status']['code'])
                if status_code != 200:
                    self.errorLog(
                        f"Send key press action failed with status code: {status_code:d} message: "
                        f"{reply['status']['msg']} (probably an incorrect key name: '{key}')"
                    )
            except:
                self.errorLog("Send key press action failed with a network error - check your DVR to make sure it's on")

    ########################################
    def setChannel(self, action):
        address: str    = action.props.get('address', "")
        channel: str    = action.props.get('channelNumber', "")
        client_mac: str = action.props.get('clientMAC', "0")
        minor: str      = action.props.get('minorNumber', "65535")
        self.debugLog(f"setChannel called: send channel {channel} minor {minor} to {address} client {client_mac}")
        if (address == "") or (channel == "") or (minor == ""):
            self.errorLog("Go To Channel action misconfigured")
        else:
            try:
                url = f"http://{address}:8080/tv/tune?major={channel}&minor={minor}&clientAddr={client_mac}"
                f = requests.get(url, timeout=5)
                reply = f.json()
                status_code = int(reply['status']['code'])
                if status_code != 200:
                    self.errorLog(
                        f"Go To Channel action failed with status code: {status_code:d} message: "
                        f"{reply['status']['msg']}"
                    )
            except:
                self.errorLog("Go To Channel action failed with a network error - check your DVR to make sure it's on")
