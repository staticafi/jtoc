public class ExceptionC {
    public void throwFunc() throws IllegalArgumentException {
        throw new IllegalArgumentException();
    }
    public static void main(String[] args) {
        ExceptionB e = new ExceptionB();
        e.throwFunc();
        System.out.println("This should not print");
    }
}
