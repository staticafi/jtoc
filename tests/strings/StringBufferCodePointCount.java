public class StringBufferCodePointCount {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Sweetest Perfection");

        int b = a.codePointCount(0, 10);
        System.out.println(b);
    }
}
