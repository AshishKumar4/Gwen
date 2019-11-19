import xmlrpc
import xmlrpc.client

class gwenClient:
    def __init__(self, ip= 'localhost', port = 8888):
        self.ip = ip
        self.port = port 
        print("Trying to connect to gwen server at ", ip, port)
        try:
            self.proxy = xmlrpc.client.ServerProxy('http://' + ip + ':' + str(port) + "/")
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

    def increaseVolume(self):
        print("Increasing Volume by 1 unit...")
        self.proxy.increaseVolume(1)

    def decreaseVolume(self):
        print("Decreasing Volume by 1 unit...")
        self.proxy.decreaseVolume(1)

    # REMEMBER TO PUT THESE CALLS IN TRY/EXCEPT BLOCKS!!!!


# Demo ==>
# obj = gwenClient()
# if obj is not None:
#     obj.play()
#     obj.stop()
#     obj.increaseVolume()
