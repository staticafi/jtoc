public class JavaSpecificB {
    private int some_number;

    public JavaSpecificB(int num) {
        some_number = num;
    }

    public static void main(String[] args) {
        JavaSpecificB jspec = new JavaSpecificB(42);
        System.out.println(jspec.some_number);
    }
}