interface StringFunction {
    String run(String str);
}
  
public class Ltest {
    public static void main(String[] args) {
        StringFunction exclaim = (s) -> s + "!";
        printFormatted("Hello", exclaim);
    }
    
    public static void printFormatted(String str, StringFunction format) {
        String result = format.run(str);
        System.out.println(result);
    }
}