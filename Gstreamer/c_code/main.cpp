#include"Gstapp.h"
int main(int argc, char *argv[]) {

    /* Check command line argument */
    if(argc<3)
    {
        g_print("\n -------------------------Usage------------------------------ \n");
        g_print("\n ./run <rtsp url > < HW Decode > \n");
        g_print("\n 1st argument: RTSP url Ex: rtsp://admin:hcltech@10.160.102.14:554 \n");
        g_print("\n 2nd argument: Enable HW (VAAPI) decoding. Enable: 1, Disable: 0 \n");
        g_print("\n 3rd argument: Enable IFrame only decoding. Enable: 1, Disable: 0 \n");
        g_print("\n 4th argument: Enable IFrame only decoding. Enable: 1, Disable: 0 \n");
        g_print("\n 5th argument: Enable IFrame only decoding. Enable: 1, Disable: 0 \n");
        g_print("\n Example: ./run rtsp://admin:hcltech@10.160.102.14:554 1");
        g_print("\n          with HW( VAAPI) decoding is enabled \n");

        return 0;
    }

	GstPlayer stream;
        FdvdPlayer fdvdplayer;
  	FdvdPlayer::CustomData data;
  	GstStateChangeReturn ret;
  	GstBus *bus;
  	GstCaps *filtercaps;
	GstPad *identitypad;

        /* Parsing command line arguments */
        fdvdplayer.mpRtspUrl = argv[1];
        fdvdplayer.mHWDecodeFlag = atoi(argv[2]);
        fdvdplayer.miframeFlag = atoi(argv[3]);
  	
  	/* Initialize GTK */
  	gtk_init (&argc, &argv);
   
  	/* Initialize GStreamer */
  	gst_init (&argc, &argv);
   
  	/* Initialize our data structure */
 	memset (&data, 0, sizeof (data));
  	data.duration = GST_CLOCK_TIME_NONE;

  	stream.loop = g_main_loop_new (NULL, FALSE);

  	/* Create gstreamer elements */
  	data.pipeline = gst_pipeline_new("Create pipeline");

	data.source = gst_element_factory_make ("rtspsrc", "rtsp source");
  	data.demux = gst_element_factory_make ("rtph264depay", "rtp depacketizer");
  	data.parse = gst_element_factory_make("h264parse","parse");

        data.identity = gst_element_factory_make("identity","identity-frame");
	data.filter = gst_element_factory_make("capsfilter","filter");

        /* If HW Decoding flag is disabled then decode it using 
         SW Decoder (avdec_h264) otherwise enable HW ( VAAPI) decoding */
        if(!fdvdplayer.mHWDecodeFlag)
            data.decodebin = gst_element_factory_make ("avdec_h264","decode");
        else
            data.decodebin = gst_element_factory_make ("vaapidecode","decode");

        data.identity_after = gst_element_factory_make("identity","identity-after");
	data.conv = gst_element_factory_make ("videoconvert",  "converter");

        data.playsink = gst_element_factory_make("appsink","video sink");
        g_object_set(GST_OBJECT(data.playsink),"emit-signals",TRUE,"sync", FALSE , NULL);
        filtercaps = gst_caps_from_string("video/x-raw, format=(string)BGRA");
        g_object_set(GST_OBJECT(data.playsink),"caps",filtercaps);
        gst_caps_unref(filtercaps);

	g_object_set(GST_OBJECT(data.source),"location",fdvdplayer.mpRtspUrl, NULL);


	/* we add a message handler */
  	bus = gst_pipeline_get_bus (GST_PIPELINE (data.pipeline));
	gst_bus_set_sync_handler (bus, stream.bus_sync_handler, NULL, NULL);
  	stream.bus_watch_id = gst_bus_add_watch (bus, stream.bus_call, stream.loop);
  	gst_object_unref (bus);

	filtercaps = gst_caps_from_string("application/x-rtp");
	g_object_set (G_OBJECT (data.filter), "caps",filtercaps,NULL);

	gst_caps_unref(filtercaps);

	gst_bin_add_many (GST_BIN (data.pipeline),data.source
											  ,data.demux
											  ,NULL);
	// listen for newly created pads
	g_signal_connect(data.source, "pad-added", G_CALLBACK(stream.cb_new_rtspsrc_pad),data.demux);

	gst_bin_add_many (GST_BIN (data.pipeline),data.parse,NULL);
	if(!gst_element_link(data.demux,data.parse))
			g_print("\nNOPE\n");


	/* Dropping the buffer which is not a DELTA UNIT (Not I-Frame) from identity,
           If I Frmae flag is true */
        if(fdvdplayer.miframeFlag)
	    g_object_set(G_OBJECT(data.identity), "drop-buffer-flags",GST_BUFFER_FLAG_DELTA_UNIT,NULL);

    /* Adding the identity element in the pipeline */
	gst_bin_add_many (GST_BIN (data.pipeline),data.identity,NULL);
        g_signal_connect(data.identity , "handoff",G_CALLBACK(stream.checkidentity),NULL);

	/* Adding the identity element in the pipeline */
	if(!gst_element_link(data.parse,data.identity))
			g_print("\nNOPE IDENTITY\n");



	if(!gst_element_link_many(data.identity /*data.parse*/, data.decodebin,data.identity_after,data.conv,data.playsink,NULL))
		g_print("\n********Failed to link parse to sink******************\n");

	g_signal_connect(data.demux, "pad-added", G_CALLBACK(stream.on_pad_added), data.parse);
        g_signal_connect(data.playsink , "new-sample",G_CALLBACK(stream.checkbuffer),NULL);
   
  	/* Create the GUI */
  	GtkWidgets::create_ui (&data);

  	/* Start playing */
 	ret = gst_element_set_state (data.pipeline, GST_STATE_PLAYING);
  	if (ret == GST_STATE_CHANGE_FAILURE) {
    	g_print ("Unable to set the pipeline to the playing state.\n");
    	gst_object_unref (data.pipeline);
    	return -1;
  	}
   
  	/* Iterate */
  	g_print ("Running...\n");

  	gtk_main ();
   
  	return 0;
}
