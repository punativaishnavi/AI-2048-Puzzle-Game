import java.io.*;
import java.util.List;

public class TwoZeroFourEightMain {

    public static void main(String[] args) {
        int[][][] matrix = convertToList();
        Pos pos;
        Pos[] position = new Pos[matrix.length];
        for (int p = 0; p < matrix.length; p++) {
            pos = TwoZeroFourEight.findBFSScore(matrix[p]);
            position[p] = pos;
        }
        output(position);
    }

    private static void output(Pos[] nodes) {
        File file = new File("2048_out.txt");
        try {
            FileWriter toFile = new FileWriter(file, false);
            int score;
            List<String> path;
            for (int p = 0; p < nodes.length; p++) {
                score = nodes[p].totalSum();
                path = nodes[p].direction();
                toFile.write(score + "," + path.get(0) + "," + path.get(1) + "," + path.get(2) + "\n");
            }
            toFile.close();
        } catch (IOException ioEx) {
            System.out.println("IO error occurred.");
        }
    }

    @SuppressWarnings("resource")
	private static int[][][] convertToList() {
        int[][][] result;
        File input = new File("2048_in.txt");
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(input));
        } catch (FileNotFoundException notFound) {
            System.out.println("File not found");
            return null;
        }
        String st;
        try {
            st = br.readLine();
            int numTestCases = Integer.parseInt(st);
            result = new int[numTestCases][4][4];
            for (int p = 0; p < numTestCases * 4; p++) {
                st = br.readLine();
                String[] strArr = st.split(",", 4);
                for (int q = 0; q < 4; q++) {
                    result[p/4][p%4][q] = Integer.parseInt(strArr[q]);
                }
            }
        } catch (IOException ioEx) {
            System.out.println("IO error occurred.");
            return null;
        }
        return result;
    }
}
