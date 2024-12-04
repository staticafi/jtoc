public class StringBuilderAppendE {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Abcd");
        int c = '.';

        StringBuilder b = a.appendCodePoint(c);
        System.out.println(b.toString());
    }
}
