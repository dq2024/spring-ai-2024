package ProgrammingAssignment1;
import java.util.*;

public class Main {

    public static class Item {
        String name;
        int value;
        int cost;

        Item(String name, int value, int cost) {
            this.name = name;
            this.value = value;
            this.cost = cost;
        }
        public String toString(){
            return this.name;
        }
    }

    public static void main(String[] args) {
        Scanner kb = new Scanner(System.in);

        String[] lineOne = kb.nextLine().split("\\s+");
        int targetValue = Integer.parseInt(lineOne[0]);
        int budget = Integer.parseInt(lineOne[1]);
        String flag = lineOne[2];
        ArrayList<Item> itemList = new ArrayList<>();

        while (kb.hasNextLine()) {
            String[] inputLine = kb.nextLine().split("\\s+");
            String name = inputLine[0];
            int value = Integer.parseInt(inputLine[1]);
            int cost = Integer.parseInt(inputLine[2]);
            itemList.add(new Item(name, value, cost));
        }
        iterativeDeepening(itemList, targetValue, budget, flag);
    }
    public static void iterativeDeepening(List<Item> itemList, int targetVal,
                                          int budget, String flag){
        int maxDepth = itemList.size();
        int depth = 0;
        boolean result = false;
        while(true){
            depth++;
            if(flag.equals("V")){
                if(depth == 1){
                    System.out.println("Depth = " + depth + ".");
                }
                else{
                    System.out.println("\nDepth = " + depth + ".");
                }
            }
            result = search(itemList, new ArrayList<>(), 0, 0, depth, targetVal, budget, flag);
            if(result){
                break;
            }
            if(depth == maxDepth){
                break;
            }
        }
        if(!result){
            if(flag.equals("V")){
                System.out.println();
            }
            System.out.println("No Solution");
        }

    }
    public static boolean search(List<Item> itemList, List<Item> path, int currVal, int currCost, int depth, int targetVal, int budget, String flag){

        if(currVal >= targetVal){
            if(flag.equals("C")){
                System.out.print("Found solution " );
            }
            else{
                System.out.print("\nFound solution " );
            }
            printVerbose(path, currVal, currCost);
            return true;
        }
        if(depth == 0 || currCost > budget){
            return false;
        }

        for(Item item : itemList){
            if(!path.isEmpty() && item.name.compareTo(path.get(path.size() - 1).name) <= 0){
                continue;
            }
            List<Item> nextPath = new ArrayList<>(path);
            nextPath.add(item);
            int nextVal = currVal + item.value;
            int nextCost = currCost + item.cost;

            if(nextCost <= budget){
                if(flag.equals("V")){
                    printVerbose(nextPath, nextVal, nextCost);
                }
                if(search(itemList, nextPath, nextVal, nextCost, depth - 1, targetVal, budget, flag)){
                    return true;
                }
            }
        }
        return false;
    }
    public static void printVerbose(List<Item> path, int currVal, int currCost){
        StringJoiner joiner = new StringJoiner(" ");
        for(Item item : path){
            joiner.add(item.name);
        }
        System.out.println("{" + joiner + "}. Value = " + currVal + ". Cost = " + currCost + ".");
    }
}
/*
INITIAL THOUGHTS, changes tbd:


iterativeDeepening(itemList, targetValue, budget, flag):
    - loop from 1 to N, the variable here will be depth
    - print out Depth 1: Depth 2: etc, before calling our modified dfs search

search():
    - base case when depth is 0, that means we need to check if the state is valid
        - if it is, AND it exceeds target value then we are done
        - if it is just a potential goal state, then we print accordingly and continue with our search

    - base case when index > itemList.size(), we have exceeded maximum size so we must return false


    - at this point, we can now check for potentially valid state
        - if the state is underbudget, then recursively call dfs with:
            - index + 1, depth - 1,

printVerbose:
    - print in verbose form
 */

