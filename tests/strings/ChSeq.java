public class ChSeq {
    public static void main(String[] args) {
        // Using a String as a CharSequence
        CharSequence charSeq = "Hello, World!";

        // Accessing methods from the CharSequence interface
        System.out.println(charSeq.length());
        System.out.println(charSeq.charAt(7));
        System.out.println(charSeq.toString());
    }
}
