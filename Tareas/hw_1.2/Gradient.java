/* Omar Jiménez Armendáriz - A01732097
Francisco Rocha Juárez - A01730560
Alejandro Ubeto Yañez - A01734977 */
import java.awt.Color;
import java.awt.Graphics;
import javax.swing.JPanel;
import javax.swing.JFrame;

public class Gradient extends JPanel{
    public void paintComponent(Graphics g){
        super.paintComponent(g);

        for (int y = 0; y < 512; y++) {
            for (int x = 0; x < 512; x++) {
                g.setColor(new Color(255 - x/2, 255 - y/2, x/2));
                g.drawLine(x, y, x, y);
            }
        }
    }

    public static void main(String args[]){
        Gradient panel = new Gradient();
        JFrame application = new JFrame();
        application.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        application.add(panel);
        application.setSize(512, 512);
        application.setVisible(true);
    }
}
