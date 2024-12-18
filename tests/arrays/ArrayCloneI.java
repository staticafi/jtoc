public class ArrayCloneI {
    public static void main(String[] args) {
        char[] arr = {'n', 'o'};

        char[] brr = arr.clone();
        
        for (char b : brr) {
            System.out.println(b);
        }
    }
}
