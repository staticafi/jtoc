public class ArrayComplex {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};

        System.out.println(numbers[2]);
        for (int i = 0; i < numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        numbers[2] = 10;
        for (int num : numbers) {
            System.out.println(num);
        }
    }
}
