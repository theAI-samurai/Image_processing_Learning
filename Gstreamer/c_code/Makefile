cc=g++

CFLAGS= -c -Wall

LDFLAGS = -lopencv_legacy -lopencv_highgui -lopencv_core -lopencv_ml -lopencv_video -lopencv_imgproc -lopencv_calib3d -lopencv_objdetect -L/usr/lib
CPPFLAGS = -g -I/usr/include/opencv -I/usr/include/opencv2


all: run

run: main.o Gstapp.o
	$(cc) main.o Gstapp.o -o run -lgstvideo-1.0 `pkg-config --cflags --libs gstreamer-1.0 gstreamer-app-1.0 gtk+-3.0 opencv`

main.o: main.cpp
	$(cc) $(CFLAGS) main.cpp -lgstvideo-1.0 `pkg-config --cflags --libs gstreamer-1.0 gstreamer-app-1.0 gtk+-3.0 opencv`

Gstapp.o: Gstapp.cpp
	$(cc) $(CFLAGS) Gstapp.cpp -lgstvideo-1.0 `pkg-config --cflags --libs gstreamer-1.0 gstreamer-app-1.0 gtk+-3.0 opencv`

 
clean:
	rm -rf *o run

