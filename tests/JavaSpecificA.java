public class JavaSpecificA {
    public JavaSpecificA() {
        System.out.println("Called from Constructor");
    }
    public static void main(String[] args) {
        new JavaSpecificA();
    }
}