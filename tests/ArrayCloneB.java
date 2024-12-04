public class ArrayCloneB {
    public static void main(String[] args) {
        float[] arr = {1.2f, 2.3f};

        float[] brr = arr.clone();
        
        for (float b : brr) {
            System.out.println(b);
        }
    }
}
