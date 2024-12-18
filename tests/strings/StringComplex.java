public class StringComplex {
    public static void main(String[] args) {
        // Create a String instance
        String str = "  Hello, World!  ";
        String anotherStr = "Java Programming";

        // Basic properties
        System.out.println(str.length());
        System.out.println(str.isEmpty());

        // System.out.println(str.equals(anotherStr));
        System.out.println(str.equalsIgnoreCase("  hello, world!  "));
        System.out.println(str.compareTo(anotherStr));

        // Searching and matching
        System.out.println(str.contains("World"));
        System.out.println(str.startsWith("  Hello"));
        System.out.println(str.endsWith("World!  "));
        System.out.println(str.indexOf('o'));

        // Modifications and transformations
        System.out.println(str.toUpperCase());
        System.out.println(str.toLowerCase());
        System.out.println(str.trim());

        // StringBuilder/StringBuffer interaction
        StringBuilder sb = new StringBuilder("Dynamic ");
        sb.append("String");
        System.out.println(sb.toString());

        // Empty check
        String emptyStr = "";
        System.out.println(emptyStr.isEmpty());

        // Concatenation
        System.out.println(str.concat(" Enjoy learning Java!"));
    }
}