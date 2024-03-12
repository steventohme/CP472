# A Comparison of Object-Oriented Programming (OOP) Concepts in Java and Python

In this report, we compare the object-oriented programming (OOP) concepts used in the provided Java and Python code snippets. Both languages follow OOP principles such as encapsulation, inheritance, and polymorphism. We'll explore how these concepts are implemented in each language based on the provided code.

## Encapsulation

### Java

- In Java, encapsulation is achieved using access modifiers (private, protected, public) to restrict access to class members.
- Getters and setters are commonly used to provide controlled access to private fields.

### Python

- In Python, encapsulation is conventionally achieved using underscores (_) to denote private members.
- Direct access to attributes is discouraged, and properties or methods are used to access or modify attributes indirectly.

## Inheritance

### Java

- Java supports single inheritance, where a class can inherit from only one superclass.
- Inheritance relationships are established using the extends keyword.

### Python

- Python supports both single and multiple inheritance.
- Inheritance relationships are established by listing parent classes in parentheses after the class name.

## Polymorphism

### Java

- Polymorphism in Java is achieved through method overriding and method overloading.
- Method overriding allows a subclass to provide a specific implementation of a method that is already defined in its superclass.
- Method overloading allows multiple methods with the same name but different parameters in the same class.

### Python

- Polymorphism in Python is more flexible due to dynamic typing.
- Polymorphism is achieved implicitly; objects of different classes can be used interchangeably if they support the same interface or method names.

## Conclusion
Both Java and Python support fundamental OOP concepts such as encapsulation, inheritance, and polymorphism. While Java relies on explicit syntax for encapsulation and inheritance, Python emphasizes convention and flexibility. Understanding these differences can help developers choose the right language and approach for their projects.