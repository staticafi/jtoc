import java.util.Random;


public class Exception {
    public static void main(String[] args) {
        Random r = new Random();
        try {
            int a = 10 / r.nextInt(1);
            System.out.println(a);
        } catch (ArithmeticException exc) {
            System.out.println(exc);
        }
    }
}
