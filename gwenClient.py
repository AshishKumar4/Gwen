import xmlrpc
import xmlrpc.client

class gwenClient:
    def __init__(self, ip= 'localhost', port = 8888):
        self.ip = ip
        self.port = port 
        print("Trying to connect to gwen server at ", ip, port)
        try:
            self.proxy = xmlrpc.client.ServerProxy('http://' + ip + ':' + str(port) + "/")
            self.handlerMap = dict({
                'play':self.play,
                'stop':self.stop,
                'pause':self.pause,
                'increaseVolume':self.increaseVolume,
                'decreaseVolume':self.decreaseVolume,
                'replay':self.replay
            })
            print("Connected!")
        except Exception as e:
            print("Server could not be contacted!!! Check your connection or ip/port!")
            print(e)
            return None
    
    def play(self):
        print("Playing Video...")
        self.proxy.play()
        # Play is equivalent to Resume!!!

    def pause(self):
        print("Pausing Video...")
        self.proxy.pause()

    def stop(self):
        print("Stopping Video...")
        self.proxy.stop()

    def increaseVolume(self, lvl=1):
        print("Increasing Volume by 1 unit...")
        self.proxy.increaseVolume(lvl)

    def decreaseVolume(self, lvl=1):
        print("Decreasing Volume by 1 unit...")
        self.proxy.decreaseVolume(lvl)

    def replay(self):
        print("Replaying Video...")
        self.proxy.replay()
    # REMEMBER TO PUT THESE CALLS IN TRY/EXCEPT BLOCKS!!!!

    def autoHandler(self, option):
        try:
            self.handlerMap[option]()
        except Exception as e:
            print("Error occured in auto handler!!!")
            print(e)

