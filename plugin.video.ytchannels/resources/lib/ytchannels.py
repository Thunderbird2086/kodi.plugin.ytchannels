
from six.moves import urllib
import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import os
from .functions import build_url, delete_database, get_folders, add_folder, remove_folder, get_channels, get_channel_id_from_uploads_id, add_channel, remove_channel, search_channel, search_channel_by_username, get_latest_from_channel, get_playlists, local_string

def ytchannels_main():

	my_addon = xbmcaddon.Addon()
	enable_playlists = my_addon.getSetting('enable_playlists')

	addon_handle = int(sys.argv[1])
	args = urllib.parse.parse_qs(sys.argv[2][1:])

	xbmcplugin.setContent(addon_handle, 'movies')

	mode = args.get('mode', None)

	show_adds=my_addon.getSetting('show_adds')
	
	addon_path = my_addon.getAddonInfo('path')
	folder_img = os.path.join(addon_path,'resources/img/folder.png')
	plus_img = os.path.join(addon_path,'resources/img/plus.png')
	playlist_img = os.path.join(addon_path,'resources/img/playlist.png')

	if mode is None:
		folders=get_folders()
	
		for i in range(len(folders)):
			if folders[i]!='Other':
				url = build_url({'mode': 'open_folder', 'foldername': '%s'%folders[i]})
				li = xbmcgui.ListItem('%s'%folders[i])
				li.setArt({'icon':folder_img})

				rem_uri = build_url({'mode': 'rem_folder', 'foldername': '%s'%str(folders[i])})
			
				add_uri = build_url({'mode': 'add_folder'})
				addch_uri = build_url({'mode': 'add_channel', 'foldername': 'Other'})
				li.addContextMenuItems([ (local_string(30000), 'RunPlugin(%s)'%rem_uri),
									(local_string(30001), 'RunPlugin(%s)'%add_uri),
									(local_string(30002), 'RunPlugin(%s)'%addch_uri)])

			

				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
									listitem=li,isFolder=True)
	
		channels=get_channels('Other')
		for i in range(len(channels)):
			url = build_url({'mode': 'open_channel', 'foldername': '%s'%str(channels[i][1]), 'page':'1'})
			li = xbmcgui.ListItem('%s'%channels[i][0])
			li.setArt({'icon':'%s'%channels[i][2]})

			rem_uri = build_url({'mode': 'rem_channel', 'channel_id': '%s'%str(channels[i][1])})
			add_uri = build_url({'mode': 'add_folder'})
			addch_uri = build_url({'mode': 'add_channel', 'foldername': 'Other'})
			li.addContextMenuItems([(local_string(30003), 'RunPlugin(%s)'%rem_uri),('Add folder', 'RunPlugin(%s)'%add_uri),
									(local_string(30002), 'RunPlugin(%s)'%addch_uri)])
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
								listitem=li,isFolder=True)
	
		if show_adds !='false' or (len(folders) == 0):

			url = build_url({'mode': 'add_folder', 'foldername': 'Add folder'})
			li = xbmcgui.ListItem('[COLOR green]%s[/COLOR]'%local_string(30001))
			li.setArt({'icon':plus_img})
			add_uri = build_url({'mode': 'add_folder'})
			addch_uri = build_url({'mode': 'add_channel', 'foldername': 'Other'})
			li.addContextMenuItems([(local_string(30001), 'RunPlugin(%s)'%add_uri),
									(local_string(30002), 'RunPlugin(%s)'%addch_uri)])

			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
									listitem=li,isFolder=True)
		
			url = build_url({'mode': 'add_channel', 'foldername': 'Other'})
			li = xbmcgui.ListItem('[COLOR green]%s[/COLOR] [COLOR blue]%s[/COLOR]'%(local_string(30009),local_string(30010)))
			li.setArt({'icon':plus_img})
			add_uri = build_url({'mode': 'add_folder'})
			addch_uri = build_url({'mode': 'add_channel', 'foldername': 'Other'})
			li.addContextMenuItems([(local_string(30001), 'RunPlugin(%s)'%add_uri),
									(local_string(30002), 'RunPlugin(%s)'%addch_uri)])
		
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
									listitem=li,isFolder=True)
							  

		xbmcplugin.endOfDirectory(addon_handle)

	elif mode[0]=='del_all':
		delete_database()
		xbmc.executebuiltin("Container.Refresh")

	elif mode[0]=='add_folder':
		keyboard = xbmc.Keyboard('', '%s:'%local_string(30011), False)
		keyboard.doModal()
	
		if keyboard.isConfirmed():
			folder_name = keyboard.getText()

			add_folder(folder_name)
		xbmc.executebuiltin("Container.Refresh")

	elif mode[0]=='open_folder':

		dicti=urllib.parse.parse_qs(sys.argv[2][1:])
		foldername=dicti['foldername'][0]
	
		channels=get_channels(foldername)
	
		for i in range(len(channels)):
			url = build_url({'mode': 'open_channel', 'foldername': '%s'%str(channels[i][1]), 'page':'1'})
			li = xbmcgui.ListItem('%s'%channels[i][0])
			li.setArt({'icon':'%s'%channels[i][2]})

			rem_uri = build_url({'mode': 'rem_channel', 'channel_id': '%s'%str(channels[i][1])})
			li.addContextMenuItems([ (local_string(30003), 'RunPlugin(%s)'%rem_uri)])
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
								listitem=li,isFolder=True)
			url = build_url({'mode': 'add_channel', 'foldername': '%s'%foldername})
			li = xbmcgui.ListItem('[COLOR green]%s[/COLOR] [COLOR blue]%s[/COLOR]'%(local_string(30009),local_string(30010)))
			li.setArt({'icon':plus_img})
		

		url = build_url({'mode': 'add_channel', 'foldername': '%s'%foldername})
		li = xbmcgui.ListItem('[COLOR green]%s[/COLOR] [COLOR blue]%s[/COLOR]'%(local_string(30009),foldername))
		li.setArt({'icon':plus_img})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
								listitem=li,isFolder=True)

		xbmcplugin.endOfDirectory(addon_handle)

	elif mode[0]=='open_channel':
		dicti=urllib.parse.parse_qs(sys.argv[2][1:])
		page=dicti['page'][0]

		id=dicti['foldername'][0]

		try:
			playlist=dicti['playlist'][0]
			if playlist=='yes':
				playlista=True
		except:
			playlista=False

	
		if not playlista and enable_playlists=='true':

			url = build_url({'mode': 'open_playlists', 'id':'%s'%id, 'page':'1'})
			li = xbmcgui.ListItem('[COLOR yellow]%s[/COLOR]'%local_string(30004))
			li.setArt({'icon':playlist_img})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
									listitem=li,isFolder=True)

		game_list=get_latest_from_channel(id,page)
		next_page=game_list[0]

		for i in range(1,len(game_list)):
			title=game_list[i][0]
			video_id=game_list[i][1]
			thumb=game_list[i][2]
			desc=game_list[i][3]
		
			uri='plugin://plugin.video.youtube/play/?video_id='+video_id
			li = xbmcgui.ListItem('%s'%title)
			li.setArt({'icon':thumb})
			li.setProperty('IsPlayable', 'true')
			li.setInfo('video', { 'genre': 'YouTube' } )

			xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li)#,isFolder=True)

		if next_page!='1':
			if playlista:
				uri = build_url({'mode': 'open_channel', 'foldername': '%s'%id, 'page' : '%s'%next_page ,'playlist':'yes'})
			else:
				uri = build_url({'mode': 'open_channel', 'foldername': '%s'%id, 'page' : '%s'%next_page })

			li = xbmcgui.ListItem('%s >>'%local_string(30005))
			li.setArt({'icon':thumb})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
			xbmcplugin.endOfDirectory(addon_handle)

	elif mode[0]=='open_playlists':
		dicti=urllib.parse.parse_qs(sys.argv[2][1:])
		id=dicti['id'][0]
		page=dicti['page'][0]
		channel_id=get_channel_id_from_uploads_id(id)
		playlists=get_playlists(channel_id,page)

		next_page=playlists[0]
		for i in range (1,len(playlists)):
			id=playlists[i][0]
			name=playlists[i][1]
			thumb=playlists[i][2]

			url = build_url({'mode': 'open_channel', 'foldername': '%s'%id, 'page':'1', 'playlist':'yes'})
			li = xbmcgui.ListItem('%s'%name)
			li.setArt({'icon':'%s'%thumb})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,isFolder=True)

		if next_page!='1':
		
			uri = build_url({'mode': 'open_playlists', 'id': '%s'%id, 'page' : '%s'%next_page ,'playlist':'yes'})
	  

			li = xbmcgui.ListItem('%s >>'%local_string(30005))
			li.setArt({'icon':thumb})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
			xbmcplugin.endOfDirectory(addon_handle)
	

	elif mode[0]=='add_channel':
		options=[local_string(30006),local_string(30007)]
		ind = xbmcgui.Dialog().select(local_string(30008), options)
		if ind==0:

			dicti=urllib.parse.parse_qs(sys.argv[2][1:])
			foldername=dicti['foldername'][0]
		
			keyboard = xbmc.Keyboard('', '%s:'%local_string(30012), False)
			keyboard.doModal()
		
			if keyboard.isConfirmed():
				channel_name = keyboard.getText()
		

				results=search_channel(channel_name)
			
				result_list=[]
				for i in range(len(results)):
					result_list+=[results[i][0]]
				dialog = xbmcgui.Dialog()
				index = dialog.select(local_string(30013), result_list)
				if index>-1:
					channel_uplid=results[index][1]
					channel_name=results[index][0]
					thumb=results[index][2]
					channel_id=results[index][3]

					add_channel(foldername,channel_name,channel_uplid,thumb)
		elif ind==1:
			dicti=urllib.parse.parse_qs(sys.argv[2][1:])
			foldername=dicti['foldername'][0]
		
			keyboard = xbmc.Keyboard('', '%s:'%local_string(30014), False)
			keyboard.doModal()
		
			if keyboard.isConfirmed():
				channel_name = keyboard.getText()
				help_list=search_channel_by_username(channel_name)
			
				if help_list== 'not found':
					xbmcgui.Dialog().ok(local_string(30099), '%s "%s" %s'%(local_string(30018),channel_name,local_string(30019)))
				else:
					channel_name=help_list[0]
					channel_id=help_list[1]
					thumb=help_list[2]
					add_channel(foldername,channel_name,channel_id,thumb)

		xbmc.executebuiltin("Container.Refresh")

	elif mode[0]=='rem_channel':
		dicti=urllib.parse.parse_qs(sys.argv[2][1:])
		channel_id=dicti['channel_id'][0]
		remove_channel(channel_id)
		xbmc.executebuiltin("Container.Refresh")

	elif mode[0]=='rem_folder':
		dicti=urllib.parse.parse_qs(sys.argv[2][1:])
		foldername=dicti['foldername'][0]
		remove_folder(foldername)
		xbmc.executebuiltin("Container.Refresh")

	elif mode[0]=='erase_all':
		ret = xbmcgui.Dialog().yesno(local_string(30015), local_string(30016)) 
	
		if ret:       

			delete_database()
			xbmcgui.Dialog().ok(local_string(30099), local_string(30017))
