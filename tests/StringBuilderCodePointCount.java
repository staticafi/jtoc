public class StringBuilderCodePointCount {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Sweetest Perfection");

        int b = a.codePointCount(0, 10);
        System.out.println(b);
    }
}
