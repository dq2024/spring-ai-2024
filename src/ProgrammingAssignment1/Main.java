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
        boolean result = false;
        for(int depth = 1; depth < itemList.size(); depth++){
            if(flag.equals("V")){
                if(depth == 1){
                    System.out.println("Depth = " + depth + ".");
                }
                else{
                    System.out.println("\nDepth = " + depth + ".");
                }
            }
            result = search(itemList, new ArrayList<>(), 0, 0, 0, depth, targetVal, budget, flag);
            if(result){
                break;
            }
        }
        if(!result && flag.equals("C")){
            System.out.println("No Solution");
        }
    }
    public static boolean search(List<Item> itemList, List<Item> path,
                                 int currVal, int currCost, int idx, int depth,
                                 int targetVal, int budget, String flag){
        if(depth == 0 || idx == itemList.size()){
            if(!path.isEmpty() && currCost <= budget){
                if(flag.equals("V")){
                    printVerbose(path, currVal, currCost);
                }
                // we have found goal state
                if(currVal >= targetVal){
                    System.out.println("\nFound solution " + path + ". Value = " + currVal + ". Cost = " + currCost + ".");
                    return true;
                }

            }
            return false;
        }

        if(idx >= itemList.size()){
            return false;
        }

        Item currItem = itemList.get(idx);

        if(currCost + currItem.cost <= budget){
            path.add(currItem);
            if(search(itemList, new ArrayList<>(path), currVal + currItem.value, currCost + currItem.cost,
                    idx + 1, depth - 1, targetVal, budget, flag)){
                return true;
            }
            // backtracking step
            path.remove(path.size() - 1);
        }

        if(search(itemList, new ArrayList<>(path), currVal, currCost, idx + 1, depth,
                targetVal, budget, flag)){
            return true;
        }
        return false;
    }
    public static void printVerbose(List<Item> path, int currVal, int currCost){
        StringJoiner joiner = new StringJoiner(" ");
        for(Item item : path){
            joiner.add(item.name);
        }
        System.out.println("{" + joiner.toString() + "}. Value = " + currVal + ". Cost = " + currCost + ".");
    }
}
/*
INITIAL THOUGHTS:


iterativeDeepening(itemList, targetValue, budget, flag):
    - loop from 1 to N, the variable here will be depth
    - print out Depth 1: Depth 2: etc, before calling our modified dfs search

dfs():
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

