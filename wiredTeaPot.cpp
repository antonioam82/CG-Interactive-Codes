 #include <GL/gl.h>
 #include <GL/glu.h>
 #include <GL/glut.h>
 void init(void)
{
   glClearColor (0.0, 0.0, 0.0, 0.0);
   glShadeModel (GL_FLAT);
 }
 void display(void)
 {
   glClear (GL_COLOR_BUFFER_BIT);
   glColor3f (1.0, 1.0, 1.0);
   glLoadIdentity();             /* clear the matrix */
           /* viewing transformation  */
   //gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
   glTranslatef(0.0,0.0,-5.0);
   glScalef (1.0, 1.0, 1.0);      /* modeling transformation */
   //glRotatef(0.0,0.0,90.0,20.0);
   //glutWireCube (1.0);
   glRotatef(20.0,1.0,0.0,0.0);
   glutWireTeapot(1.0);


   //glutWireTorus(0.5, 1.0, 30, 30);


   glFlush ();
 }
 void reshape (int w, int h)
 {
   glViewport (0, 0, (GLsizei) w, (GLsizei) h);
   glMatrixMode (GL_PROJECTION);
   glLoadIdentity ();
   //glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0);
   gluPerspective(60.0, 1.0, 2.5, 20.0);
   glMatrixMode (GL_MODELVIEW);
 }
 int main(int argc, char** argv)
 {
   glutInit(&argc, argv);
   glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB);
   glutInitWindowSize (500, 500);
   glutInitWindowPosition (100, 100);
   glutCreateWindow (argv[0]);
   init ();
   glutDisplayFunc(display);
   glutReshapeFunc(reshape);
   glutMainLoop();
   return 0;
 }
