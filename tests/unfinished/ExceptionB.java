public class ExceptionB {
    public void throwFunc() throws IllegalArgumentException {
        throw new IllegalArgumentException();
    }
    public static void main(String[] args) {
        ExceptionB e = new ExceptionB();

        try {
            e.throwFunc();
        } catch (IllegalArgumentException exc) {
            System.out.println(exc);
        } finally {
            System.out.println("Finally");
        }
    }
}
