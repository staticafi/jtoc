public class StringBufferAppendC {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Abcd");
        String c = "efghij";

        StringBuffer b = a.append(c);
        System.out.println(b.toString());
    }
}
