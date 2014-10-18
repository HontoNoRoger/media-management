'''
Created on 15.06.2014

@author: hontonoroger
'''

import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from cgitb import text

class GUI(object):
    '''
    classdocs
    '''


    def __init__(self, client):
        '''
        Constructor
        '''
        
        self._client = client
        
        # Main window
        root = tk.Tk()
        root.title("Medienverwaltung")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        
        # Menu
        topmenu = tk.Menu(root, title='Menu')
        topmenu.add_cascade(label='Datei')
        
        listmenu = tk.Menu(topmenu)
        topmenu.add_cascade(label='Liste', menu=listmenu)
        listmenu.add_command(label='Aktualisieren', command=self.refresh_medialist)
        root.config(menu=topmenu)
        
        # Search bar
        tk.Label(root, text='Search for:').grid(row=0, column=8, sticky='ne')
        tk.Entry(root, width=50).grid(row=0, column=9, columnspan=3, sticky='ne')
        
        # Directory Browser
        treecontainer = tk.Frame(root).grid(row=1, column=0, sticky='nw')
        self.tree = ttk.Treeview(treecontainer)
        ysb = ttk.Scrollbar(treecontainer, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(treecontainer, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Path', anchor='nw')

        abspath = os.path.abspath('.') #TODO set to servers content path 
        treecontainer_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(treecontainer_node, abspath)

        self.tree.grid(row=1, column=0, sticky='nsew')
        ysb.grid(row=1, column=0, sticky='ens')
        xsb.grid(row=1, column=0, sticky='sew')
        
        # Media listing 
        self._media_listing = ttk.Treeview(root, columns=['Name', 'Typ', 'Genre', 'Länge', 'Size'])
        self._media_listing.heading('#0', text='#')
        self._media_listing.heading('#1', text='Name')
        self._media_listing.heading('#2', text='Typ')
        self._media_listing.heading('#3', text='Genre')
        self._media_listing.heading('#4', text='Länge')
        self._media_listing.heading('#5', text='Size')
        vsb = ttk.Scrollbar(orient="vertical",
            command=self._media_listing.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self._media_listing.grid(row=1, column=1, columnspan=11, sticky='ne')
        
        # Thumbnail
        image = Image.open("files/noimage.jpeg")
        thumbnail = ImageTk.PhotoImage(image)
        tk.Label(root, image=thumbnail).grid(row=2, rowspan=3, column=0, sticky='nsew')
        
        # Details section
        details_group = tk.LabelFrame(root, text='Details').grid(row=2, rowspan=3, column=1, columnspan=10)
        tk.Label(details_group, text='Name: ').grid(row=2, column=1, sticky='nw')
        tk.Label(details_group, text='').grid(row=2, column=2, sticky='nw')
        tk.Label(details_group, text='Typ: ').grid(row=2, column=3, sticky='nw')
        tk.Label(details_group, text='').grid(row=2, column=4, sticky='nw')
        tk.Label(details_group, text='Genre: ').grid(row=2, column=5, sticky='nw')
        tk.Label(details_group, text='').grid(row=2, column=6, sticky='nw')
        tk.Label(details_group, text='Länge: ').grid(row=2, column=7, sticky='nw')
        tk.Label(details_group, text='').grid(row=2, column=8, sticky='nw')
        tk.Label(details_group, text='Größe: ').grid(row=2, column=9, sticky='nw')
        tk.Label(details_group, text='').grid(row=2, column=10, sticky='nw')
        tk.Label(details_group, text='Beschreibung: ').grid(row=3, column=1, sticky='sw')
        tk.Label(details_group, text='').grid(row=4, column=1, columnspan=10, sticky='nw')

        
        # Play button
        tk.Button(root, text="Add to Playlist").grid(row=2, column=11, sticky='sew')
        play_image = Image.open("files/play.png")
        play_image = ImageTk.PhotoImage(play_image)
        tk.Button(root, image=play_image).grid(row=3, rowspan=2, column=11, sticky='sew')

        root.mainloop()
        
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)
                
    def refresh_medialist(self):
        self._client.refresh_server_media()
        for medium in self._client.get_server_media():
            self._media_listing.insert('', 0, iid=medium['media_id'])
        # TODO: in Liste einordnen
                
if __name__ == '__main__':
    gui = GUI()