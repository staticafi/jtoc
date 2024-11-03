public class LogicalC {
    public static void main(String[] args) {
        boolean t = true;
        boolean f = false;
        
        boolean d = t || f; 
        boolean e = d ? t : f;
        System.out.println(e);
    }
}