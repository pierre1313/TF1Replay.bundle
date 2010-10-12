# -*- coding: utf-8 -*-
# PMS plugin framework
from PMS import *

####################################################################################################
# Author : GuinuX. For any bug report, PM GuinuX on Plex Forums
# Version : 0.1
####################################################################################################
# ChangeLog : * 0.1 : Initial version 
####################################################################################################

VIDEO_PREFIX = "/video/tf1replay"
XML_CATALOG = "http://www.guinux.net/tf1.xml?v=1"
XML_DATA	= ""
NAME = "TF1 Replay"

PLUGIN_ID               = "com.plexapp.plugins.tf1eplay"
PLUGIN_REVISION         = 0.1
PLUGIN_UPDATES_ENABLED  = True

ART           = 'art-default.jpg'
ICON          = 'icon-default.png'

####################################################################################################

def Start():

	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("Coverflow", viewMode="Coverflow", mediaType="items")
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

	
	MediaContainer.art = R(ART)
	MediaContainer.title1 = NAME
	DirectoryItem.thumb = R(ICON)



def VideoMainMenu():
	global XML_DATA
	
	dir = MediaContainer(viewGroup="Coverflow")
	
	try:
		XML_DATA = HTTP.Request(XML_CATALOG, cacheTime=CACHE_1MINUTE * 30)
	except Ex.HTTPError, e:
		Log(NAME + " Plugin : " + str(e))
		return MessageContainer(NAME, "Erreur lors de la récupération du flux XML.")	
	except Exception, e :
		Log(NAME + " Plugin : " + str(e))
		return MessageContainer(NAME, "Erreur lors de la récupération du flux XML.")

    
	for category in XML.ElementFromString(XML_DATA).xpath("//category"):
		id = category.get('id')
		nom = category.get('name')
		thumb = category.get('picture')
		dir.Append(Function(DirectoryItem(ListShows, title = nom, thumb = R(thumb)), idCategorie = id, nomCategorie = nom))

	return dir


def ListShows(sender, idCategorie, nomCategorie):
	global XML_DATA

	dir = MediaContainer(viewGroup="Coverflow", title1 = NAME, title2 = nomCategorie)
	search = "//category[@id='" + idCategorie + "']/show"
	
	for show in XML.ElementFromString(XML_DATA).xpath(search):
		id = show.get('id')
		nom = show.get('name')
		thumb = show.get('thumb')
		if thumb == 'none':
			thumb = R('tf1.png')
			
		dir.Append(Function(DirectoryItem(ListEpisodes, title = nom, thumb = thumb), idShow = id, nomShow = nom))
		
	return dir
	
	
def ListEpisodes(sender, idShow, nomShow):
	global XML_DATA

	dir = MediaContainer(viewGroup="InfoList", title1 = NAME, title2 = nomShow)
	search = "//show[@id='" + idShow + "']/episode"
	for episode in XML.ElementFromString(XML_DATA).xpath(search):
		description	= ""
		nom			= episode.xpath("./title")[0].text
		duree		= episode.xpath("./duration")[0].text
		thumb		= episode.xpath("./picture")[0].text
		video		= episode.xpath("./video")[0].text
		desc		= episode.xpath("./description")[0].text 
		if desc:
			description = desc
		if duree:
			description	= description + "\n\nTemps : " + duree
		dir.Append(WebVideoItem(url = video, title = nom, subtitle = nomShow, summary = description, thumb = thumb))


	return dir
	