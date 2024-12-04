public class ArrayCloneA {
    public static void main(String[] args) {
        byte[] arr = {-1, 20, 64};

        byte[] brr = arr.clone();
        
        for (byte b : brr) {
            System.out.println(b);
        }
    }
}
