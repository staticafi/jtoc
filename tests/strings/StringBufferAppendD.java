public class StringBufferAppendD {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Abcd");
        int c = '.';

        StringBuffer b = a.appendCodePoint(c);
        System.out.println(b.toString());
    }
}
