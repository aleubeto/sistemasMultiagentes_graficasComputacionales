/*
Omar Jiménez Armendáriz - A01732097
Francisco Rocha Juárez - A01730560
Alejandro Ubeto Yañez - A01734977
*/

class Rectangle{
    public static void main(String[] args){
        int nFilas = Integer.valueOf(args[0]);
        int nColumnas = Integer.valueOf(args[1]);
        linea(nColumnas);
        for (int i = 0; i < nFilas - 2; i++){
            System.out.print("+ ");
            for (int j = 0; j < nColumnas - 2; j++){
                System.out.print("  ");
            }
            System.out.print("+\n");  
        }
        linea(nColumnas);
    }

    private static void linea (int nTamano) {
        for (int i = 0; i < nTamano; i++){
            System.out.print("+ ");
        }
        System.out.print('\n');     
    }
}