import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class TwoZeroFourEight {

    public static Pos findBFSScore(int[][] lis) {
    	String[] moves = new String[]{"U", "R", "D", "L"};
        Queue<Pos> q = new LinkedList<Pos>();
        Pos res = new Pos (0, null, null);
        Pos pos = new Pos (0, new ArrayList<String>(), lis);
        q.add(pos);
        
        while (!q.isEmpty()) {
        	Pos secondary;
        	Pos initial = q.remove();
            if (initial.noOfTurns() < 3) {
                for (int p = 0; p < moves.length; p = p + 1) {
                    Tuple box = stepCheck(initial.stateList(), moves[p]);
                    int sum = box.getInt();
                    if (sum >= 0) {
                        List<String> currentState = initial.direction();
                        List<String> updatedState = new ArrayList<String>(currentState);
                        updatedState.add(moves[p]);
                        sum += initial.totalSum();
                        secondary = new Pos(sum, updatedState, box.getArr());
                        q.add(secondary);
                        if (secondary.totalSum() >= res.totalSum()) {
                            res = secondary;
                        }
                    }
                }
            }
        }

        return res;
    }

    private static Tuple stepCheck(int[][] lis, String nextMove) {
        Tuple box = newStateList(lis, nextMove);
        int[][] res = box.getArr();
        boolean next = (box.getInt() == 1);
        box = combineSum(res, nextMove);
        res = box.getArr();
        int sum = box.getInt();
        box = newStateList(res, nextMove);
        if (sum == 0 && next == false) {
            return new Tuple(box.getArr(), -1);
        } else {
            addTwoHere(box.getArr());
            return new Tuple(box.getArr(), sum);
        }
    }

    private static int[][] addTwoHere(int[][] lis) {
        for (int p = 0; p < 4; p = p + 1) {
            for (int q = 0; q < 4; q = q + 1) {
                if (lis[p][q] == 0) {
                    lis[p][q] = 2;
                    return lis;
                }
            }
        }
        return lis;
    }

    private static Tuple combineSum(int[][] lis, String nextMove) {
        int[][] res = new int[4][4];
        int sum = 0;
        if (nextMove.equalsIgnoreCase("U")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 0;
                for (int q = 0; q < 3; q = q + 1) {
                    if (lis[q][p] == lis[q + 1][p]) {
                        sum += lis[q][p] * 2;
                        res[loc][p] = lis[q][p] * 2;
                        lis[q + 1][p] = 0;
                        loc++;
                    } else if (lis[q][p] != lis[q + 1][p]) {
                        res[loc][p] = lis[q][p];
                        loc++;
                    }
                }
                res[3][p] = lis[3][p];
            }
        } else if (nextMove.equalsIgnoreCase("D")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 3;
                for (int q = 3; q > 0; q = q - 1) {
                    if (lis[q][p] == lis[q - 1][p]) {
                        sum += lis[q][p] * 2;
                        res[loc][p] = lis[q][p] * 2;
                        lis[q - 1][p] = 0;
                        loc--;
                    } else if (lis[q][p] != lis[q - 1][p]) {
                        res[loc][p] = lis[q][p];
                        loc--;
                    }
                }
                res[0][p] = lis[0][p];
            }
        } else if (nextMove.equalsIgnoreCase("L")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 0;
                for (int q = 0; q < 3; q = q + 1) {
                    if (lis[p][q] == lis[p][q + 1]) {
                        sum += lis[p][q] * 2;
                        res[p][loc] = lis[p][q] * 2;
                        lis[p][q + 1] = 0;
                        loc++;
                    } else if (lis[p][q] != lis[p][q + 1]) {
                        res[p][loc] = lis[p][q];
                        loc++;
                    }
                }
                res[p][3] = lis[p][3];
            }
        } else if (nextMove.equalsIgnoreCase("R")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 3;
                for (int q = 3; q > 0; q = q - 1) {
                    if (lis[p][q] == lis[p][q - 1]) {
                        sum += lis[p][q] * 2;
                        res[p][loc] = lis[p][q] * 2;
                        lis[p][q - 1] = 0;
                        loc--;
                    } else if (lis[p][q] != lis[p][q - 1]) {
                        res[p][loc] = lis[p][q];
                        loc--;
                    }
                }
                res[p][0] = lis[p][0];
            }
        } 
        return new Tuple(res, sum);
    }

    private static Tuple newStateList(int[][] lis, String nextMove) {
        int[][] res = new int[4][4];
        int counter = 0;
        boolean next = false;
        if (nextMove.equalsIgnoreCase("U")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 0;
                for (int q = 0; q < 4; q = q + 1) {
                    boolean empty = false;
                    next = false;
                    if (lis[q][p] != 0) {
                        res[loc][p] = lis[q][p];
                        loc++;
                        if (empty) {
                            next = true;
                        }
                    } else {
                        empty = true;
                    }
                }
                if (next) {
                    counter++;
                }
            }
        } else if (nextMove.equalsIgnoreCase("D")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 3;
                for (int q = 3; q >= 0; q = q - 1) {
                    boolean empty = false;
                    next = false;
                    if (lis[q][p] != 0) {
                        res[loc][p] = lis[q][p];
                        loc--;
                        if (empty) {
                            next = true;
                        }
                    } else {
                        empty = true;
                    }
                }
                if (next) {
                    counter++;
                }
            }
        } else if (nextMove.equalsIgnoreCase("L")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 0;
                for (int q = 0; q < 4; q = q + 1) {
                    boolean empty = false;
                    next = false;
                    if (lis[p][q] != 0) {
                        res[p][loc] = lis[p][q];
                        loc++;
                        if (empty) {
                            next = true;
                        }
                    } else {
                        empty = true;
                    }
                }
                if (next) {
                    counter++;
                }
            }
        } else if (nextMove.equalsIgnoreCase("R")) {
            for (int p = 0; p < 4; p = p + 1) {
                int loc = 3;
                for (int q = 3; q >= 0; q = q - 1) {
                    boolean empty = false;
                    next = false;
                    if (lis[p][q] != 0) {
                        res[p][loc] = lis[p][q];
                        loc--;
                        if (empty) {
                            next = true;
                        }
                    } else {
                        empty = true;
                    }
                }
                if (next) {
                    counter++;
                }
            }
        } 
        if (counter != 4) {
            return new Tuple(res, 1);
        } else {
            return new Tuple(res, -1);
        }
    }
}