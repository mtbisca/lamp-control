from kivy.app import App
import socket
import time
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout

PORT = 50007
flag = 0

class blinkApp(App):

    def on_start(self):
         App.get_running_app().HOST = ''

    def timeout_callback(self, *args):
        flag = 1
        self.root.ids.log.text = "timeout!"
        print ("Callback fired")

    def turn_on(self):
        try:
            sk = App.get_running_app().connect_server()
            try:
                self.root.ids.state.text = 'Set to On'
                sk.send("Turn on!\r")
                event = Clock.schedule_once(self.timeout_callback, 5)
                data = sk.recv(128)
                if not flag:
                    event.cancel()
                    self.root.ids.log.text = data
            finally:
                sk.close()
        except:
            self.root.ids.log.text = "On? not connected!"


    def turn_off(self):
        try:
            sk = App.get_running_app().connect_server()
            try:
                self.root.ids.state.text = 'Set to Off'
                sk.send("Turn off!\r")
                # event = Clock.schedule_once(self.timeout_callback, 5)
                data = sk.recv(1024)
                self.root.ids.log.text = data
            finally:
                sk.close()
        except:
            self.root.ids.log.text = "Insert IP!"

    def get_info(self, info_name):
        try:
            sk = App.get_running_app().connect_server()
            try:
                sk.send("Get " + info_name + "\r")
                # event = Clock.schedule_once(self.timeout_callback, 15)
                data = sk.recv(1024)

                if info_name == "lum":
                    self.root.ids.lum_val.text = data
                elif info_name == "hum":
                    self.root.ids.hum_val.text = data + " %"
                elif info_name == "temp":
                    self.root.ids.temp_val.text = data + " C"
                else:
                    self.root.ids.state.text = data
                self.root.ids.log.text = data
            finally:
                sk.close()
        except:
            self.root.ids.log.text = "Cannot fetch %s: server not connected." % sensor_name

    def connect_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = App.get_running_app().HOST
        print(HOST)
        try:
            socket.inet_aton(HOST)
            s.settimeout(10) # 10 s to complete operation
            res = s.connect_ex((HOST, PORT))
            s.settimeout(None) # reset timeout
            if res == 0:
                self.root.ids.log.text = "Connected to "+ HOST
                return s
            else:
                self.root.ids.log.text = "Error connecting to "+ HOST
        except socket.timeout as e:
            self.root.ids.log.text = str(e)
        except socket.error as e:
            self.root.ids.log.text = str(e)
        if HOST == '':
            s.connect_ex((HOST, PORT))
            print ("On Android: to avoid typing errors on input text")

    def validate_server(self):
        App.get_running_app().HOST = self.root.ids.serverip.text
        print(App.get_running_app().HOST)

if __name__ == '__main__':
    app = blinkApp()
    app.run()
