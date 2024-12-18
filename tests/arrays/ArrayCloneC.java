public class ArrayCloneC {
    public static void main(String[] args) {
        long[] arr = {100000L, 200000L, 300000L};

        long[] brr = arr.clone();
        
        for (long b : brr) {
            System.out.println(b);
        }
    }
}
