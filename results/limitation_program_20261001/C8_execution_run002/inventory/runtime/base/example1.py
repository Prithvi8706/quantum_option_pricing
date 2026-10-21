def sum_of_divisors(num):
    total = 0
    for i in range(1, num):
        if num % i == 0:
            total += i
    return total

def is_perfect_number(num):
    return num == sum_of_divisors(num)

def find_and_print_perfect_numbers(limit):
    print("Perfect numbers between 1 and " + str(limit) + " are:")
    for num in range(2, limit + 1):
        if is_perfect_number(num):
            print(str(num))

def main():
    limit = 10000
    find_and_print_perfect_numbers(limit)

if __name__ == "__main__":
    main()
