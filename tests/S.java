public class S {
    public static void main(String[] args) {
        // Create a String instance
        String str = "  Hello, World!  ";
        String anotherStr = "Java Programming";

        // Basic properties
        System.out.println(str.length());
        System.out.println(str.isEmpty());

        // // Character operations
        // System.out.println(str.charAt(1));
        // System.out.println(str.codePointAt(1));
        // System.out.println(str.codePointBefore(1));
        // System.out.println(str.codePointCount(0, 5));

        // Comparison operations
        // System.out.println(str.equals(anotherStr));
        System.out.println(str.equalsIgnoreCase("  hello, world!  "));
        System.out.println(str.compareTo(anotherStr));

        // Searching and matching
        System.out.println(str.contains("World"));
        System.out.println(str.startsWith("  Hello"));
        System.out.println(str.endsWith("World!  "));
        System.out.println(str.indexOf('o'));
        //System.out.println(str.lastIndexOf('o'));

        // Modifications and transformations
        System.out.println(str.toUpperCase());
        System.out.println(str.toLowerCase());
        System.out.println(str.trim());
        //System.out.println(str.replace("World", "Java"));

        // StringBuilder/StringBuffer interaction
        StringBuilder sb = new StringBuilder("Dynamic ");
        sb.append("String");
        System.out.println(sb.toString());

        // Empty check
        String emptyStr = "";
        System.out.println(emptyStr.isEmpty());

        // Concatenation
        System.out.println(str.concat(" Enjoy learning Java!"));

        // Chaining operations
        //String result = str.trim().toUpperCase().replace("HELLO", "HI");
        //System.out.println(result);
    }
}