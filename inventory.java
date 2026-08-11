import java.util.ArrayList;
import java.util.Scanner;

class Product {
    private int id;
    private String name;
    private String category;
    private double price;
    private int quantity;

    public Product(int id, String name, String category,
                   double price, int quantity) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.price = price;
        this.quantity = quantity;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getCategory() {
        return category;
    }

    public double getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public void display() {
        System.out.println("---------------------------------------------");
        System.out.println("Product ID : " + id);
        System.out.println("Name       : " + name);
        System.out.println("Category   : " + category);
        System.out.println("Price      : $" + price);
        System.out.println("Quantity   : " + quantity);
    }
}

public class InventoryManagementSystem {

    static ArrayList<Product> products = new ArrayList<>();
    static Scanner scanner = new Scanner(System.in);

    static int nextId = 1;

    // Find a product using its ID
    static Product findProduct(int id) {

        for (Product product : products) {
            if (product.getId() == id) {
                return product;
            }
        }

        return null;
    }

    // Add a new product
    static void addProduct() {

        scanner.nextLine();

        System.out.print("Enter product name: ");
        String name = scanner.nextLine();

        System.out.print("Enter category: ");
        String category = scanner.nextLine();

        System.out.print("Enter price: ");
        double price = scanner.nextDouble();

        System.out.print("Enter quantity: ");
        int quantity = scanner.nextInt();

        if (price < 0 || quantity < 0) {
            System.out.println("Invalid price or quantity.");
            return;
        }

        Product product = new Product(
                nextId,
                name,
                category,
                price,
                quantity
        );

        products.add(product);

        System.out.println(
                "Product added successfully. ID: " + nextId
        );

        nextId++;
    }

    // Display all products
    static void displayProducts() {

        if (products.isEmpty()) {
            System.out.println("No products available.");
            return;
        }

        System.out.println("\n========== PRODUCT LIST ==========");

        for (Product product : products) {
            product.display();
        }
    }

    // Search for a product
    static void searchProduct() {

        System.out.print("Enter product ID: ");
        int id = scanner.nextInt();

        Product product = findProduct(id);

        if (product == null) {
            System.out.println("Product not found.");
        } else {
            product.display();
        }
    }

    // Update product price
    static void updatePrice() {

        System.out.print("Enter product ID: ");
        int id = scanner.nextInt();

        Product product = findProduct(id);

        if (product == null) {
            System.out.println("Product not found.");
            return;
        }

        System.out.print("Enter new price: ");
        double price = scanner.nextDouble();

        if (price < 0) {
            System.out.println("Price cannot be negative.");
            return;
        }

        product.setPrice(price);

        System.out.println("Price updated successfully.");
    }

    // Add stock
    static void addStock() {

        System.out.print("Enter product ID: ");
        int id = scanner.nextInt();

        Product product = findProduct(id);

        if (product == null) {
            System.out.println("Product not found.");
            return;
        }

        System.out.print("Enter quantity to add: ");
        int quantity = scanner.nextInt();

        if (quantity <= 0) {
            System.out.println("Quantity must be positive.");
            return;
        }

        product.setQuantity(
                product.getQuantity() + quantity
        );

        System.out.println("Stock added successfully.");
        System.out.println(
                "New quantity: " + product.getQuantity()
        );
    }

    // Remove stock
    static void removeStock() {

        System.out.print("Enter product ID: ");
        int id = scanner.nextInt();

        Product product = findProduct(id);

        if (product == null) {
            System.out.println("Product not found.");
            return;
        }

        System.out.print("Enter quantity to remove: ");
        int quantity = scanner.nextInt();

        if (quantity <= 0) {
            System.out.println("Quantity must be positive.");
            return;
        }

        if (quantity > product.getQuantity()) {
            System.out.println("Not enough stock available.");
            return;
        }

        product.setQuantity(
                product.getQuantity() - quantity
        );

        System.out.println("Stock removed successfully.");
    }

    // Delete product
    static void deleteProduct() {

        System.out.print("Enter product ID: ");
        int id = scanner.nextInt();

        Product product = findProduct(id);

        if (product == null) {
            System.out.println("Product not found.");
            return;
        }

        products.remove(product);

        System.out.println("Product deleted successfully.");
    }

    // Search products by category
    static void searchByCategory() {

        scanner.nextLine();

        System.out.print("Enter category: ");
        String category = scanner.nextLine();

        boolean found = false;

        for (Product product : products) {

            if (product.getCategory()
                    .equalsIgnoreCase(category)) {

                product.display();
                found = true;
            }
        }

        if (!found) {
            System.out.println(
                    "No products found in this category."
            );
        }
    }

    // Display products with low stock
    static void lowStockReport() {

        System.out.print(
                "Enter low-stock threshold: "
        );

        int threshold = scanner.nextInt();

        boolean found = false;

        System.out.println("\n========== LOW STOCK ==========");

        for (Product product : products) {

            if (product.getQuantity() <= threshold) {

                product.display();
                found = true;
            }
        }

        if (!found) {
            System.out.println(
                    "No products have low stock."
            );
        }
    }

    // Calculate total inventory value
    static void inventoryValue() {

        double total = 0;

        for (Product product : products) {

            total += product.getPrice()
                    * product.getQuantity();
        }

        System.out.println(
                "Total inventory value: $" + total
        );
    }

    // Display inventory statistics
    static void statistics() {

        if (products.isEmpty()) {
            System.out.println("No products available.");
            return;
        }

        int totalProducts = products.size();
        int totalQuantity = 0;
        double totalValue = 0;

        Product mostExpensive = products.get(0);

        for (Product product : products) {

            totalQuantity += product.getQuantity();

            totalValue += product.getPrice()
                    * product.getQuantity();

            if (product.getPrice()
                    > mostExpensive.getPrice()) {

                mostExpensive = product;
            }
        }

        System.out.println(
                "\n========== INVENTORY STATISTICS =========="
        );

        System.out.println(
                "Number of Products : " + totalProducts
        );

        System.out.println(
                "Total Items        : " + totalQuantity
        );

        System.out.println(
                "Inventory Value     : $" + totalValue
        );

        System.out.println(
                "Most Expensive     : "
                        + mostExpensive.getName()
        );

        System.out.println(
                "Highest Price      : $"
                        + mostExpensive.getPrice()
        );
    }

    // Main menu
    static void showMenu() {

        System.out.println("\n=================================");
        System.out.println("     INVENTORY MANAGEMENT");
        System.out.println("=================================");
        System.out.println("1. Add Product");
        System.out.println("2. Display Products");
        System.out.println("3. Search Product");
        System.out.println("4. Update Price");
        System.out.println("5. Add Stock");
        System.out.println("6. Remove Stock");
        System.out.println("7. Delete Product");
        System.out.println("8. Search by Category");
        System.out.println("9. Low Stock Report");
        System.out.println("10. Inventory Value");
        System.out.println("11. Statistics");
        System.out.println("12. Exit");
        System.out.println("=================================");
    }

    public static void main(String[] args) {

        // Sample products
        products.add(
                new Product(
                        nextId++,
                        "Laptop",
                        "Electronics",
                        850.00,
                        10
                )
        );

        products.add(
                new Product(
                        nextId++,
                        "Keyboard",
                        "Electronics",
                        45.50,
                        25
                )
        );

        products.add(
                new Product(
                        nextId++,
                        "Office Chair",
                        "Furniture",
                        180.00,
                        8
                )
        );

        int choice;

        while (true) {

            showMenu();

            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {

                case 1:
                    addProduct();
                    break;

                case 2:
                    displayProducts();
                    break;

                case 3:
                    searchProduct();
                    break;

                case 4:
                    updatePrice();
                    break;

                case 5:
                    addStock();
                    break;

                case 6:
                    removeStock();
                    break;

                case 7:
                    deleteProduct();
                    break;

                case 8:
                    searchByCategory();
                    break;

                case 9:
                    lowStockReport();
                    break;

                case 10:
                    inventoryValue();
                    break;

                case 11:
                    statistics();
                    break;

                case 12:
                    System.out.println(
                            "Exiting Inventory System..."
                    );

                    scanner.close();
                    return;

                default:
                    System.out.println(
                            "Invalid choice. Try again."
                    );
            }
        }
    }
}
