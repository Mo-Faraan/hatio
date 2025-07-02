import java.util.Scanner;

public class FormatAmount {


    public static String shiftAmount(String amount, int decimal){

        long longAmount = Long.parseLong(amount);
        double rupees = longAmount/100.0;
        String strFormat = "%." + decimal + "f";
        String result = String.format(strFormat, rupees);

        return result; 
    }

    public static String formatAmount(String format, String amount){

        int decimal;
        String result = null;

        try{
            if((format == null) || (format == "")){
                result = amount;
            }
            
            else if ("rs".equals(format.toLowerCase())){

                decimal = 2;
                result = shiftAmount(amount, decimal);
            }

            else if (format.contains("(")){

                int startIndex = format.indexOf('(');
                int endIndex = format.indexOf(')');
                String extractedNumber = format.substring(startIndex + 1, endIndex);
                decimal = Integer.parseInt(extractedNumber);

                result = shiftAmount(amount,decimal); 
            }

            else{
                result = amount;
            }
        }
        catch(Exception e){
            
            result = amount;
        }

        return result;

    }
    
    public static void main(String[] args){

        Scanner sc = new Scanner(System.in);

        System.out.println("Enter Format = ");
        String format = sc.nextLine();

        System.out.println("Enter Amount = ");
        String amount = sc.nextLine();
        
        System.out.println(formatAmount(format, amount));

        sc.close();

        

    }
    
    

}
    
