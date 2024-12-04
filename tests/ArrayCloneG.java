public class ArrayCloneG {
    public static void main(String[] args) {
        double[] arr = {5.6, 8.4, 9.9, 12.74};

        double[] brr = arr.clone();
        
        for (double b : brr) {
            System.out.println(b);
        }
    }
}
