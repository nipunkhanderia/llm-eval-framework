
account_list = []

def create_account(name, balance):
    account_holder = {"name" : name, "balance": balance}
    account_list.append(account_holder)
    print(account_list)
    return account_list

def search_account(name):
    for account in account_list:
        if account["name"] == name:
            print(f"{account["name"]} Name found")

            return name

        else:
            print(f"{account["name"]} Name not found")

def withdraw(name, amount):
    name_found = search_account(name)
    for account in account_list:
       if account["name"] == name:
          balance =  account["balance"]
          new_balance = balance - amount
          print (f"{name} balance is {new_balance}")
          return new_balance

    
    


if __name__ == "__main__":

    create_account("Nipun", 99)
    create_account("Rhythm", 100)
    create_account("Payal", 100)


    # search_account("Nipun")
    withdraw("Nipun", 10)
    withdraw("Rhythm", 10)
    # withdraw("Payal", 10)


