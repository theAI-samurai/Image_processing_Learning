#!/usr/bin/env python

import os
import sys
import gi
import cv2
import numpy
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

image_arr = None

class GTK_Main(object):

    player = ''
    demuxer = ''
    parse = ''
    
    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Mpeg2-Player")
        window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        vbox.add(self.movie_window)
        window.show_all()
        
        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("rtspsrc", "rtsp-source")
        self.demuxer = Gst.ElementFactory.make("rtph264depay", "rtp depackketizer")
        self.parse = Gst.ElementFactory.make("h264parse","parse")
        self.filter = Gst.ElementFactory.make("capsfilter","filter")
        conv = Gst.ElementFactory.make("videoconvert", "converter")
        self.video_decoder = Gst.ElementFactory.make("avdec_h264", "video-decoder")
        sink = Gst.ElementFactory.make("appsink", "video sink")
        sink.set_property("emit-signals", True)
        #cap = Gst.Caps.from_string("video/x-raw-rgb") # ,format=(string){RGB, GRAY8}")
        #cap = Gst.caps_from_string("video/x-raw(meta:GstVideoGLTextureUploadMeta), format=(string)BGRA")
        cap = Gst.caps_from_string("video/x-raw, format=(string)BGRA")
        #cap = Gst.caps_from_string("video/x-raw, format=(string)RGBA")
        #self.filter.set_property("caps",cap)
        sink.set_property('caps', cap)
        print("*******---- App Sink Callback to be called ---***********")
        try:
            sink.connect("new-sample", self.appsink_callback)
            #print("=====  Returned to Main ======")
            #print(buff)
        except Exception as e:
            print("$$$$$$$$$$  Inside Exception ----- ", e)

        #sink.connect("new-sample", self.appsink_callback)

        source.connect("pad-added",self.on_pad_added)
        self.demuxer.connect("pad-added", self.demuxer_callback)

        #self.video_decoder = Gst.ElementFactory.make("mpeg2dec", "video-decoder")
        #self.audio_decoder = Gst.ElementFactory.make("mad", "audio-decoder")
        #audioconv = Gst.ElementFactory.make("audioconvert", "converter")
        #audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")
        #videosink = Gst.ElementFactory.make("xvimagesink", "video-output")
        #self.queuea = Gst.ElementFactory.make("queue", "queuea")
        self.queuev = Gst.ElementFactory.make("queue", "queuev")
        #colorspace = Gst.ElementFactory.make("videoconvert", "colorspace")
        print ("pipeline creted")
        self.player.add(source) 
        self.player.add(self.demuxer)
        self.player.add(self.parse)
        self.player.add(self.video_decoder) 
        self.player.add(conv)
        self.player.add(sink)
        print ("pipeline added")
        #self.player.add(self.audio_decoder) 
        #self.player.add(audioconv) 
        #self.player.add(audiosink) 
        #self.player.add(videosink) 
        #self.player.add(self.queuea) 
        #self.player.add(self.queuev) 
        #self.player.add(colorspace)
        print ("link demuxer")
        source.link(self.demuxer)
        print ("link parse")
        self.demuxer.link(self.parse)
        print("link decoder")
        self.parse.link(self.video_decoder)
        self.video_decoder.link(conv)
        print("link sink")
        conv.link(sink)
        print ("link done")
        
        #self.queuev.link(self.video_decoder)
        #self.video_decoder.link(colorspace)
        #self.video_decoder.link(sink)

        #self.queuea.link(self.audio_decoder)
        #self.audio_decoder.link(audioconv)
        #audioconv.link(audiosink)
        
        bus = self.player.get_bus()
        print ("get bus")
        bus.add_signal_watch()
        print ("get signal")
        bus.enable_sync_message_emission()
        print ("message emmision")
        bus.connect("message", self.on_message)
        print ("bus connect")
        bus.connect("sync-message::element", self.on_sync_message)


    def ctrate_pipeline(self):
        pass


    def start_stop(self, w):
        if self.button.get_label() == "Start":
            print ("**************START**********88")
            filepath = self.entry.get_text().strip()
            if True: #os.path.isfile(filepath):
                print(filepath)
                #filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.get_by_name("rtsp-source").set_property("location", filepath)
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            
    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            xid = self.movie_window.get_property('window').get_xid()
            imagesink.set_window_handle(xid)
    
    def appsink_callback(self , sink):
        try:
            print("*************-- Method Called --**************")
            sample = sink.emit("pull-sample")
            caps = sample.get_caps()
            buff = sample.get_buffer()
            (result, mapinfo) = buff.map(Gst.MapFlags.READ)
            arr = numpy.ndarray(shape=(int(caps.get_structure(0).get_value('height')), caps.get_structure(0).get_value('width'), 4), dtype=numpy.uint8, buffer = mapinfo.data)
            buff.unmap(mapinfo)
            #print(type(buff.extract_dup(0, buff.get_size())))
            print(caps)
            print(caps.get_structure(0).get_value('format'))
            print(caps.get_structure(0).get_value('height'))
            print(caps.get_structure(0).get_value('width'))
            #arr = numpy.zeros((1280, 720))
            #arr = numpy.frombuffer(buff.extract_dup(0, buff.get_size()), dtype=numpy.uint8, count=-1)

            #print(arr.shape)
            '''img = cv2.cvtColor(buff, cv2.COLOR_YUV2RGBA_I420)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            print("+++++++++++ About to Save +++++++++++")
            #print(img.shape)
            print(cv2.imwrite('image.jpg', img))
            print("+++++++++++ File Saved +++++++++++")
            sys.exit(0)'''
            #imgUMat = cv2.UMat(buff, buff.get_size())
            #imgUMat = cv2.Mat(buff.get_size(), CV_8UC1, buff);
            #cv2.imwrite('Image1.jpg', arr)
            #sys.exit(0)
            #print(arr)
            # return False
            #sample.gst_buffer_unref(buff)
            return Gst.FlowReturn.OK
        except Exception as e:
            print("Inside Exception")
            print(e)
            sys.exit(0)
        

    def demuxer_callback(self, demuxer, pad):
        print ("start")
        if True : #pad.get_property("template").name_template == "video_%02d":
            print ("enter")
            qv_pad = self.queuev.get_pad("sink")
            pad.link(qv_pad)
            print ("end")
        '''elif pad.get_property("template").name_template == "audio_%02d":
            qa_pad = self.queuea.get_pad("sink")
            pad.link(qa_pad)'''

    def rtsp_pad(self, rtspsrc, pad):
        demuxsinkpad = self.demuxer.get_static_pad("sink")
        pad.link(demuxsinkpad)


    def on_pad_added(self, src, new_pad):
        print(
            "Received new pad '{0:s}' from '{1:s}'".format(
                new_pad.get_name(),
                src.get_name()))

        # check the new pad's type
        new_pad_caps = new_pad.get_current_caps()
        new_pad_struct = new_pad_caps.get_structure(0)
        new_pad_type = new_pad_struct.get_name()
        #print("new_pad_caps  Type is '{0:s}' but link failed".format(new_pad_caps))
        '''if new_pad_type.startswith("audio/x-raw"):
            sink_pad = self.audio_convert.get_static_pad("sink")
        elif new_pad_type.startswith("video/x-raw"):
            sink_pad = self.video_convert.get_static_pad("sink")
        else:
            print(
                "It has type '{0:s}' which is not raw audio/video. Ignoring.".format(new_pad_type))
            return'''
        sink_pad = self.demuxer.get_static_pad("sink")
        print ("sink pad (type '{0:s}')".format(sink_pad.get_name()))
        # if our converter is already linked, we have nothing to do here
        if(sink_pad.is_linked()):
            print("We are already linked. Ignoring.")
            return

        # attempt the link
        ret = new_pad.link(sink_pad)
        if not ret == Gst.PadLinkReturn.OK:
            print("Type is '{0:s}' but link failed".format(new_pad_type))
        else:
            print ("linked to (type '{0:s}')".format(new_pad.get_name()))
            print("Link succeeded (type '{0:s}')".format(new_pad_type))

        return

    def demuxer_callback(self, src, new_pad):
        print ("*************DEMUXER **********")
        print(
            "Received new pad '{0:s}' from '{1:s}'".format(
                new_pad.get_name(),
                src.get_name()))

        # check the new pad's type
        new_pad_caps = new_pad.get_current_caps()
        new_pad_struct = new_pad_caps.get_structure(0)
        new_pad_type = new_pad_struct.get_name()

        '''if new_pad_type.startswith("audio/x-raw"):
            sink_pad = self.audio_convert.get_static_pad("sink")
        elif new_pad_type.startswith("video/x-raw"):
            sink_pad = self.video_convert.get_static_pad("sink")
        else:
            print(
                "It has type '{0:s}' which is not raw audio/video. Ignoring.".format(new_pad_type))
            return'''
        sink_pad = self.parse.get_static_pad("sink")
        # if our converter is already linked, we have nothing to do here
        if(sink_pad.is_linked()):
            print("We are already linked. Ignoring.")
            return

        # attempt the link
        ret = new_pad.link(sink_pad)
        if not ret == Gst.PadLinkReturn.OK:
            print("Type is '{0:s}' but link failed".format(new_pad_type))
        else:
            print ("linked to (type '{0:s}')".format(new_pad.get_name()))
            print("Link succeeded (type '{0:s}')".format(new_pad_type))

        return

Gst.init(None)
print ("gst init")
GTK_Main()
print ("GTK_Main init")
GObject.threads_init()
print("thread init")
Gtk.main()
print ("Gtk.main")
