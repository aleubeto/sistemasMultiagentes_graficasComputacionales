/*
Compila tu programa
  javac Main.java

Ejecuta tu class Main con parámetros
  java Main hola 123
*/

class Main {
    public static void main(String[] args) {

      // ¡Tu primer "Hello World" en Java!
      System.out.println("Hello world");
  
      // ¡Tu primer ciclo for en Java!
      for (int i = 0; i < 10; i++) {
        System.out.println(i);
      }
  
      // Recorriendo lista de strings "args" con un for
      for (int i = 0; i < args.length; i++) {
        System.out.println(args[i]);
      }
    }
  }