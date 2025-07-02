import java.util.Scanner;

public class StringValid {

    public static String validator(String word, String delimiter, int index) {
        
        try {
            String[] parts = word.split(java.util.regex.Pattern.quote(delimiter), -1);
            if (index < 0 || index >= parts.length) {
                return word;
            }
            return parts[index];
        } catch (Exception e) {
            return word;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String word = sc.nextLine();
        String delimiter = sc.nextLine();
        int index = sc.nextInt();

        String extractedWord = validator(word, delimiter, index);
        System.out.println(extractedWord);

        sc.close();
    }
}