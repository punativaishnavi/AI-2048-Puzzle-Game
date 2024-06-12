import java.util.List;

public class Pos {
    private List<String> directionStore;
    private int directionSum;
    private int[][] allStatesList;

    public Pos (int directionSum, List<String> directionStore, int[][] allStatesList) {
        this.directionStore = directionStore;
        this.directionSum = directionSum;
        this.allStatesList = allStatesList;}
    public int totalSum() { 
    	return this.directionSum; 
    	}
    public List<String> direction() {
    	return this.directionStore; 
    	}
    public int noOfTurns() { 
    	return this.directionStore.size(); 
    	}
    public int[][] stateList() { 
    	return this.allStatesList; 
    	}
}
