import cv2
import threading

class GifDisplay():
    '''
    Note: 
    this class loops an mp4 file. 
    DO NOT use a GIF file. 
    Convert your gif to mp4 if you want to use this class.

    To use:
    1. create object.
        
        obj = gif_display("~/video.mp4")

    2. start the gif display. This will start the gif display in a separate thread. 
        can be terminated by pressing q when using the cv2 window.
        
        obj.open() 

    3. stop the gif display.

        obj.close()

    Note: If the gif_display() object goes out of scope 
          the window will be automatically closed and the video object will be released.
    '''
    def __init__(self, file_path):

        self.file_path = file_path
        self.video = cv2.VideoCapture(self.file_path)

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
        if int(major_ver)  < 3 :
            fps = self.video.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = self.video.get(cv2.CAP_PROP_FPS)

        self.delay = int((1000/fps)*0.25)

    def __del__(self):
        self.video.release()

    def display(self):
        cv2.namedWindow(self.file_path, cv2.WINDOW_FREERATIO)
        cv2.setWindowProperty(self.file_path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while(self.isopen):
            
            ret, frame = self.video.read()
            
            if ret:
                frame = cv2.resize(frame, (1024, 600))
                cv2.imshow(self.file_path, frame)
            else:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            if cv2.waitKey(self.delay) & 0xFF == ord('q'):
                break
        
        cv2.destroyWindow(self.file_path)

    def open(self):
        print(self.file_path + " gif opened")
        self.isopen = True
        gif_thread = threading.Thread(target=self.display)
        gif_thread.start()

    def close(self):

        self.isopen = False

if __name__ == '__main__':

    import time
    happy_face = GifDisplay('/home/jetson/clab_ws/src/clab/gif_files/happy.mp4')
    sad_face = GifDisplay('/home/jetson/clab_ws/src/clab/gif_files/sad.mp4')

    happy_face.open()
    time.sleep(5)
    happy_face.close()
    time.sleep(1)
    sad_face.open()
    time.sleep(5)
    sad_face.close()
    time.sleep(1)
    happy_face.open()
    time.sleep(5)
    happy_face.close()
    time.sleep(1)
