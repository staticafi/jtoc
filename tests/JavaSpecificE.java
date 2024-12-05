public class JavaSpecificE {
    private String some_str = "Standard string";
    private int[] arr = {1, 2, 3};

    public int[] getArr() {
        return arr;
    }

    public String getSomeStr() {
        return some_str;
    }

    public void setMember(String newString) {
        this.some_str = newString; 
    }

    public void setMember(int[] newArray) {
        this.arr = newArray;
    }

    public void printArr() {
        for (int i : getArr()) {
            System.out.println(i);
        }
    }

    public static void main(String[] args) {
        JavaSpecificE jspec = new JavaSpecificE();
        int[] brr = {5, 6, 7, 8, 9};

        jspec.printArr();
        jspec.setMember(brr);
        jspec.printArr();
    }
}