import java.awt.Color;
import java.awt.Graphics;
import javax.swing.JPanel;
import javax.swing.JFrame;

public class Graficos extends JPanel {

  // Método para pintar
  public void paintComponent(Graphics g) {
    super.paintComponent(g); // Setting inicial para pintar

    g.setColor(new Color(255, 0, 0)); // Pincel con pintura roja
    g.drawLine(0, 0, 300, 200); // Dibuja una línea de rojo

    g.setColor(new Color(0, 0, 255)); // Pincel con pintura azul
    g.drawArc(10, 10, 300, 300, 90, -180); // Dibuja una línea de azul
    g.drawString("Hola mundo", 200, 200); // Escribe "hola mundo" en azul

    for (int i = 0; i < 256; i++) { // Creando gradiente
      g.setColor(new Color(i, 0, 0));
      g.drawLine(0, i, 1000, i);
    }
  }

  // Función principal
  public static void main(String args[]) {
    Graficos panel = new Graficos();
    JFrame application = new JFrame();
    application.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    application.add(panel);
    application.setSize(1000, 600);
    application.setVisible(true);
  }
}