public class ExceptionA {
    public static void main(String[] args) {
        try {
            throw new ArithmeticException();
        } catch (ArithmeticException exc) {
            System.out.println(exc);
        }
    }
}
