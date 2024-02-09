package ProgrammingAssignment1;
import java.util.*;

public class Main {

    public static class Item {
        String name;
        int value;
        int cost;

        Item(String name, int value, int cost){
            this.name = name;
            this.value = value;
            this.cost = cost;
        }
    }
    public static void main(String[] args) {
        Scanner kb = new Scanner(System.in);

        String[] lineOne = kb.nextLine().split("\\s+");
        int targetValue = Integer.parseInt(lineOne[0]);
        int budget = Integer.parseInt(lineOne[1]);
        String flag = lineOne[2];
        ArrayList<Item> itemList = new ArrayList<>();

        while(kb.hasNextLine()){
            String[] inputLine = kb.nextLine().split("\\s+");
            String name = inputLine[0];
            int value = Integer.parseInt(inputLine[1]);
            int cost = Integer.parseInt(inputLine[2]);
            itemList.add(new Item(name, value, cost));
        }
        iterativeDeepening(itemList, targetValue, budget, flag);
    }


