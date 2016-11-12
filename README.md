DIRECTV DVR Control
===================

This plugin is an extremely simple plugin that uses the DIRECTV SHEF protocol to
enable Indigo to command your DIRECTV DVR or set-top box to change channels or
to simulate a button press on the standard remote. According to the protocol
specification document, it supports the H21 and HR20 and newer DVR models.
Others may work as well but we make no claims about those. In practice, we've
only tested it with the HR24-500 (the only one we have available).

Note: if you have the IP address wrong or your DVR is completely powered off, it
will take up to a minute before an error shows in the Event Log that a command
sent to the DVR couldn't be executed. Also, you must have your DVR configured
for external device access - see your setup menus to find the appropriate
setting, it should be called “External Access” or similar and the description
will mention external devices controlling your receiver.

Downloading for use
-------------------

Click the releases link above and download the release you’re interested in.
Once downloaded to your Indigo Server Mac, double-click the .indigoPlugin file
to install.

How to use
----------

See the [docs in the Indigo Domotics
wiki](http://wiki.indigodomo.com/doku.php?id=plugins:directvdvrcontrol) for
details.

Contributing
------------

If you want to contribute, just clone the repository in your account, make your
changes, and issue a pull request. Make sure that you describe the change you're
making thoroughly - this will help the repository managers accept your request
more quickly.

Terms
-----

Perceptive Automation is hosting this repository and will do minimal management.
Unless a pull request has no description or upon cursory observation has some
obvious issue, pull requests will be accepted without any testing by us. We may
choose to delegate commit privledges to other users at some point in the future.

We (Perceptive Automation) don't guarantee anything about this plugin - that
this plugin works or does what the description above states, so use at your own
risk. We will attempt to answer questions about the plugin but note that since
we don't use it regularly we may not have the answers. We certainly can't really
help with questions about your ISY.
