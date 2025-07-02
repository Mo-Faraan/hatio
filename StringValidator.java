import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class StringValidator {

    public static String Validator(String word, String delimiter, int index){
        List<Integer> positions = new ArrayList<>();
        List<String> parts = new ArrayList<>();

        for (int i = 0; i < word.length(); i++) {
            if (word.charAt(i) == delimiter.charAt(0)) {
            positions.add(i);
            }
        }
        System.out.println(positions);
        parts.add(word.substring(0, positions.get(0)));
        for (int i = 0; i < positions.size() - 1; i++) {
            int start = positions.get(i);
            int end = positions.get(i + 1);
            parts.add(word.substring(start+1, end));
        }
        parts.add(word.substring(positions.get((positions.size() - 1))+1));
        System.out.println(parts);
        return parts.get(index);
    }
        
    public static void main(String args[]){

        Scanner sc = new Scanner(System.in);
        String word = sc.nextLine();
        String delimiter = sc.nextLine();
        int index = sc.nextInt();
        try {
            String extractedWord = Validator(word,delimiter,index);
            System.out.println(extractedWord);
        } catch (Exception e) {
            System.out.println(word);
        }
        

    }
    
}
