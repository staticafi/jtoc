public class JavaSpecificD {
    private String some_str = "Standard string";

    public String getSomeString() {
        return some_str;
    }

    public void setSomeString(String newString) {
        this.some_str = newString; 
    }

    public static void main(String[] args) {
        JavaSpecificD jspec = new JavaSpecificD();
        System.out.println(jspec.getSomeString());
        jspec.setSomeString("Newly set String");
        System.out.println(jspec.getSomeString());
    }
}