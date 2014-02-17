#include <panda_parser.h>
#include <kdebug.h>

#include <X11/Xlib.h>
#include <X11/Xutil.h>

// OpenGL includes
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glx.h>


void PandaParser::getGlStrings()
{
  GLXContext ctx;
  char *displayName = NULL;
  int scrnum = 0;

  const int attribSingle[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    None };
  const int attribDouble[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    GLX_DOUBLEBUFFER,
    None };

  Display *dpy = XOpenDisplay(displayName);
  unsigned long mask;
  XVisualInfo *visinfo;
  Window root, win;
  XSetWindowAttributes attr;

  root = DefaultRootWindow(dpy);

  visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribSingle));
  if (!visinfo) {
     visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribDouble));
     if (!visinfo) {
       kDebug() << "Error: couldn't find RGB GLX visual\n";
       return ;
     }
  }

  attr.colormap = XCreateColormap(dpy, root, visinfo->visual, AllocNone);
  attr.event_mask = StructureNotifyMask | ExposureMask;
  mask = CWBackPixel | CWBorderPixel | CWColormap | CWEventMask;
  win = XCreateWindow(dpy, root, 0, 0, 600, 600, 0, visinfo->depth, InputOutput, visinfo->visual, mask, &attr);

  ctx = glXCreateContext( dpy, visinfo, NULL, GL_TRUE);

  if (glXMakeCurrent(dpy, win, ctx)) {
    glVendor = (const char *) glGetString(GL_VENDOR);
    glRenderer = (const char *) glGetString(GL_RENDERER);
    glVersion = (const char *) glGetString(GL_VERSION);
  }

}
