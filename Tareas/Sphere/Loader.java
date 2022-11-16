import javax.swing.JFrame;
import javax.swing.JPanel;

class Loader{
      //We receive as parameters the radius of the sphere, the number of meridians and the number of parallels
      public static void main(String[] args) {

            Sphere applet = new Sphere();
            applet.init();
            final JFrame frame = new JFrame("Sphere Viewer");
            frame.setContentPane(applet.getContentPane());
            frame.setJMenuBar(applet.getJMenuBar());
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(800, 600);
            frame.setLocation(100, 100);
            frame.setVisible(true);
            applet.start();
      }
}