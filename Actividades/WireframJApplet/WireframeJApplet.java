import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class Point3D {
    public int x, y, z;
    public Point3D(int X, int Y, int Z){
        x = X;
        y = Y;
        z = Z;
    }
}

class Edge {
    public int a, b;
    public Edge(int A,int B){
        a = A;
        b = B;
    }
}

public class WireframeJApplet extends JApplet implements KeyListener, FocusListener, MouseListener {
    int width, height;
    int azimuth = 0;
    int elevation = 0;

    Point3D[] vertices;
    Edge[] edges;

    boolean focussed = false;

    DisplayPanel canvas;

    public void init(){
        vertices = new Point3D[8];
        vertices[0] = new Point3D(-1, -1, -1);
        vertices[1] = new Point3D(-1, -1, 1);
        vertices[2] = new Point3D(-1, 1, -1);
        vertices[3] = new Point3D(-1, 1, 1);
        vertices[4] = new Point3D(1, -1, -1);
        vertices[5] = new Point3D(1, -1, 1);
        vertices[6] = new Point3D(1, 1, -1);
        vertices[7] = new Point3D(1, 1, 1);

        edges = new Edge[12];
        edges[0]  = new Edge( 0, 1 );
        edges[1]  = new Edge( 0, 2 );
        edges[2]  = new Edge( 0, 4 );
        edges[3]  = new Edge( 1, 3 );
        edges[4]  = new Edge( 1, 5 );
        edges[5]  = new Edge( 2, 3 );
        edges[6]  = new Edge( 2, 6 );
        edges[7]  = new Edge( 3, 7 );
        edges[8]  = new Edge( 4, 5 );
        edges[ 9] = new Edge( 4, 6 );
        edges[10] = new Edge( 5, 7 );
        edges[11] = new Edge( 6, 7 );

        canvas = new DisplayPanel();
        setContentPane(canvas);

        canvas.addFocusListener(this);
        canvas.addKeyListener(this);
        canvas.addMouseListener(this);
    }

    class DisplayPanel extends JPanel {
        public void paintComponent(Graphics g) {
            super.paintComponent(g);

            if(focussed)
                g.setColor(Color.cyan);
            else
                g.setColor(Color.lightGray);

            int width = getSize().width;    //Anchura del applet
            int height = getSize().height;  //Altura del applet
            g.drawRect(0, 0, width-1, height-1);
            g.drawRect(0, 0, width-3, height-3);
            g.drawRect(0, 0, width-5, height-5);

            if (!focussed) {
                g.setColor(Color.magenta);
                g.drawString("Click to activate",100,120);
                g.drawString("Use arrow keys to change azimuth and elevation",100,150);
            }
            else{
                double theta = Math.PI * azimuth / 180.0;
                double phi = Math.PI * elevation / 180.0;
                float cosT = (float)Math.cos( theta );
                float sinT = (float)Math.sin( theta );
                float cosP = (float)Math.cos( phi );
                float sinP = (float)Math.sin( phi );
                float cosTcosP = cosT*cosP;
                float cosTsinP = cosT*sinP;
                float sinTcosP = sinT*cosP;
                float sinTsinP = sinT*sinP;

                Point[] points;
                points = new Point[vertices.length];
                int j;
                int scaleFactor = width/8;
                float near = 3; // distance from eye to near plane
                float nearToObj = 1.5f;  // distance from near plane to center of object
                for ( j = 0; j < vertices.length; ++j ) {
                    int x0 = vertices[j].x;
                    int y0 = vertices[j].y;
                    int z0 = vertices[j].z;

                    // compute an orthographic projection
                    float x1 = cosT*x0 + sinT*z0;
                    float y1 = -sinTsinP*x0 + cosP*y0 + cosTsinP*z0;
                    float z1 = cosTcosP*z0 - sinTcosP*x0 - sinP*y0;

                    // now adjust things to get a perspective projection
                    x1 = x1*near/(z1+near+nearToObj);
                    y1 = y1*near/(z1+near+nearToObj);

                    // the 0.5 is to round off when converting to int
                    points[j] = new Point(
                       (int)(width/2 + scaleFactor*x1 + 0.5),
                       (int)(height/2 - scaleFactor*y1 + 0.5)
                    );
                }

                // draw the wireframe
                g.setColor( Color.black );
                g.fillRect( 0, 0, width, height );
                g.setColor( Color.white );
                for ( j = 0; j < edges.length; ++j ) {
                    g.drawLine(
                        points[ edges[j].a ].x, points[ edges[j].a ].y,
                        points[ edges[j].b ].x, points[ edges[j].b ].y
                    );
                }
            }
        }   // end paintComponent
    }   // end nested class DisplayPanel


   // ------------------- Event handling methods ----------------------
    public void focusGained(FocusEvent evt) {
        focussed = true;
        canvas.repaint();
    }
    public void focusLost(FocusEvent evt) {
        focussed = false;
        canvas.repaint();
    }
    public void keyTyped(KeyEvent evt) {}

    public void keyPressed(KeyEvent evt) {

        // keyboard code for the key that was pressed
        int key = evt.getKeyCode();

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
    }   // end keyPressed

    // empty method, required by the KeyListener Interface
    public void keyReleased(KeyEvent evt){}

    public void mousePressed(MouseEvent evt) {
        canvas.requestFocus();
    }

    // Required by the MouseListenerinterface
    public void mouseEntered(MouseEvent evt){}
    public void mouseExited(MouseEvent evt){}
    public void mouseReleased(MouseEvent evt){}
    public void mouseClicked(MouseEvent evt){}
    public void mouseDragged(MouseEvent e){}
}
