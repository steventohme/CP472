public class Task2 {
    public static void main(String[] args){

        if (args.length <= 0) {
			System.out.println("No command line arguments found.");
        }

        int n = Integer.parseInt(args[0]);
        int[] fib = new int[n];
        fib[0] = 0;
        fib[1] = 1;
        for(int i = 2; i < n; i++){
            fib[i] = fib[i-1] + fib[i-2];
        }
        for(int i = 0; i < n; i++){
            System.out.println(fib[i]);
        }
    }
}