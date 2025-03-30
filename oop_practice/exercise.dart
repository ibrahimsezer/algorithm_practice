class Product {
  final String name;
  final int stockAmount;
  final double price;

  Product(this.name, this.stockAmount, this.price) {}

  void getInfo() {
    print("name:$name, price:$price, stock:$stockAmount");
  }

  void increaseStock(int addAmount) {
    if (addAmount > 0) {
      stockAmount + addAmount;
      print("stock increased");
    } else {
      print("amount must be positive");
    }
  }

  void decreaseStock(int removeAmount) {
    if (stockAmount > removeAmount) {
      stockAmount - removeAmount;
      print("stock decreased");
    } else {
      print("stock not have");
    }
  }

  double totalPrice(double price, int amount) {
    return price * amount;
  }
}

class Book extends Product {
  final String author;
  final String isbn;

  Book(String name, double price, int stockAmount, this.author, this.isbn)
      : super(name, stockAmount, price);

  @override
  void getInfo() {
    super.getInfo();
    print("Author:$author, ISBN:$isbn");
  }
}

class Electronic extends Product {
  final String brand;
  final String model;
  int warrantyMonths;

  Electronic(String name, int stockAmount, double price, this.brand, this.model,
      this.warrantyMonths)
      : super(name, stockAmount, price);

  void extendWarranty(int months) {
    warrantyMonths += months;
    print("Name: $name, new warrantyMonths: $warrantyMonths");
  }

  @override
  void getInfo() {
    super.getInfo();
    print("brand $brand, model $model, warranty $warrantyMonths");
  }
}

void main() {
  Electronic el = Electronic("phone", 12, 1200, "nokia", "3310", 12);

  el.increaseStock(12);
  el.decreaseStock(1);
  el.extendWarranty(12);
  print(el.totalPrice(el.price, el.stockAmount));
  el.getInfo();
}
