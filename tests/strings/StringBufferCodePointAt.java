public class StringBufferCodePointAt {
    public static void main(String[] args) {
        StringBuffer a = new StringBuffer("Sweetest Perfection");

        int b = a.codePointAt(1);
        System.out.println(b);
    }
}
