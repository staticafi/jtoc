public class ArrayCloneE {
    public static void main(String[] args) {
        int[] arr = {-1, 20, 64};

        int[] brr = arr.clone();
        
        for (int b : brr) {
            System.out.println(b);
        }
    }
}
