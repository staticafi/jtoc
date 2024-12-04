public class StringBuilderAppendB {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Abcd");
        CharSequence c = "efg";

        StringBuilder b = a.append(c);
        System.out.println(b.toString());
    }
}
