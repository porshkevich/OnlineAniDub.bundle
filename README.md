About
=====

This is a plugin that creates a new channel in Plex Media Server to view content from the website AnimePlus.tv.  Includes search, bookmarks and the ability to browse alphabetically or by genre.

**Note:** The author of this plugin has no affiliation with AnimePlus.tv or the owners of the content that it hosts.

System Requirements
===================

- **Plex Media Server Version 0.9.8.4 or newer:**
	
	- Tested Working:
		- Windows
		- Mac OSX
		
	- Not Working:
		- ARM based NAS (Transcoding required)

- **Plex Clients:**

	- Tested Working:
		- Plex Media Centre / Home Theater
		- Android
		- Plex/Web
		- Windows 8
		- iOS
		- Roku
		
	- Not Tested:
		- Windows Phone
		- LG, Samsung Google Smart TV
		- Ouya

How To Install
==============

- [Download](https://github.com/TehCrucible/AnimePlus.bundle/archive/master.zip) the latest version of the plugin.

- Unzip and rename folder to "AnimePlus.bundle"

- Copy AnimePlus.bundle into the PMS plugins directory under your user account:
	- Windows 7, Vista, or Server 2008: C:\Users[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	- Windows XP, Server 2003, or Home Server: C:\Documents and Settings[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	- Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins

- Restart PMS

Known Issues
============

- Episode thumbnails are not consistent or slow to load.  This is due to AnimePlus.tv not displaying thumbs by default and needing to pull them from the video iframes.
- Multiple part episodes are not yet supported.

Roadmap
=======

- Multiple part episodes.

Changelog
=========

**1.00** - 10/01/14 - Initial release.
