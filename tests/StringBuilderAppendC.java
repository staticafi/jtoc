public class StringBuilderAppendC {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Abcd");
        String c = "efghij";

        StringBuilder b = a.append(c);
        System.out.println(b.toString());
    }
}
