public class StringBufferAppendA {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Abcd");

        StringBuffer b = a.append('e');
        System.out.println(b.toString());
    }
}
