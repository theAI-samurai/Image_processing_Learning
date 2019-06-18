#include"Gstapp.h"

guintptr video_window_handle = 0;

gboolean GstPlayer::bus_call (GstBus     *bus,
          GstMessage *msg,
          gpointer    data)
{
  GMainLoop *loop = (GMainLoop *) data;

  switch (GST_MESSAGE_TYPE (msg)) {

    case GST_MESSAGE_EOS:
      g_print ("Calling EOS\n");
      g_print ("End of stream\n");
      g_main_loop_quit (loop);
      break;

    case GST_MESSAGE_ERROR: {
      gchar  *debug;
      GError *error;

      gst_message_parse_error (msg, &error, &debug);
      g_free (debug);

      g_printerr ("Error: %s\n", error->message);
      g_error_free (error);

      g_main_loop_quit (loop);
      break;
    }
    default:
      break;
  }

  return TRUE;
}

void GstPlayer::on_pad_added (GstElement *element, GstPad *pad, gpointer data)
{
    GstPad *sinkpad;
    //GstElement *decoder = (GstElement *) data;
    GstElement *encoder = (GstElement *) data;
    g_print ("\n****************Dynamic pad created, linking source/demuxer**************\n");
    sinkpad = gst_element_get_static_pad (encoder, "sink");
    gst_pad_link (pad, sinkpad);
    gst_object_unref (sinkpad);
}

//void GstPlayer::checkbuffer (GstElement *identity, GstPad *pad, gpointer data)
void GstPlayer::checkbuffer (GstElement *sink, gpointer data)
{
    g_print ("********CHECK BUFFER FUNCTION**********\n");
    GstSample *sample;
    GstBuffer *buffer;
    const GstStructure *str;
    gint width, height;
    const gchar *format;
    GstMapInfo map;

    sample = gst_app_sink_pull_sample(GST_APP_SINK(sink));
    if(sample!=NULL){
        buffer = gst_sample_get_buffer(sample);
        //std::ofstream outfile ("new.txt",std::ofstream::binary);
        //outfile.write (buffer,gst_buffer_get_size (buffer));
        //outfile.close();

        GstCaps *sampleCaps = gst_sample_get_caps(sample);
        str = gst_caps_get_structure(sampleCaps,0);
        g_print("Size : %d",gst_buffer_get_size (buffer));
        gst_structure_get_int(str,"width", &width);
        gst_structure_get_int(str,"height", &height);
        format = gst_structure_get_string(str,"format");
        g_print("width = %d", width);
        g_print("height = %d", height);
        g_print("Format : %s", format);
        gst_buffer_map(buffer, &map, GST_MAP_READ);
        //cv::Mat image(cv::Size(width, height), CV_8UC4, (char*) map.data, cv::Mat::AUTO_STEP);

        //g_print(*sampleCaps);
        g_print ("\n********BFFER EXTRACTED**********\n");
        gst_buffer_unmap(buffer, &map);
        
    }
    
    //exit(1);
    gst_sample_unref(sample);
    //g_object_set(G_OBJECT(identity), "drop-probability",0.0,NULL);
    //if(NULL !=buffer) {
    //    if(!GST_BUFFER_FLAG_IS_SET(buffer, GST_BUFFER_FLAG_DELTA_UNIT)) {
    //         g_print("\n********Received I Frame*****\n");
             

    //     }
    //    else {
    //           if(identity){
	             //g_print("\n****************BEFORE DROP******************\n");
        	     //g_object_set(G_OBJECT(identity), "drop-probability",1.0,NULL); 
    //    	     g_print("\n****************FRAME DROPPED******************\n");
                     //gst_buffer_unref(buffer);
    //           }
    //     }
    //}
    
}


//void GstPlayer::checkbuffer (GstElement *identity, GstPad *pad, gpointer data)
void GstPlayer::checkidentity (GstElement *identity, gpointer data)
{
    g_print ("********CHECK IDENTITY FUNCTION**********\n");
    //g_object_set(G_OBJECT(identity), "drop-probability",0.0,NULL);
    //if(NULL !=buffer) {
    //    if(!GST_BUFFER_FLAG_IS_SET(buffer, GST_BUFFER_FLAG_DELTA_UNIT)) {
    //         g_print("\n********Received I Frame*****\n");
             

    //     }
    //    else {
    //           if(identity){
	             //g_print("\n****************BEFORE DROP******************\n");
        	     //g_object_set(G_OBJECT(identity), "drop-probability",1.0,NULL); 
    //    	     g_print("\n****************FRAME DROPPED******************\n");
                     //gst_buffer_unref(buffer);
    //           }
    //     }
    //}
    
}


GstPadProbeReturn GstPlayer::probebuffer (GstPad *pad, GstPadProbeInfo *buffer, gpointer user_data)
{
    GstBuffer *gstbuffer;

    gstbuffer = GST_PAD_PROBE_INFO_BUFFER (buffer);
    g_print("\n************BUFFER PROBE**************\n");

    if(NULL !=gstbuffer) {
        if(!GST_BUFFER_FLAG_IS_SET(gstbuffer, GST_BUFFER_FLAG_DELTA_UNIT)) {
             g_print("\n********Received I Frame*****\n");           

         }
	else {
		return GST_PAD_PROBE_DROP;
	}
    }
    return GST_PAD_PROBE_OK;

}
void GstPlayer::cb_new_rtspsrc_pad(GstElement *element,GstPad*pad,gpointer  data)
{
	//g_print ("********New RTSP PAD Created**********\n");
	gchar *name;
	const GstCaps * p_caps;
	gchar * description;
	GstElement *p_rtph264depay;

	name = gst_pad_get_name(pad);
	g_print("A new pad %s was created\n", name);

	// here, you would setup a new pad link for the newly created pad
	// sooo, now find that rtph264depay is needed and link them?
	p_caps = gst_pad_get_pad_template_caps (pad);

	description = gst_caps_to_string(p_caps);
	//g_print("%s\n",p_caps,", ",description,"\n");
	g_free(description);

	p_rtph264depay = GST_ELEMENT(data);

	// try to link the pads then ...
	if(!gst_element_link_pads(element, name, p_rtph264depay, "sink"))
	{
		g_print("Failed to link elements 3\n");
	}

	g_free(name);
}

void GtkWidgets::realize_cb (GtkWidget *widget, CustomData *data) 
{
	//g_print ("********Realize Called on Widget**********\n");
  	GdkWindow *window = gtk_widget_get_window (widget);
   
  	if (!gdk_window_ensure_native (window))
    	g_error ("Couldn't create native window needed for GstXOverlay!");
   
    	gulong xid = GDK_WINDOW_XID (gtk_widget_get_window (widget));
    	video_window_handle = xid;
}

GstBusSyncReply GstPlayer::bus_sync_handler (GstBus * bus, GstMessage * message, gpointer user_data)
{
	//g_print ("********BUS Handler called**********\n");
 	if (video_window_handle != 0) {
   	GstVideoOverlay *overlay;

   	// message will be sent to sink
   	overlay = GST_VIDEO_OVERLAY (GST_MESSAGE_SRC (message));
   	gst_video_overlay_set_window_handle (overlay, video_window_handle);
 	} else {
   		g_warning ("Should have obtained video_window_handle by now!");
 	}

 	gst_message_unref (message);
 	return GST_BUS_DROP;
}
   
/* This function is called when the PLAY button is clicked */
void GtkWidgets::play_cb (GtkButton *button, CustomData *data) 
{
  	gst_element_set_state (data->pipeline, GST_STATE_PLAYING);
}
   
/* This function is called when the PAUSE button is clicked */
void GtkWidgets::pause_cb (GtkButton *button, CustomData *data) 
{
  	gst_element_set_state (data->pipeline, GST_STATE_PAUSED);
}
   
/* This function is called when the STOP button is clicked */
void GtkWidgets::stop_cb (GtkButton *button, CustomData *data) 
{
	gst_element_send_event(data->pipeline, gst_event_new_eos());
}
   
/* This function is called when the main window is closed */
void GtkWidgets::delete_event_cb (GtkWidget *widget, GdkEvent *event, CustomData *data) 
{
	g_print("****DELETE CALLED**********");
	g_print("****STOP BUTTON CLICKED CALLED**********");
	stop_cb (NULL, data);
	gtk_main_quit ();
}

gboolean GtkWidgets::expose_cb (GtkWidget *widget, GdkEventExpose *event, CustomData *data) {
  if (data->state < GST_STATE_PAUSED) {
    GtkAllocation allocation;
    GdkWindow *window = gtk_widget_get_window (widget);
    cairo_t *cr;
    /* Cairo for 2D graphics library */
    gtk_widget_get_allocation (widget, &allocation);
    cr = gdk_cairo_create (window);
    cairo_set_source_rgb (cr, 0, 0, 0);
    cairo_rectangle (cr, 0, 0, allocation.width, allocation.height);
    cairo_fill (cr);
    cairo_destroy (cr);
  }
  return FALSE;
}

/* This creates all the GTK+ widgets that compose our application, and registers the callbacks */
void GtkWidgets::create_ui (CustomData *data) {
  GtkWidget *main_window;  /* The uppermost window, containing all other windows */
  GtkWidget *video_window; /* The drawing area where the video will be shown */
  GtkWidget *main_box;     /* VBox to hold main_hbox and the controls */
  GtkWidget *main_hbox;    /* HBox to hold the video_window and the stream info text widget */
  GtkWidget *controls;     /* HBox to hold the buttons and the slider */
  GtkWidget *play_button, *pause_button, *stop_button, *quit_button; /* Buttons */
   
  main_window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  g_signal_connect (G_OBJECT (main_window), "delete-event", G_CALLBACK (delete_event_cb), data);
   
  video_window = gtk_drawing_area_new ();
  gtk_widget_set_double_buffered (video_window, FALSE);
  g_signal_connect (video_window, "realize", G_CALLBACK (realize_cb), data);
  g_signal_connect (video_window, "expose_event", G_CALLBACK (expose_cb), data);
   
  play_button = gtk_button_new_with_label (GTK_STOCK_MEDIA_PLAY);
  g_signal_connect (G_OBJECT (play_button), "clicked", G_CALLBACK (play_cb), data);
   
  pause_button = gtk_button_new_with_label (GTK_STOCK_MEDIA_PAUSE);
  g_signal_connect (G_OBJECT (pause_button), "clicked", G_CALLBACK (pause_cb), data);
   
  stop_button = gtk_button_new_with_label (GTK_STOCK_MEDIA_STOP);
  g_signal_connect (G_OBJECT (stop_button), "clicked", G_CALLBACK (stop_cb), data);

  quit_button = gtk_button_new_with_label (GTK_STOCK_QUIT);
  g_signal_connect (G_OBJECT (quit_button), "clicked", G_CALLBACK (gtk_main_quit), data);

  controls = gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0);
  gtk_box_pack_start (GTK_BOX (controls), play_button, FALSE, FALSE, 2);
  gtk_box_pack_start (GTK_BOX (controls), pause_button, FALSE, FALSE, 2);
  gtk_box_pack_start (GTK_BOX (controls), stop_button, FALSE, FALSE, 2);
  gtk_box_pack_start (GTK_BOX (controls), quit_button, FALSE, FALSE, 2);
    
  main_hbox = gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0);
  gtk_box_pack_start (GTK_BOX (main_hbox), video_window, TRUE, TRUE, 0);

  main_box = gtk_vbox_new (FALSE, 0);
  gtk_box_pack_start (GTK_BOX (main_box), main_hbox, TRUE, TRUE, 0);
  gtk_box_pack_start (GTK_BOX (main_box), controls, FALSE, FALSE, 0);
  gtk_container_add (GTK_CONTAINER (main_window), main_box);
  gtk_window_set_default_size (GTK_WINDOW (main_window), 640, 480);
   
  gtk_widget_show_all (main_window);
}


