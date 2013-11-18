#!/usr/bin/env/python2
# -*- encoding: utf-8 -*-
__docformat__ = "restructuredtext"
'''
Created on 22/12/2011

@author: Jesus Becerril Navarrete (jbnkuma)
@email: jesusbn5@gmail.com

Copyright (C) 2013 Jesus Becerril Navarrete <jesusbn5@gmail.com>

visor.py is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

visor.py is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygtk

pygtk.require("2.0")
import gtk
from os import path, remove
from PythonMagick import Image


class visor():
    def guardar_img(self, widget, string, img):
        filechooser = gtk.FileChooserDialog("Guardar Imagen", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        filechooser.set_default_response(gtk.RESPONSE_OK)
        filechooser.set_current_name(img.split("/")[3])
        filter = gtk.FileFilter()
        filter.set_name("Todos los archivos")
        filter.add_pattern("*")
        filechooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Imágenes")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        filechooser.add_filter(filter)

        respuesta = filechooser.run()

        if respuesta == gtk.RESPONSE_OK:
            try:
                fimg = Image(img)
                fimg.write(filechooser.get_filename())
                filechooser.destroy()
            except:
                pass
        else:
            filechooser.destroy()

    def cerrar(self, widget, event, data=None):
        if path.exists(data):
            remove(data)
        gtk.main_quit()
        return gtk.FALSE

    def __init__(self, imagen, puesto_name):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.cerrar, imagen)
        window.set_title(puesto_name)
        window.set_border_width(20)
        vbox = gtk.VBox(gtk.FALSE, 1)
        window.add(vbox)
        vbox.show()
        pixbufimg = gtk.gdk.PixbufAnimation(imagen)
        image = gtk.Image()
        image.set_from_animation(pixbufimg)
        vbox.pack_end(image)
        image.show()

        menu = gtk.Menu()
        buf = "Guardar"
        menu_items = gtk.MenuItem(buf)
        menu.append(menu_items)
        menu_items.connect("activate", self.guardar_img, buf, imagen)
        menu_items.show()

        save_item = gtk.MenuItem("Archivo")
        save_item.show()
        save_item.set_submenu(menu)
        menu_bar = gtk.MenuBar()
        menu_bar.show()
        vbox.pack_start(menu_bar, gtk.TRUE, gtk.TRUE, 1)
        menu_bar.append(save_item)
        window.show()


def main2():
    gtk.main()
    return 0


def exe(img, namep):
    visor(img, namep)
    main2()
