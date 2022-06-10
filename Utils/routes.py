
from fastapi import FastAPI,File,UploadFile,Form
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from typing import List,Dict
from Utils.camera import Stream
from Utils.camera import Webcam
import os
import cv2
import numpy as np





class Routes:

    app = FastAPI()

    def __init__(self):
        self.app.mount("/static", StaticFiles(directory="./static"), name="static")
        self.templates = Jinja2Templates(directory="templates")
        self.stream = Stream()
        self.webcam = Webcam()

    def run(self):
        print("Run Routes")
        self.start()
        return self.app
    
    def start_stream(self):
        print("function start_stream")
        self.stream.start()
        self.webcam.set_switch_webcam(True)
    
    def stop_stream(self):
        print("function stop_stream")
        if self.webcam.get_switch_webcam() == True:
            self.webcam.set_switch_webcam(False)
            self.stream.__del__()
        

    def start(self):
        print("Start Routes")
        app = self.app
        templates = self.templates
        print("WEBCAM SWITCH = ",self.webcam.get_switch_webcam())

        @app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            self.stop_stream()
            context = {"request": request}
            return templates.TemplateResponse("index.html", context)
        
        @app.get("/browse", response_class=HTMLResponse)
        async def browse(request: Request):
            self.stop_stream()
            context = {"request": request}
            return templates.TemplateResponse("browse.html", context)
        
        @app.get("/prediction", response_class=HTMLResponse)
        async def prediction(request: Request):
            self.stop_stream()
            context = {"request": request}
            return templates.TemplateResponse("prediction.html", context)
        
        @app.get("/type", response_class=HTMLResponse)
        async def browse(request: Request):
            self.stop_stream()
            types = os.listdir('static/clothes/') 
            number_of_types = len(types)
            print(types)
            context = {"request": request}
            context["types"] = types
            context["number_of_types"] = number_of_types
            return templates.TemplateResponse("type.html", context)

        @app.get("/camera", response_class=HTMLResponse)
        async def browse(request: Request):
            self.start_stream()
            context = {"request": request}
            return templates.TemplateResponse("camera.html", context)

        
        @app.get("/video/",response_class=HTMLResponse)
        def video(request:Request):
            print("camera video route")
            return StreamingResponse(self.webcam.generate(self.stream),
            media_type="multipart/x-mixed-replace;boundary=frame"
            )

        @app.post("/submitform",response_class=HTMLResponse)
        async def handle_form(request:Request):
            print("form submitted!!!!!!!!!!")
            file_name = "new-Picture.jpg"
            print("writing image")
            cv2.imwrite("./static/Images/" + file_name,self.stream.get_image())
            context = {"request":request}
            context["filename"] = file_name
            return templates.TemplateResponse("prediction.html",context)