public class ArrayCloneD {
    public static void main(String[] args) {
        short[] arr = {0, 0, 2};

        short[] brr = arr.clone();
        
        for (short b : brr) {
            System.out.println(b);
        }
    }
}
