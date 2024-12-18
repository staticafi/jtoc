public class StringBufferInitA {
    public static void main(String[] args) {
        String a = "World in My Eyes";
        StringBuffer b = new StringBuffer(a);

        System.out.println(b.toString());
    }
}
