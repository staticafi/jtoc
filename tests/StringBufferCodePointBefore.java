public class StringBufferCodePointBefore {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Sweetest Perfection");

        int b = a.codePointBefore(3);
        System.out.println(b);
    }
}
