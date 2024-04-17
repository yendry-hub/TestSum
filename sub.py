# sub.py
def subtract(num1, num2):
    return num1 - num2

if __name__ == "__main__":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    result = subtract(num1, num2)
    print(f"The subtraction result is: {result}")
