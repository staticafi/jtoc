public class JavaSpecificC {
    private String some_str = "Standard string";

    public String getSomeString() {
        return some_str;
    }

    public static void main(String[] args) {
        JavaSpecificC jspec = new JavaSpecificC();
        System.out.println(jspec.getSomeString());
    }
}