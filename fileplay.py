import time
import threading
import socket

# singleton
__instance = None

# need to "play" from a different thread to keep UI available to user
# no need to use this class; the functions below handle everything
class FilePlayThread(threading.Thread):

     # execution states
     __RUN_STATE_PAUSED = 0
     __RUN_STATE_PLAY   = 1
     __RUN_STATE_STOP   = 2

     # time between characters
     __DELAY_MS         = 25

     def __init__(self, text_to_play, out_socket):
          super(FilePlayThread, self).__init__()
          self.__current_file_text     = text_to_play
          self.__current_file_position = 0
          self.__out_socket            = out_socket
          self.__run_state             = FilePlayThread.__RUN_STATE_PLAY

          # clear the output before each new file
          self.__out_socket.send(('\n' * 100).encode("utf-8"))

     # send a single character
     def send_char(self, c):
          self.__out_socket.send(c.encode("utf-8"))

     def play(self):
          self.__run_state = FilePlayThread.__RUN_STATE_PLAY

     def pause(self):
          self.__run_state = FilePlayThread.__RUN_STATE_PAUSED

     def stop(self):
          self.__run_state = FilePlayThread.__RUN_STATE_STOP

     # with proper respect to state, send 1 character to the display every __DELAY_MS milliseconds
     # play the file once, no looping
     def run(self):

          while FilePlayThread.__RUN_STATE_STOP != self.__run_state:

               while FilePlayThread.__RUN_STATE_PLAY == self.__run_state and self.__current_file_position < len(self.__current_file_text):

                    self.send_char(self.__current_file_text[self.__current_file_position])
                    time.sleep(FilePlayThread.__DELAY_MS / 1000)
                    self.__current_file_position += 1

               # no need to poll at 100% CPU, wait "idle" at 4 Hz polling rate
               time.sleep(0.25)

# "plays" a string, needs a socket to play to
# first kills any current file playing
def play(text_to_play, out_socket):

     global __instance

     # resume a paused file
     if __instance is not None:
          __instance.stop()
          __instance.join()

     # start
     __instance = FilePlayThread(text_to_play, out_socket)
     __instance.start()

# pauses the current file if one is playing
def pause():

     global __instance

     if __instance is not None:
          __instance.pause()

# resumes a paused file
def resume():

     global __instance

     if __instance is not None:
          __instance.play()

# ends play for the current file
def stop():

     global __instance

     if __instance is not None:
          __instance.stop()
          __instance.join()
          __instance = None