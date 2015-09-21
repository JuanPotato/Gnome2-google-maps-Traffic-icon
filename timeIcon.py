#!/usr/bin/env python

import threading, multiprocessing, time, gtk, json, requests

def calculate(origins, destinations, mode="driving", language="en-US"):
	payload = {
		'departure_time': time.time() + 5
		'destinations': destinations,
		'language': language,
		'origins': origins,
		'mode': mode,
		'signature': "", #ADD SIGNATURE IN THE QUOTES
		'client': "", #ADD CLIENT ID THING IN THE QUOTES
		}

	r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=payload).json()
	
	try:
		if "duration_in_traffic" in r["rows"][0]["elements"][0]:
			return r["rows"][0]["elements"][0]["duration"]
		else:
			return r["rows"][0]["elements"][0]["duration_in_traffic"]
	except:
		return

def updateTimes(icon, seconds):
	next_call = time.time()
	while True:
		data = json.load(open("options.json"))
		value = calculate(data["from"], data["to"])
		print(value)
		if value:
			if value["value"] < 300:
				icon.set_from_file("green.png")
			elif value["value"] < 600:
				icon.set_from_file("yellow.png")
			else:
				icon.set_from_file("red.png")
		else:
			icon.set_from_file("grey.png")
		icon.set_tooltip_text(value["text"] or "ERR")
		next_call = next_call + seconds
		time.sleep(next_call - time.time())
 
def message(data=None):
	#Function to display messages to the user."
	
	msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
	msg.run()
	msg.destroy()
 
def open_app(data=None):
	message(data)
 
def close_app(data=None):
	message(data)
	gtk.main_quit()
 
def make_menu(event_button, event_time, data=None):
	menu = gtk.Menu()
	open_item = gtk.MenuItem("Open App")
	close_item = gtk.MenuItem("Close App")
	
	#Append the menu items  
	menu.append(open_item)
	menu.append(close_item)
	#add callbacks
	open_item.connect_object("activate", open_app, "Open App")
	close_item.connect_object("activate", close_app, "Close App")
	#Show the menu items
	open_item.show()
	close_item.show()
	
	#Popup the menu
	menu.popup(None, None, None, event_button, event_time)
 
def on_right_click(data, event_button, event_time):
	make_menu(event_button, event_time)
 
def on_left_click(event):
	message("Status Icon Left Clicked")
 
if __name__ == '__main__':
	gtk.gdk.threads_init()
	icon = gtk.status_icon_new_from_file("grey.png")
	threading.Thread(target=updateTimes,args=(icon, 300)).start()
	#multiprocessing.Process(target=updateTimes,args=(icon, 1)).start()
	icon.connect('popup-menu', on_right_click)
	icon.connect('activate', on_left_click)
	gtk.main()
