package practice.base;


/**
 * Rodent
 */
public class Rodent {

    void eat(){
        System.out.println("Rodent eat");
    }

    public static void main(String[] args) {
        Rodent[] a = {
            new Mouse(),
            new Gerbil(),
            new Hamster()
        };

        for(Rodent item: a){
            item.eat();
        }
    }
}

class Mouse extends Rodent {
    @Override
    void eat() {
        System.out.println("Mouse eat");
    }
}

class Gerbil extends Rodent {
    @Override
    void eat() {
        System.out.println("Gerbil eat");
    }
}

class Hamster extends Rodent {
    @Override
    void eat() {
        System.out.println("Hamster eat");
    }
}

