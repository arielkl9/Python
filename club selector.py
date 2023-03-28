#!/usr/bin/python
import base64

users_list = []


again = True
while again:
    user_name = input("insert your name: ")
    user_age = input("insert your age: ")

    brought_a_friend = input("brought a friend? (yes or no please...)")
    if brought_a_friend == "yes":
        brought_a_friend = True
    elif brought_a_friend == "no":
        brought_a_friend = False
    else:
        print("dont understand what r u telling me noob... u must have come alone...")
        brought_a_friend = False

    if user_age.isdigit():
        user_age = int(user_age)
        if user_age < 18:
            print("no")
        elif 18 <= user_age <= 21:
            user_id = input("insert id:")
            if len(user_id) >= 8:
                user_id_bytes = user_id.encode('ascii')
                base64_bytes = base64.b64encode(user_id_bytes)
                price = 220
                if brought_a_friend:
                    user_data_list = [user_name, user_age, price / 2, base64_bytes.decode('UTF-8')]
                    users_list.append(user_data_list)
                else:
                    user_data_list = [user_name, user_age, price, base64_bytes.decode('UTF-8')]
                    users_list.append(user_data_list)
        elif 21 < user_age < 53:
            price = 200
            if brought_a_friend:
                user_data_list = [user_name,user_age,price / 2]
                users_list.append(user_data_list)
            else:
                user_data_list = [user_name,user_age,price]
                users_list.append(user_data_list)
        elif 53 < user_age < 120:
            price = 165
            if brought_a_friend:
                user_data_list = [user_name,user_age,price / 2]
                users_list.append(user_data_list)
            else:
                user_data_list = [user_name,user_age,price]
                users_list.append(user_data_list)
        else:
            print("free pass")
            user_data_list = [user_name,user_age]
            users_list.append(user_data_list)
        ans = input("again? (yes or no)?: ")
        if ans == "yes":
            print("again")
            continue
        elif ans == "no":
            print("bye")
            again = False
        else:
            print("again")
            continue
    else:
        print("wrong input only numbers allowed")
        ans = input("again? (yes or no)?: ")
        if ans == "yes":
            print("again")
            continue
        elif ans == "no":
            print("bye")
            again = False
        else:
            print("again")
            continue


for tzora in users_list:
    print(tzora)
