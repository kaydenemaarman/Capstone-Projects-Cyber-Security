# Python code:

import math

# show the user a menu of calculator options
print("Investment - to calculate the amount of interest you'll earn on your investment.")
print("Bond - to calculate the amount you'll need to pay back on a loan.")

# request the user to choose a calculator
calculator_type = input("Enter either 'investment' or 'bond' from the menu above to proceed: ").lower()

# investment option
if calculator_type == "investment":
    # ask user for additional inputs
    P = float(input("Enter the amount of money to deposit: "))
    r = float(input("Enter the interest rate (without %): ")) / 100
    t = int(input("Enter the number of years to invest: "))

    # request user to choose interest type
    interest = input("Choose either 'simple' or 'compound' interest: ").lower()

    # calculate simple or compound interest
    if interest == "simple":
        total_amount = P * (1 + r * t)
        print(f"The total amount after {t} years with simple interest is: R{total_amount:.2f}")
    elif interest == "compound":
        total_amount = P * math.pow((1 + r), t)
        print(f"The total amount after {t} years with compound interest is: R{total_amount:.2f}")
    else:
        print("Invalid interest type. Please choose either 'simple' or 'compound'.")

# bond option
elif calculator_type == "bond":
    P = float(input("Enter the present value of the house: "))
    i = float(input("Enter the annual interest rate (without %): ")) / 100 / 12
    n = int(input("Enter the number of months to repay the bond: "))

    repayment = (i * P) / (1 - (1 + i) ** (-n))
    print(f"The monthly repayment amount is: R{repayment:.2f}")

else:
    print("Invalid selection. Please choose either 'investment' or 'bond'.")

# I played around a lot with this task and during that, I discovered I could input directly from the terminal. I didn't know I could do that. So this discovery helped a lot with testing this code until it worked.