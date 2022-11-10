
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class KeyboardAndFocusDemo extends JApplet 
                  implements KeyListener, FocusListener, MouseListener {
                      // (Note:  MouseListener is implemented only so that
                      //         the applet can request the input focus when
                      //         the user clicks on it.)

   static final int SQUARE_SIZE = 40;  // Length of a side of the square.
   
   Color squareColor;  // The color of the square.
   
   int squareTop, squareLeft;  // Coordinates of top-left corner of square.
   
   boolean focussed = false;   // True when this applet has input focus.
   
   DisplayPanel canvas;  // The drawing surface on which the applet draws,
                         // belonging to a nested class DisplayPanel, which
                         // is defined below.

   public void init() {
        // Initialize the applet; set it up to receive keyboard
        // and focus events.  Place the square in the middle of
        // the applet, and make the initial color of the square red.
        // Then, set up the drawing surface.
        
	    setSize(800,600); 
	   
      squareTop = getSize().height / 2 - SQUARE_SIZE / 2;
      squareLeft = getSize().width / 2 - SQUARE_SIZE / 2;

      squareTop = getSize().height / 2 - SQUARE_SIZE / 2;
      squareLeft = getSize().width / 2 - SQUARE_SIZE / 2;
      
      squareColor = Color.red;
      
      canvas = new DisplayPanel();  // Create drawing surface and 
      setContentPane(canvas);       //    install it as the applet's content pane.

      canvas.setBackground(Color.white);  // Set the background color of the canvas.

      canvas.addFocusListener(this);   // Set up the applet to listen for events
      canvas.addKeyListener(this);     //                          from the canvas.
      canvas.addMouseListener(this);
      
   } // end init();
   
   
   class DisplayPanel extends JPanel {
          // An object belonging to this nested class is used as
          // the content pane of the applet.  It displays the
          // moving square on a white background with a border
          // that changes color depending on whether this 
          // component has the input focus or not.
   
      public void paintComponent(Graphics g) {
      
         super.paintComponent(g);  // Fills the panel with its
                                   // background color, which is white.

         /* Draw a 3-pixel border, colored cyan if the applet has the
            keyboard focus, or in light gray if it does not. */

         if (focussed) 
            g.setColor(Color.cyan);
         else
            g.setColor(Color.lightGray);
         
         

         int width = getSize().width;  // Width of the applet.
         int height = getSize().height; // Height of the applet.
         g.drawRect(0,0,width-1,height-1);
         g.drawRect(1,1,width-3,height-3);
         g.drawRect(2,2,width-5,height-5);

         /* Draw the square. */

         g.setColor(squareColor);
         g.fillRect(squareLeft, squareTop, SQUARE_SIZE, SQUARE_SIZE);

         /* If the applet does not have input focus, print a message. */

         if (!focussed) {
            g.setColor(Color.magenta);
            g.drawString("Click to activate",7,20);
         }

      }  // end paintComponent()
    
    } // end nested class DisplayPanel 
    
    

   // ------------------- Event handling methods ----------------------
   
   public void focusGained(FocusEvent evt) {
         // The applet now has the input focus.
      focussed = true;
      canvas.repaint();  // redraw with cyan border
   }
   

   public void focusLost(FocusEvent evt) {
         // The applet has now lost the input focus.
      focussed = false;
      canvas.repaint();  // redraw without cyan border
   }
   
   
   public void keyTyped(KeyEvent evt) {
          // The user has typed a character, while the
          // applet has the input focus.  If it is one
          // of the keys that represents a color, change
          // the color of the square and redraw the applet.
          
      char ch = evt.getKeyChar();  // The character typed.

      if (ch == 'B' || ch == 'b') {
         squareColor = Color.blue;
         canvas.repaint();
      }
      else if (ch == 'G' || ch == 'g') {
         squareColor = Color.green;
         canvas.repaint();
      }
      else if (ch == 'R' || ch == 'r') {
         squareColor = Color.red;
         canvas.repaint();
      }
      else if (ch == 'K' || ch == 'k') {
         squareColor = Color.black;
         canvas.repaint();
      }

   }  // end keyTyped()
   
   
   public void keyPressed(KeyEvent evt) { 
          // Called when the user has pressed a key, which can be
          // a special key such as an arrow key.  If the key pressed
          // was one of the arrow keys, move the square (but make sure
          // that it doesn't move off the edge, allowing for a 
          // 3-pixel border all around the applet).
          
      int key = evt.getKeyCode();  // keyboard code for the key that was pressed
      
      if (key == KeyEvent.VK_LEFT) {
         squareLeft -= 8;
         if (squareLeft < 3)
            squareLeft = 3;
         canvas.repaint();
      }
      else if (key == KeyEvent.VK_RIGHT) {
         squareLeft += 8;
         if (squareLeft > getSize().width - 3 - SQUARE_SIZE)
            squareLeft = getSize().width - 3 - SQUARE_SIZE;
         canvas.repaint();
      }
      else if (key == KeyEvent.VK_UP) {
         squareTop -= 8;
         if (squareTop < 3)
            squareTop = 3;
         canvas.repaint();
      }
      else if (key == KeyEvent.VK_DOWN) {
         squareTop += 8;
         if (squareTop > getSize().height - 3 - SQUARE_SIZE)
            squareTop = getSize().height - 3 - SQUARE_SIZE;
         canvas.repaint();
      }

   }  // end keyPressed()


   public void keyReleased(KeyEvent evt) { 
      // empty method, required by the KeyListener Interface
   }
   

   public void mousePressed(MouseEvent evt) {
        // Request that the input focus be given to the
        // canvas when the user clicks on the applet.
      canvas.requestFocus();
   }   
   
   
   public void mouseEntered(MouseEvent evt) { }  // Required by the
   public void mouseExited(MouseEvent evt) { }   //    MouseListener
   public void mouseReleased(MouseEvent evt) { } //       interface.
   public void mouseClicked(MouseEvent evt) { }

   


} // end class KeyboardAndFocusDemo
