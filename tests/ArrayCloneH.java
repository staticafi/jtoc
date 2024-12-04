public class ArrayCloneH {
    public static void main(String[] args) {
        boolean[] arr = {true, false, false};

        boolean[] brr = arr.clone();
        
        for (boolean b : brr) {
            System.out.println(b);
        }
    }
}
