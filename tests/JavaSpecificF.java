class JavaSpecificE {
    private int[] arr = {1, 2, 3};

    public int[] getArr() {
        return arr;
    }

    public void printArr() {
        for (int i : getArr()) {
            System.out.println(i);
        }
    }
}

public class JavaSpecificF extends JavaSpecificE {
    public void specificForF() {
        System.out.println("JavaSpecificF method");
    }

    public static void main(String[] args) {
        JavaSpecificF jspec = new JavaSpecificF();

        jspec.printArr();
        jspec.specificForF();
    }
}