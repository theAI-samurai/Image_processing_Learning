#include <string.h>
#include <gtk/gtk.h>
#include <gst/gst.h>
#include <gst/video/videooverlay.h>
//#include <gst/interfaces/xoverlay.h>
#include <gdk/gdk.h>
#include <gdk/gdkx.h>
#include <gst/app/gstappsink.h>
#include <stdlib.h>
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
   
class FdvdPlayer
{
	public:
	typedef struct _CustomData 
	{
	  GstElement *pipeline, *source, *demux, *decoder, *playsink, *recordsink, *mp4Mux, *parse, *filter, *decodebin, *identity ,  *conv;
	  GtkWidget *streams_list;        
	  GstState state;                 
	  gint64 duration;                
	} CustomData;
        char *mpRtspUrl;
        int mHWDecodeFlag;
        int miframeFlag;

	
};
class GstPlayer:protected FdvdPlayer
{
	public:
	CustomData data;
	//GSTREAMER
  	GMainLoop *loop;
  	guint bus_watch_id;

	GstPlayer()
	{
		
	}
	~GstPlayer()
	{
		/* Free resources */
  		gst_element_set_state (data.pipeline, GST_STATE_NULL);
  		gst_object_unref (data.pipeline);
  		g_print ("Deleting pipeline\n");
  		gst_object_unref (GST_OBJECT (data.pipeline));
  		g_source_remove (bus_watch_id);
  		g_main_loop_unref (loop);
  	}
	static gboolean bus_call (GstBus *bus, GstMessage *msg, gpointer data);
	static void on_pad_added (GstElement *element, GstPad *pad, gpointer data);
	//static void checkbuffer (GstElement *element, GstPad *pad, gpointer data);
	static void checkbuffer (GstElement *element, gpointer user_data);
	static void checkidentity (GstElement *element, gpointer user_data);
	static GstPadProbeReturn probebuffer(GstPad *pad, GstPadProbeInfo *buffer, gpointer user_data);
	static void cb_new_rtspsrc_pad(GstElement *element,GstPad *pad,gpointer  data);
	static GstBusSyncReply bus_sync_handler (GstBus *bus, GstMessage * message, gpointer user_data);
};

class GtkWidgets:protected FdvdPlayer
{
	public:
	static void realize_cb (GtkWidget *widget, CustomData *data);
 	static void play_cb (GtkButton *button, CustomData *data); 
	static void pause_cb (GtkButton *button, CustomData *data);
	static void stop_cb (GtkButton *button, CustomData *data); 
	static void delete_event_cb (GtkWidget *widget, GdkEvent *event, CustomData *data); 
	static gboolean expose_cb (GtkWidget *widget, GdkEventExpose *event, CustomData *data);
	static void create_ui (CustomData *data); 
};


