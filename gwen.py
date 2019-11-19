import vlc
from xmlrpc.server import SimpleXMLRPCServer
from gi.repository import GdkX11
from gi.repository import Gtk
import sys
import gi
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('GdkX11', '3.0')


MRL = ""    # Path to our video

######################################################################################################################
############################################ Class for Media Player ##################################################
######################################################################################################################


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused = False
        self.is_player_active = False
        self.connect("destroy", Gtk.main_quit)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()

        self.play_image = Gtk.Image.new_from_icon_name(
            "gtk-media-play",
            Gtk.IconSize.MENU
        )
        self.pause_image = Gtk.Image.new_from_icon_name(
            "gtk-media-pause",
            Gtk.IconSize.MENU
        )
        self.stop_image = Gtk.Image.new_from_icon_name(
            "gtk-media-stop",
            Gtk.IconSize.MENU
        )

        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)

        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300, 300)

        self.draw_area.connect("realize", self._realized)

        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)

    def toggle_player_playback(self, widget, data=None):
        """
        Handler for Player's Playback Button (Play/Pause).
        """

        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass

    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True

######################################################################################################################
############################################ APIs To control player ##################################################
######################################################################################################################

global window
window = None


def increaseVolume(lvl=1):
    print("Increasing Volume by ", lvl, "level")
    global window 
    window.player.audio_set_volume(window.player.audio_get_volume() + lvl*5)
    return 1


def decreaseVolume(lvl=1):
    print("Decreasing Volume by ", lvl, "level")
    global window 
    window.player.audio_set_volume(window.player.audio_get_volume() - lvl*5)
    return 1


def fastForward(lvl=1):
    print("FastForwarding by ", lvl, "level")
    return 1


def stop():
    print("Stopping...")
    global window
    window.player.stop()
    return 1


def pause():
    print("Pausing...")
    global window
    window.player.pause()
    return 1


def play():
    print("Playing...")
    global window
    window.player.play()
    return 1

def replay():
    print("Replaying Video...")
    stop()
    play()

######################################################################################################################
########################################## Initializers and Main func ################################################
######################################################################################################################

if __name__ == '__main__':
    if not sys.argv[1:]:
        print("Exiting \nMust provide the MRL.")
        sys.exit(1)

######################################################################################################################
############################################ RPC Bindings and setup ##################################################
######################################################################################################################

    if len(sys.argv) >= 3:
        port = sys.argv[2]
    else:
        port = 8888
    if len(sys.argv) == 4:
        ip = sys.argv[3]
    else:
        ip = 'localhost'
    print("Setting up RPC server on ", ip, port)
    server = SimpleXMLRPCServer((ip, port))
    server.register_function(increaseVolume, 'increaseVolume')
    server.register_function(decreaseVolume, 'decreaseVolume')
    server.register_function(fastForward, 'fastForward')
    server.register_function(stop, 'stop')
    server.register_function(pause, 'pause')
    server.register_function(play, 'play')
    server.register_function(replay, 'replay')
    serverThread = threading.Thread(target=server.serve_forever, args=()) # Launch RPC server to serve Asynchronously

######################################################################################################################
############################################## Media player setup ####################################################
######################################################################################################################

    print("Setting up Gwen media player...")
    MRL = sys.argv[1]
    window = ApplicationWindow()
    window.setup_objects_and_events()
    window.show()
    serverThread.start()
    Gtk.main()
    window.player.stop()
    window.vlcInstance.release()
