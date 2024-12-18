public class StringBufferAppendB {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Abcd");
        StringBuffer c = new StringBuffer("ef");

        StringBuffer b = a.append(c);
        System.out.println(b.toString());
    }
}
