//Program to display a wireframe sphere receiving as parameter the radius, meridians and parallels

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;  // for Vector

class Point {
   public double x, y;
   public Point( double X, double Y ) {
      x = X;  y = Y;
   }
}

class PointInt {
   public int x, y;
   public PointInt( int X, int Y ) {
      x = X;  y = Y;
   }
}

class Point3D {
   public double x, y, z;
   public Point3D( double X, double Y, double Z ) {
      x = X;  y = Y;  z = Z;
   }
}

class Edge {
   public double a, b;
   public Edge( double A, double B ) {
      a = A;  b = B;
   }
}

public class Sphere extends JApplet 
                  implements KeyListener, FocusListener, MouseListener {
                      
   double width, height;
   // int mx, my;  // the most recently recorded mouse coordinates

   double azimuth = 0, elevation = 0;  // angles of rotation of the sphere

   boolean focussed = false;   // True when this applet has input focus.

   //We create a vector of vertices
   Vector<Point3D> vertices = new Vector<Point3D>();

   //We create a vector of edges
   Vector<Edge> edges = new Vector<Edge>();
   
   DisplayPanel canvas;  

   public void init() {
      
      //We fill the vector with the vertices of the sphere
      double radius = 2;
      int meridians = 36;
      int parallels = 32;
      double dphi = 2*Math.PI/meridians; // angle between meridians
      double dtheta = Math.PI/parallels; // angle between parallels
      for ( int i = 0; i <= meridians; i++ ) { // loop over meridians
         double phi = i*dphi; // angle of meridian
         for ( int j = 0; j <= parallels; j++ ) { // loop over parallels
            double theta = j*dtheta; // angle of parallel
            double x = radius*Math.cos(phi)*Math.sin(theta); // x coordinate
            double y = radius*Math.sin(phi)*Math.sin(theta); // y coordinate
            double z = radius*Math.cos(theta); // z coordinate
            vertices.add( new Point3D(x,y,z) ); // add vertex to vector
         }
      }

      //We fill the vector with the edges of the sphere
      for ( int i = 0; i < meridians; i++ ) {
         //We add the edges of the meridian
         for ( int j = 0; j < parallels; j++ ) { // loop over parallels
            edges.add( new Edge( i*(parallels+1)+j, i*(parallels+1)+j+1 ) ); // edge from vertex (i,j) to vertex (i,j+1)
            edges.add( new Edge( i*(parallels+1)+j, (i+1)*(parallels+1)+j ) ); // edge from vertex (i,j) to vertex (i+1,j)
         }
         //We close the meridian
         edges.add( new Edge( i*(parallels+1)+parallels, (i+1)*(parallels+1)+parallels ) ); // edge from vertex (i,parallels) to vertex (i+1,parallels)
      }
      //We add the last meridian
      for ( int j = 0; j < parallels; j++ ) // loop over parallels
         edges.add( new Edge( meridians*(parallels+1)+j, meridians*(parallels+1)+j+1 ) ); // edge from vertex (meridians,j) to vertex (meridians,j+1)

    
      canvas = new DisplayPanel();  // Create drawing surface and 
      setContentPane(canvas);       //    install it as the applet's content pane.
   
      canvas.addFocusListener(this);   // Set up the applet to listen for events
      canvas.addKeyListener(this);     //                          from the canvas.
      canvas.addMouseListener(this);
      
   } // end init();
   
   class DisplayPanel extends JPanel {
      public void paintComponent(Graphics g) {
         super.paintComponent(g);  

         if (focussed) 
            g.setColor(Color.cyan);
         else
            g.setColor(Color.lightGray);

         double width = getSize().width;  // Width of the applet.
         double height = getSize().height; // Height of the applet.
         g.drawRect(0,0,(int)width-1,(int)height-1);
         g.drawRect(1,1,(int)width-3,(int)height-3);
         g.drawRect(2,2,(int)width-5,(int)height-5);

         if (!focussed) {
            g.setColor(Color.magenta);
            g.drawString("Click to activate",100,120); 
            g.drawString("Use arrow keys to change azimuth and elevation",100,150);

         }
         else {

            double theta = Math.PI * azimuth / 180.0; // azimuth in radians
            double phi = Math.PI * elevation / 180.0; // elevation in radians
            double cosT = Math.cos( theta ), sinT = Math.sin( theta ); // cos and sin of azimuth
            double cosP = Math.cos( phi ), sinP = Math.sin( phi ); // cos and sin of elevation
            double cosTcosP = cosT*cosP, cosTsinP = cosT*sinP,
                  sinTcosP = sinT*cosP, sinTsinP = sinT*sinP;

            // project vertices onto the 2D viewport
            // We create a vector of projected vertices
            Vector<Point> points = new Vector<Point>();
            double scaleFactor = width/8; // arbitrary scale factor
            double near = 3;  // distance from eye to near plane
            double nearToObj = 1.5;  // distance from near plane to center of object

            // We project the vertices
            for ( int i = 0; i < vertices.size(); ++i ) {
               double x0 = vertices.get(i).x;
               double y0 = vertices.get(i).y;
               double z0 = vertices.get(i).z;

               // compute an orthographic projection
               double x1 = cosT*x0 + sinT*z0;
               double y1 = -sinTsinP*x0 + cosP*y0 + cosTsinP*z0;
               double z1 = cosTcosP*z0 - sinTcosP*x0 - sinP*y0;

               // now adjust things to get a perspective projection
               x1 = x1*near/(z1+near+nearToObj);
               y1 = y1*near/(z1+near+nearToObj);


               //We add the projected vertices to the vector
               points.add(new Point(width/2 + scaleFactor*x1, height/2 - scaleFactor*y1));
            }

            //We convert the points array from double to int and we draw the edges
            //We define a vector called pointsInt of type PointInt
            Vector<PointInt> pointsInt = new Vector<PointInt>(); //We create the vector
            for (int i = 0; i < points.size(); i++) { //We loop over the points
               pointsInt.add(new PointInt((int)points.get(i).x, (int)points.get(i).y)); //We add the projected vertices to the vector
            }

            // draw the wireframe
            g.setColor( Color.black ); //We set the color to black
            g.fillRect( 0, 0, (int)width, (int)height ); //We fill the background
            g.setColor( Color.white ); //We set the color to white for the edges of the sphere
            for (int i = 0; i < edges.size(); ++i ) {
               g.drawLine(
                  pointsInt.get((int)edges.get(i).a).x, pointsInt.get((int)edges.get(i).a).y,
                  pointsInt.get((int)edges.get(i).b).x, pointsInt.get((int)edges.get(i).b).y
               );
            }
         } 
      }  // end paintComponent()    
    } // end nested class DisplayPanel 

   // ------------------- Event handling methods ----------------------
   
   public void focusGained(FocusEvent evt) {
      focussed = true;
      canvas.repaint();
   }
   
   public void focusLost(FocusEvent evt) {
      focussed = false;
      canvas.repaint(); 
   }
      
   public void keyTyped(KeyEvent evt) {  
   }  // end keyTyped()
      
   public void keyPressed(KeyEvent evt) { 
       
      int key = evt.getKeyCode();  // keyboard code for the key that was pressed
      
      if (key == KeyEvent.VK_LEFT) {
         azimuth += 5;
         canvas.repaint();         
      }
      else if (key == KeyEvent.VK_RIGHT) {
         azimuth -= 5;
         canvas.repaint();         
      }
      else if (key == KeyEvent.VK_UP) {
         elevation -= 5;
         canvas.repaint();         
      }
      else if (key == KeyEvent.VK_DOWN) {
         elevation += 5;         
         canvas.repaint();
      }

   }  // end keyPressed()

   public void keyReleased(KeyEvent evt) { 
      // empty method, required by the KeyListener Interface
   }
   
   public void mousePressed(MouseEvent evt) {      
      canvas.requestFocus();
   }      
   
   public void mouseEntered(MouseEvent evt) { }  // Required by the
   public void mouseExited(MouseEvent evt) { }   //    MouseListener
   public void mouseReleased(MouseEvent evt) { } //       interface.
   public void mouseClicked(MouseEvent evt) { }
   public void mouseDragged( MouseEvent e ) { }
} // end class 
