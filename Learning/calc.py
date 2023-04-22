#take two number from the user
#dict = {"key" : "values"}
history = {
    "addition" : [],
    "substarcion" : [],
    "multiply" : [],
    "division" : []
}
try:
    while(True):
        try:
            num1 = float(input("enter first number: "))
            num2 = float(input("enter second number: "))
        except ValueError:
            print("numbers only!!!!")
            continue
        #ask the user what is the mathematical operator (+-*/)
        operator = input("opertor (+,-,*,/): ")
        #print the user a nice answer
        if operator == "+":
            print(f"{num1} + {num2} = {num1+num2}")
            history["addition"].append(f"{num1} + {num2} = {num1+num2}")
        elif operator == "-":
            print(f"{num1} - {num2} = {num1-num2}")
            history["substarcion"].append(f"{num1} - {num2} = {num1-num2}")
        elif operator == "/":
            try:
                print(f"{num1} / {num2} = {num1/num2}")
                history["division"].append(f"{num1} / {num2} = {num1/num2}")
            except ZeroDivisionError:
                print("kjdfjk;daf 0 lo tov")
        elif operator == "*":
            print(f"{num1} * {num2} = {num1*num2}")
            history["multiply"].append(f"{num1} * {num2} = {num1*num2}")
        else:
            print("error")

        asd = input("exit? (y/n) history(h) ")
        if asd == "y":
            print("bye..")
            break
        elif asd == "n":
            print("again..")
        elif asd == "h":
            for key, value_list in history.items():
                print(f"{key}:")
                for index, value in enumerate(value_list):
                    print(f"\t{index+1}). {value}")
        else:
            print("bye ....")
except KeyboardInterrupt:
    print("\nbye...")