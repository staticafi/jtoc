public class ClassObject {
    private static int secretNum = 10;
    private double price;

    public ClassObject() {
        price = 10.5;
    }

    public static void main(String[] args) {
        ClassObject c = new ClassObject();
        System.out.println(ClassObject.secretNum);
        System.out.println(c.price);
    }
}