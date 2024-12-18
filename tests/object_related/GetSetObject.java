public class GetSetObject {
    private int attribute;

    public GetSetObject(int attr) {
        attribute = attr;
    }

    public void setAttribute(int newAttr) {
        attribute = newAttr;
    }

    public int getAttribute() {
        return attribute;
    }

    public static void main(String[] args) {
        GetSetObject obj = new GetSetObject(20);
        
        System.out.println(obj.getAttribute());
        obj.setAttribute(35);
        System.out.println(obj.getAttribute());
    }
}