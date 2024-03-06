//package ProgrammingAssignment1;
import java.util.*;

public class BudgetHC {
    public static class Item {
        String name;
        int value;
        int cost;

        public Item(String name, int value, int cost){
            this.name = name;
            this.value = value;
            this.cost = cost;
        }
    }
    public static class errorObj{
        int error;
        int value;
        int cost;

        public errorObj(int error, int value, int cost){
            this.error = error;
            this.value = value;
            this.cost = cost;
        }
    }

    public static boolean solutionFound = false;
    public static void main(String[] args) {

        Scanner kb = new Scanner(System.in);

        String[] lineOne = kb.nextLine().split("\\s+");
        int targetValue = Integer.parseInt(lineOne[0]);
        int budget = Integer.parseInt(lineOne[1]);
        String flag = lineOne[2];
        int restarts = Integer.parseInt(lineOne[3]);
        ArrayList<Item> itemList = new ArrayList<>();

        while(kb.hasNextLine()){
            String[] inputLine = kb.nextLine().split("\\s+");
            String name = inputLine[0];
            int value = Integer.parseInt(inputLine[1]);
            int cost = Integer.parseInt(inputLine[2]);
            itemList.add(new Item(name, value, cost));
        }
        hillClimbing(itemList, targetValue, budget, flag, restarts);

        if(!solutionFound){
            System.out.println("No Solution");
        }
    }

    public static void hillClimbing(ArrayList<Item> itemList, int targetVal, int budget, String flag, int restarts){
        Random random = new Random();

        for(int i = 0; i <= restarts; i++){
            List<Item> currState = new ArrayList<>();
            int initialStateSize = 1 + random.nextInt(itemList.size());


            for(int j = 0; j < initialStateSize; j++){
                Item randomItem = itemList.get(random.nextInt(itemList.size()));
                if(!currState.contains(randomItem))
                    currState.add(randomItem);
            }

            errorObj current = getErrorObj(currState, targetVal, budget);

            if(flag.equals("V")){
                System.out.println("Randomly chosen starting state:");
                printVerbose(currState, current.value, current.cost, current.error);
                System.out.println("Neighbors:");
            }

            while(true){
                List<List<Item>> neighbors = getNeighbors(currState, itemList);
                List<Item> bestNeighbor = null;
                int bestNeighborError = current.error;

                for(List<Item> neighbor : neighbors){
                    errorObj currNeighbor = getErrorObj(neighbor, targetVal, budget);

                    if(flag.equals("V")){
                        printVerbose(neighbor, currNeighbor.value, currNeighbor.cost, currNeighbor.error);
                    }

                    if(currNeighbor.value >= targetVal && currNeighbor.cost <= budget){
                        if(flag.equals("V"))
                            System.out.println();
                        System.out.println("Found Solution: ");
                        solutionFound = true;
                        printVerbose(neighbor, currNeighbor.value, currNeighbor.cost, currNeighbor.error);
                        return;
                    }

                    if(currNeighbor.cost <= budget && currNeighbor.error <= bestNeighborError){
                        bestNeighbor = neighbor;
                        bestNeighborError = currNeighbor.error;
                    }
                }

                if(bestNeighbor == null || bestNeighbor.equals(currState)){
                    if(flag.equals("V"))
                        System.out.println("Search Failed.\n");
                    break;
                }
                else{
                    currState = bestNeighbor;
                    current = getErrorObj(currState, targetVal, budget);
                    if(flag.equals("V")){
                        System.out.print("\nMove to " );
                        printVerbose(currState, current.value, current.cost, current.error);
                        System.out.println("Neighbors:");
                    }
                }
            }
        }
    }
    public static errorObj getErrorObj(List<Item> state, int targetValue, int budget){
        int totalValue = 0;
        int totalCost = 0;
        for(Item item : state){
            totalValue += item.value;
            totalCost += item.cost;
        }
        int error = Math.max(0, targetValue - totalValue) + Math.max(0, totalCost - budget);
        return new errorObj(error, totalValue, totalCost);
    }

    public static List<List<Item>> getNeighbors(List<Item> currState, List<Item> itemList){
        List<List<Item>> neighbors = new ArrayList<>();
        for(Item item : itemList){
            List<Item> newState = new ArrayList<>(currState);

            if(newState.contains(item)){
                newState.remove(item);
            }
            else{
                newState.add(item);
            }
            neighbors.add(newState);
        }
        return neighbors;
    }
    public static void printVerbose(List<Item> path, int currVal, int currCost, int currError){
        StringJoiner joiner = new StringJoiner(" ");
        for(Item item : path){
            joiner.add(item.name);
        }
        System.out.println("{" + joiner + "}. Value = " + currVal + ". Cost = " + currCost + ". Error = " + currError + ".");
    }
}
