public class Stringifier {
    private static String constantName = "ideally something with x";
    private String varName;

    public Stringifier(String arg) {
        varName = arg;
    }

    public String getVarName() {
        return varName;
    }

    public String suffix(char ch) {
        return constantName + ch;
    }

    public String suffix(String str) {
        return constantName + str;
    }

    public static void main(String[] args) {
        Stringifier s = new Stringifier("papľuh");

        System.out.println(s.suffix(s.getVarName()));
        System.out.println(s.suffix('x'));
    }
}