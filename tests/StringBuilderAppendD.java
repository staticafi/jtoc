public class StringBuilderAppendD {
    public static void main(String[] args) {
        StringBuilder a = new StringBuilder("Abcd");
        StringBuffer c = new StringBuffer("ef");

        StringBuilder b = a.append(c);
        System.out.println(b.toString());
    }
}
