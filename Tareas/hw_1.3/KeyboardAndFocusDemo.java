
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class Pont2D {
    double x, y;
    Pont2D(double x, double y) {
        this.x = x;
        this.y = y;
    }
}

public class KeyboardAndFocusDemo extends JApplet
      implements KeyListener, FocusListener, MouseListener {
   // (Note: MouseListener is implemented only so that
   // the applet can request the input focus when
   // the user clicks on it.)

   static final int SQUARE_SIZE = 40; // Length of a side of the polygon.
   Color polygonColor; // The color of the polygon.

   int polygonTop, polygonLeft; // Coordinates of top-left corner of polygon.

   double[] xPuntos = { 82, 90, 95, 105, 104, 104, 102, 97, 50, 50, 95, 105, 116, 124, 170, 170, 123, 118, 116, 120, 127,
         131, 135,
         135, 131, 127, 120, 116, 118, 123, 170, 170, 124, 116, 105, 95, 50, 50, 97, 102, 104, 104, 105, 95, 90, 82, };

   double[] yPuntos = { 95, 90, 85, 80, 55, 51, 51, 30, 29, 25, 24, 20, 20, 24, 25, 29, 30, 51, 51, 80, 85, 91, 100,
         120, 129, 135, 140, 169, 169, 190, 191, 195, 196, 200, 200, 196, 195, 191, 190, 169, 169, 165, 140, 135, 130,
         125 };

   int POLYGON_POINTS = xPuntos.length;

   double polygonAngle = 0; // The polygon's rotation angle, in radians.


   boolean focussed = false; // True when this applet has input focus.

   DisplayPanel canvas; // The drawing surface on which the applet draws,
                        // belonging to a nested class DisplayPanel, which
                        // is defined below.

   public void init() {
      // Initialize the applet; set it up to receive keyboard
      // and focus events. Place the polygon in the middle of
      // the applet, and make the initial color of the polygon red.
      // Then, set up the drawing surface.

      setSize(1000, 600);

     


      polygonColor = Color.red;

      canvas = new DisplayPanel(); // Create drawing surface and
      setContentPane(canvas); // install it as the applet's content pane.

      canvas.setBackground(Color.white); // Set the background color of the canvas.

      canvas.addFocusListener(this); // Set up the applet to listen for events
      canvas.addKeyListener(this); // from the canvas.
      canvas.addMouseListener(this);

   } // end init();

   class DisplayPanel extends JPanel {
      // An object belonging to this nested class is used as
      // the content pane of the applet. It displays the
      // moving polygon on a white background with a border
      // that changes color depending on whether this
      // component has the input focus or not.

      public void paintComponent(Graphics g) {

         super.paintComponent(g); // Fills the panel with its
                                  // background color, which is white.

         /*
          * Draw a 3-pixel border, colored cyan if the applet has the
          * keyboard focus, or in light gray if it does not.
          */

         if (focussed)
            g.setColor(Color.cyan);
         else
            g.setColor(Color.lightGray);

         int width = getSize().width; // Width of the applet.
         int height = getSize().height; // Height of the applet.
         g.drawRect(0, 0, width - 1, height - 1);
         g.drawRect(1, 1, width - 3, height - 3);
         g.drawRect(2, 2, width - 5, height - 5);

         //Convert the polygon array to integers
         int[] xPuntosInt = new int[POLYGON_POINTS];
         int[] yPuntosInt = new int[POLYGON_POINTS];
         for (int i = 0; i < POLYGON_POINTS; i++) {
            xPuntosInt[i] = (int) xPuntos[i];
            yPuntosInt[i] = (int) yPuntos[i];
         }

         /* Draw the polygon. */

         g.setColor(polygonColor);
         g.fillPolygon(xPuntosInt, yPuntosInt, POLYGON_POINTS);

         /* If the applet does not have input focus, print a message. */

         if (!focussed) {
            g.setColor(Color.magenta);
            g.drawString("Click to activate", 7, 20);
         }

      } // end paintComponent()

   } // end nested class DisplayPanel

   // ------------------- Event handling methods ----------------------

   public void focusGained(FocusEvent evt) {
      // The applet now has the input focus.
      focussed = true;
      canvas.repaint(); // redraw with cyan border
   }

   public void focusLost(FocusEvent evt) {
      // The applet has now lost the input focus.
      focussed = false;
      canvas.repaint(); // redraw without cyan border
   }

   public void keyTyped(KeyEvent evt) {
      // The user has typed a character, while the
      // applet has the input focus. If it is one
      // of the keys that represents a color, change
      // the color of the polygon and redraw the applet.

      char ch = evt.getKeyChar(); // The character typed.

      if (ch == 'B' || ch == 'b') {
         polygonColor = Color.blue;
         canvas.repaint();
      } else if (ch == 'G' || ch == 'g') {
         polygonColor = Color.green;
         canvas.repaint();
      } else if (ch == 'R' || ch == 'r') {
         scaleAtOrigin(1.1);
      } else if (ch == 'K' || ch == 'k') {
         polygonColor = Color.black;
         canvas.repaint();
      } else if (ch == 'E' || ch == 'e') {
         rotateAtOrigin(0.1);
         //We increase the angle by 0.1 radians
         polygonAngle += 0.1;
      } else if (ch == 'D' || ch == 'd') {
         rotateAtOrigin(-0.1);
         //We decrease the angle by 0.1 radians
         polygonAngle -= 0.1;
      } else if (ch == 'F' || ch == 'f') {
         scaleAtOrigin(0.9);
      } 

   } // end keyTyped()

   //Function to get the center of the polygon
   public Pont2D getCenter() {
      double x = 0;
      double y = 0;
      for (int i = 0; i < POLYGON_POINTS; i++) {
         x += xPuntos[i];
         y += yPuntos[i];
      }
      x = x / POLYGON_POINTS;
      y = y / POLYGON_POINTS;
      return new Pont2D(x, y);
   }

   //Function to perform homogeneous transformation
   public void transform(double[][] matrix) {
      Pont2D center = getCenter();
      for (int i = 0; i < POLYGON_POINTS; i++) {
         double x = xPuntos[i] - center.x;
         double y = yPuntos[i] - center.y;
         xPuntos[i] = (x * matrix[0][0] + y * matrix[0][1] + matrix[0][2]) + center.x;
         yPuntos[i] = (x * matrix[1][0] + y * matrix[1][1] + matrix[1][2]) + center.y;
      }
   }

   //Function to perform rotation
   public void rotate(double angle) {
      double[][] matrix = { { Math.cos(angle), -Math.sin(angle), 0 }, { Math.sin(angle), Math.cos(angle), 0 } };
      transform(matrix);
   }

   //Function to perform translation
   public void translate(double x, double y) {
      double[][] matrix = { { 1, 0, x }, { 0, 1, y } };
      transform(matrix);
   }

   //Function to perform translation taking angle as parameter
   public void translateWithAngle(double angle, double distance) {
      double x = Math.cos(angle) * distance;
      double y = Math.sin(angle) * distance;
      translate(x, y);
   }

   //Function to perform scaling
   public void scale(double x, double y) {
      double[][] matrix = { { x, 0, 0 }, { 0, y, 0 } };
      transform(matrix);
   }

   //Function to take polygon to the origin perform rotation and then translate it back
   public void rotateAtOrigin(double angle) {
      Pont2D center = getCenter();
      translate(-center.x, -center.y);
      rotate(angle);
      translate(center.x, center.y);
   }

   //Function to take polygon to the origin perform scaling and then translate it back
   public void scaleAtOrigin(double scale) {
      Pont2D center = getCenter();
      translate(-center.x, -center.y);
      scale(scale, scale);
      translate(center.x, center.y);
   }

   
   //Function to translate polygon pressing the arrow keys
   public void keyPressed(KeyEvent evt) {
      int key = evt.getKeyCode();
      if (key == KeyEvent.VK_LEFT) {
         //translate(-10, 0);
         //translateWithAngle(polygonAngle, -10);
         translateWithAngle((-Math.PI / 2)+polygonAngle, -10);
      } else if (key == KeyEvent.VK_RIGHT) {
         //translate(10, 0);
         //translateWithAngle(polygonAngle, 10);
         translateWithAngle((-Math.PI / 2)+polygonAngle, 10);
      } else if (key == KeyEvent.VK_UP) {
         //translate(0, -10);
         //translateWithAngle((-Math.PI / 2)+polygonAngle, 10);
         translateWithAngle(polygonAngle, 10);
      } else if (key == KeyEvent.VK_DOWN) {
         //translate(0, 10);
         //translateWithAngle((-Math.PI / 2)+polygonAngle, -10);
         translateWithAngle(polygonAngle, -10);
      }
      canvas.repaint();
   }

   public void keyReleased(KeyEvent evt) {
      // empty method, required by the KeyListener Interface
   }

   public void mousePressed(MouseEvent evt) {
      // Request that the input focus be given to the
      // canvas when the user clicks on the applet.
      canvas.requestFocus();
   }

   public void mouseEntered(MouseEvent evt) {
   } // Required by the

   public void mouseExited(MouseEvent evt) {
   } // MouseListener

   public void mouseReleased(MouseEvent evt) {
   } // interface.

   public void mouseClicked(MouseEvent evt) {
   }

} // end class KeyboardAndFocusDemo
