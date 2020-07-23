'''**************************************************************************************
*
*	 File		    :	videodecoder_gstreamer.py
*	Description	    :	Video Decoding file opens the RTSP stream with gstreamer and Vaapi
*	Created on      :	4-feb-2019
*	Author	        :   Ankit Mishra
*	Email-id	    :   ankitmishra723@gmail.com
*   Modified By 	:   Ankit Mishra
*	Email-id 	    :    ankitmishra723@gmail.com
*	Modified Date	:    1-March-2019
*   Modification    :    1 Pylint error check handeled
*                        2 called function create_main_pipeline in init
*                        3. Wrong IP check for GStreamer
* -----------------------------------------------------------------------------

*-----------------------------------------------------------------------------
******************************************************************************************'''

# Import Python System Packages
import numpy as np
import cv2

# Third Party Library imports
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Const values
WIDTH = 1280
HEIGHT = 720

# Gstreamer initialization
Gst.init(None)
GObject.threads_init()

class GstreamerDecodeManager(object):
    '''**************************************************************************************
    *	Class name		:   GstreamerDecodeManager
    *	Description	:   Class containing function to extract real-time
    *				    stream from the camera specified by user
    *****************************************************************************************'''

    def __init__(self, source):
        '''*************************************************************************************
        *	Method name		:   __init__
        *	Description	    :  initialize attributes of the class
        *	Input value	    :  source_detail(Data dictionary from Backend),
        *************************************************************************************'''

        self.source = source
        self.size = (WIDTH, HEIGHT)
        self.valid_source = False
        self._create_main_pipeline(self.source, self.size)

    def _create_main_pipeline(self, source, size):
        pipeline_string = "uridecodebin name=decoder uri=" +self.source+ " ! videoconvert ! videoscale ! appsink name=play_sink"
        self.pipeline = Gst.parse_launch(pipeline_string)
        caps = "video/x-raw,format=BGR, width=%d, height=%d, depth=24, bpp=24" % self.size
        self.decoder = self.pipeline.get_by_name("decoder")
        self.streamsink = self.pipeline.get_by_name('play_sink')
        self.streamsink.set_property('emit-signals', True)
        self.streamsink.set_property('sync', False)
        self.streamsink.set_property('drop', True)
        self.streamsink.set_property('max-buffers', 1)
        self.streamsink.set_property('caps', Gst.caps_from_string(caps))
        source_obj = cv2.VideoCapture(self.source)
        if source_obj.isOpened():
            self.valid_source = True

    def read(self):
        '''*************************************************************************************
        *	Method name		:   read
        *	Description	    :  read the frames from stream
        *	Return value	:   Returns boolean value and Frame
        **************************************************************************************'''

        buff = self.streamsink.emit('pull-sample')
        if buff is not None:
            buff = buff.get_buffer()
            (result, mapinfo) = buff.map(Gst.MapFlags.READ)
            img_mat = np.ndarray(shape=(self.size[1], self.size[0], 3),
                                 dtype=np.uint8, buffer=mapinfo.data)
            buff.unmap(mapinfo)
            return True, img_mat
        else:
            return False, None

    def release(self):
        '''*************************************************************************************
        *	Method name		:   release
        *	Description	    :  srelease the memory
        **************************************************************************************'''

        self.pipeline.set_state(Gst.State.NULL)

    def isOpened(self):
        '''*************************************************************************************
        *	Method name		:   isOpened
        *	Description	    :  stream open or not
        *	Return value	:   Returns boolean value
        **************************************************************************************'''
        if self.valid_source:
            if self.pipeline.set_state(Gst.State.PLAYING):
                return True
        return False
