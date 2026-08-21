// Something.java
// A simple 100+ line Java program that "runs something":
// it prints information, performs calculations, manipulates text,
// creates a list, and runs a small command loop.

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Something {

    private static final String APP_NAME = "Something Runner";
    private static final Random RANDOM = new Random();

    public static void main(String[] args) {
        printBanner();
        printEnvironment();
        runDemo();

        if (args.length > 0) {
            runArguments(args);
        } else {
            runInteractiveMode();
        }

        printGoodbye();
    }

    private static void printBanner() {
        System.out.println("========================================");
        System.out.println("        " + APP_NAME);
        System.out.println("========================================");
        System.out.println("Java is running successfully!");
        System.out.println();
    }

    private static void printEnvironment() {
        System.out.println("Current time: " + LocalDateTime.now());
        System.out.println("Java version: " +
                System.getProperty("java.version"));
        System.out.println("Operating system: " +
                System.getProperty("os.name"));
        System.out.println("User: " +
                System.getProperty("user.name"));
        System.out.println();
    }

    private static void runDemo() {
        System.out.println("--- Running demo ---");

        int a = 10;
        int b = 25;

        System.out.println("a = " + a);
        System.out.println("b = " + b);
        System.out.println("a + b = " + add(a, b));
        System.out.println("a * b = " + multiply(a, b));

        String message = "Java can run something!";
        System.out.println("Original: " + message);
        System.out.println("Uppercase: " + message.toUpperCase());
        System.out.println("Length: " + message.length());

        List<String> items = createItems();

        System.out.println("Items:");
        for (String item : items) {
            System.out.println(" - " + item);
        }

        System.out.println("Random number: " + randomNumber(1, 100));
        System.out.println("--- Demo finished ---");
        System.out.println();
    }

    private static List<String> createItems() {
        List<String> items = new ArrayList<>();

        items.add("Something");
        items.add("Anything");
        items.add("Java");
        items.add("Code");
        items.add("Fun");

        return items;
    }

    private static int add(int x, int y) {
        return x + y;
    }

    private static int multiply(int x, int y) {
        return x * y;
    }

    private static int randomNumber(int min, int max) {
        return RANDOM.nextInt(max - min + 1) + min;
    }

    private static void runArguments(String[] args) {
        System.out.println("--- Arguments ---");

        for (int i = 0; i < args.length; i++) {
            System.out.println("Argument " + (i + 1) + ": " + args[i]);
        }

        System.out.println();
    }

    private static void runInteractiveMode() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("--- Interactive mode ---");
        System.out.println("Type a command:");
        System.out.println("  hello   - say hello");
        System.out.println("  random  - generate a number");
        System.out.println("  count   - count to ten");
        System.out.println("  reverse - reverse some text");
        System.out.println("  math    - run calculations");
        System.out.println("  exit    - quit");
        System.out.println();

        while (true) {
            System.out.print("> ");

            String command = scanner.nextLine().trim();

            if (command.equalsIgnoreCase("exit")) {
                break;
            }

            handleCommand(command, scanner);
        }

        scanner.close();
    }

    private static void handleCommand(String command, Scanner scanner) {
        switch (command.toLowerCase()) {

            case "hello":
                sayHello();
                break;

            case "random":
                System.out.println(
                        "Your random number is: " +
                        randomNumber(1, 1000)
                );
                break;

            case "count":
                countToTen();
                break;

            case "reverse":
                System.out.print("Enter text: ");
                String text = scanner.nextLine();
                System.out.println("Reversed: " + reverse(text));
                break;

            case "math":
                runMath();
                break;

            case "":
                System.out.println("You entered nothing.");
                break;

            default:
                System.out.println(
                        "I don't know that command, " +
                        "so I'll run SOMETHING instead!"
                );
                doSomething(command);
                break;
        }

        System.out.println();
    }

    private static void sayHello() {
        System.out.println("Hello from Java!");
        System.out.println("Something is definitely running.");
    }

    private static void countToTen() {
        for (int i = 1; i <= 10; i++) {
            System.out.println("Count: " + i);
        }
    }

    private static String reverse(String text) {
        return new StringBuilder(text)
                .reverse()
                .toString();
    }

    private static void runMath() {
        int x = randomNumber(1, 50);
        int y = randomNumber(1, 50);

        System.out.println("Generated X = " + x);
        System.out.println("Generated Y = " + y);
        System.out.println("Addition: " + (x + y));
        System.out.println("Subtraction: " + (x - y));
        System.out.println("Multiplication: " + (x * y));

        if (y != 0) {
            System.out.println("Division: " + ((double) x / y));
        }

        System.out.println("Maximum: " + Math.max(x, y));
        System.out.println("Minimum: " + Math.min(x, y));
    }

    private static void doSomething(String input) {
        System.out.println("Doing something with: " + input);

        for (int i = 0; i < 3; i++) {
            System.out.println("Something step " + (i + 1) + "...");
            pause(300);
        }

        System.out.println("Something completed!");
    }

    private static void pause(long milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            System.out.println("The operation was interrupted.");
        }
    }

    private static void printGoodbye() {
        System.out.println();
        System.out.println("========================================");
        System.out.println("        Program finished.");
        System.out.println("========================================");
    }

    // Extra methods make this class easy to extend.

    private static boolean isEven(int number) {
        return number % 2 == 0;
    }

    private static boolean isPositive(int number) {
        return number > 0;
    }

    private static int square(int number) {
        return number * number;
    }

    private static void showNumberInfo(int number) {
        System.out.println("Number: " + number);
        System.out.println("Even: " + isEven(number));
        System.out.println("Positive: " + isPositive(number));
        System.out.println("Square: " + square(number));
    }

    private static String repeat(String text, int times) {
        StringBuilder result = new StringBuilder();

        for (int i = 0; i < times; i++) {
            result.append(text);
        }

        return result.toString();
    }

    private static void extraDemo() {
        System.out.println(repeat("-", 20));
        showNumberInfo(42);
        System.out.println(repeat("-", 20));
    }
}
