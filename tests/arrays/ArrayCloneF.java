public class ArrayCloneF {
    public static void main(String[] args) {
        String[] arr = {"Sister", "of", "Night"};

        String[] brr = arr.clone();
        
        for (String b : brr) {
            System.out.println(b);
        }
    }
}
