public class ExceptionC {
    public void throwFunc() throws IllegalArgumentException {
        throw new IllegalArgumentException();
    }
    public static void main(String[] args) {
        ExceptionC e = new ExceptionC();
        e.throwFunc();
        System.out.println("This should not print");
    }
}
