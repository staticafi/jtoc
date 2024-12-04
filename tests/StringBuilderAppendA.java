public class StringBuilderAppendA {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Abcd");

        StringBuilder b = a.append('e');
        System.out.println(b.toString());
    }
}
