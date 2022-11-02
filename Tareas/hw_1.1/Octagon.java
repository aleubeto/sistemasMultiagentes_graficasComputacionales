/*
Omar Jiménez Armendáriz - A01732097
Francisco Rocha Juárez - A01730560
Alejandro Ubeto Yañez - A01734977
*/

class Octagon{
    public static void main(String[] args){
        int nTamano = Integer.valueOf(args[0]);
        linea(nTamano);
        for (int i = 1; i < nTamano; i++){
            for (int j = 1; j < nTamano - i; j++){
                System.out.print(" ");
            }
            System.out.print("+");
            for (int j = 0; j < 2 * i + 2 * nTamano - 3; j++){
                System.out.print(" ");
            }
            System.out.print("+\n");
        }

        for (int i = 0; i < nTamano - 1; i++){
            System.out.print("+ ");
            for (int j = 0; j < (2 * nTamano) - 3; j++){
                System.out.print("  ");
            }
            System.out.print("+\n");  
        }

        for (int i = 1; i < nTamano - 1; i++){
            for (int j = 0; j < i; j++){
                System.out.print(" ");
            }
            System.out.print("+");
            for (int j = 0; j < 2 * nTamano - 2 * i + 2 * nTamano - 5; j++){
                System.out.print(" ");
            }
            System.out.print("+\n");
        }
        linea(nTamano);
    }

    private static void linea (int nTamano) {
        for (int i = 0; i < nTamano - 1; i++){
            System.out.print(" ");
        }
        for (int i = 0; i < nTamano; i++){
            System.out.print("+ ");
        }
        System.out.print('\n');     
    }
}