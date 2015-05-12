#!/usr/bin/env python2
# coding=utf-8

__docformat__ = "restructuredtext"
'''
Created on 16/12/2011

@author: Jesus Becerril Navarrete (jbnkuma)
@email: jesusbn5@gmail.com
Copyright (C) 2013 Jesus Becerril Navarrete <jesusbn5@gmail.com>

capturescreen_puesto.py is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

capturescreen_puesto.py is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygtk

pygtk.require("2.0")
import gtk
from paramiko import SSHClient, AutoAddPolicy
from PythonMagick import Image
from os import path, makedirs
from shutil import rmtree
from visor import exe
from IPy import IP


class TomaFoto(object):
    """
    Clase que optiene una imagen remota del escritorio, guarda y manipula para su
    presentacion en pantalla.
    """

    def valida_ip(self, ip):
        "Valida que el dato dad sea realmente una ip"
        try:
            IP(ip)
            return True
        except:
            return False

    def conexion(self, widget, entry):
        """Realiza la conexion remota y ejecuta el comando para obtener el screenshot de la pantalla."""
        ip = entry.get_text().strip()
        if ip != "Ip del puesto" and ip != "" and self.valida_ip(ip):
            imagen_tmp = self.dir_tmp + "img_tmp.xwd"
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(ip, username="", password="")
            cmd = "/usr/bin/hostname"
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            nombre_suc = stdout.read()
            ssh_client.connect(ip, username="", password="")
            cmd = "/usr/bin/xwd -display :0.0  -root -silent "
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            imagen = stdout.read()

            archivo = open(imagen_tmp, "w")
            archivo.write(imagen)
            archivo.close()
            self.manipula_img(imagen_tmp, nombre_suc.strip("\n"))

    def comprueba_nombre(self, nombre_img, nmsuc):
        """Funcion que evita nombrar un archivo con el mismo nombre"""
        tmp = nombre_img.split("_")
        contador = int(tmp[2].split(".")[0])
        contador += 1
        image_final = self.dir_tmp + nmsuc + "_" + str(contador) + ".jpg"
        if path.exists(image_final):
            return self.comprueba_nombre(image_final, nmsuc)
        else:
            return image_final

    def manipula_img(self, img_r, nmsuc):
        """Procesa la imagen adquirida en formato xwd y la trasforma en jpg"""
        image_final = self.dir_tmp + nmsuc + ".jpg"
        contador = 0
        if path.exists(image_final):
            contador += 1
            image_final = self.dir_tmp + nmsuc + "_" + str(contador) + ".jpg"
            if path.exists(image_final):
                image_final = self.comprueba_nombre(image_final, nmsuc)
        img = Image(img_r)
        img.scale("1024x768")
        img.write(image_final)
        exe(image_final, nmsuc)

    def __init__(self):
        self.dir_tmp = "/tmp/dirs_img/"
        if path.exists(self.dir_tmp):
            rmtree(self.dir_tmp)
            makedirs(self.dir_tmp)
        else:
            makedirs(self.dir_tmp)
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(300, 100)
        window.set_title("Capturar Pantalla Remota")
        window.connect("delete_event", lambda w, e: gtk.main_quit())

        vbox = gtk.VBox(gtk.FALSE, 0)
        window.add(vbox)
        vbox.show()

        entry = gtk.Entry()
        entry.set_max_length(45)
        entry.connect("activate", self.conexion, entry)
        entry.set_text("Ip del puesto")
        entry.insert_text("", len(entry.get_text()))
        entry.select_region(0, len(entry.get_text()))
        vbox.pack_start(entry, gtk.TRUE, gtk.TRUE, 0)
        entry.show()

        hbox = gtk.HBox(gtk.FALSE, 0)
        vbox.add(hbox)
        hbox.show()

        vbox2 = gtk.HBox(gtk.FALSE, 0)
        vbox.add(vbox2)
        vbox2.show()

        button = gtk.Button("Capturar")
        button.connect("clicked", self.conexion, entry)
        vbox2.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button.connect("clicked", lambda w: gtk.main_quit())
        vbox2.pack_end(button, gtk.TRUE, gtk.TRUE, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    TomaFoto()
    main()
