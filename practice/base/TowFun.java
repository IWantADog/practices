package practice.base;

class Base {
    void func1(){
        System.out.println("base: this is func1");
    }

    void run(){
        func1();
    }
}

class SubBase extends Base {
    @Override
    void func1() {
        System.out.println("SubBase: this is func1");
    }
}


public class TowFun {
    public static void main(String[] args) {
        Base a = new SubBase();
        a.run();
    }    
}
