import cv2

class Stream():
    def __init__(self):
        print("Initializing Stream of camera") 
        self.stream = None
        self.text = None
        self.frame = None


    def get_frame(self):
        ret,image = self.stream.read()
        if ret == True:
            ret,jpeg = cv2.imencode(".jpg",image)
            if ret == True:
                return jpeg.tobytes()
        else:
            #print("failed to read get_frame")
            pass

    def get_image(self):
        ret,image = self.stream.read()
        if ret == True:
            return image
        else:
            #print("failed to read get_image")
            pass

    def start(self):
        print("start streaming of camera")
        self.stream = cv2.VideoCapture(-1)

    def __del__(self):
        self.stream.release()
        cv2.destroyAllWindows()

    def save_picture(self):
        print("ENTER SAVE PICTURE")
        ret,image = self.stream.read()
        print(ret)
        if ret == True:
            filename = "new-Picture.jpg"
            print("Type of image : ",type(image))
            cv2.imwrite("/static/Images" + filename ,image)
            print("Picture saved!")
            return filename
        else:
            print("failed to save picture. Could not read image (self.stream.read())")
            return False


class Webcam():
    def __init__(self):
        self.on = False
    
    def set_switch_webcam(self,switch:bool):
        self.on = switch

    def get_switch_webcam(self):
        return self.on


    def generate(self,stream:Stream):
        while self.on==True:         
            
            frame = stream.get_frame()

            try:
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(frame) + b'\r\n')
            except:
                #print("Error - FAILED TO GET FRAME")
                pass