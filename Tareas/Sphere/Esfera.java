// Team Integrants:
// Francisco Rocha A01730560
// Alejandro Ubeto Yañez A01734977
// Omar Jiménez Armendáriz A01732097

import javax.swing.JFrame;
import javax.swing.JPanel;

class Esfera{
      //We receive as parameters the radius of the sphere, the number of meridians and the number of parallels
      public static void main(String[] args) {
            double radius = Double.parseDouble(args[0]);
            int meridians = Integer.parseInt(args[1]);
            int parallels = Integer.parseInt(args[2]);
            System.out.println("Radius: " + radius + " Meridians: " + meridians + " Parallels: " + parallels);
            Drawing applet = new Drawing();
            applet.init(radius, meridians, parallels);
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