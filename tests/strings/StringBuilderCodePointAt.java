public class StringBuilderCodePointAt {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Sweetest Perfection");

        int b = a.codePointAt(1);
        System.out.println(b);
    }
}
