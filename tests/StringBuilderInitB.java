public class StringBuilderInitB {
    public static void main(String[] args) {
        CharSequence a = "World in My Eyes";
        StringBuilder b = new StringBuilder(a);

        System.out.println(b.toString());
    }
}
