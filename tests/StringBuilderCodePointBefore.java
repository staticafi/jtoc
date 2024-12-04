public class StringBuilderCodePointBefore {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Sweetest Perfection");

        int b = a.codePointBefore(3);
        System.out.println(b);
    }
}
