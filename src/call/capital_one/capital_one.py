# Prompt:
# Your task is to implement a simplified version of a banking system.
# Level 1:
# Ask:
# Please implement a banking system library with methods that can support new account creation as well as depositing and withdrawal functions.

# Operations:
# deposit <accountId> <amount>
# Should create a new account with the given identifier and starting balance if it doesn't already exist.
# If the account already exists, deposit the given `amount` of money to the specified account `accountId`
# Returns "true" if an account was successfully created,
# Returns `amount` of the specified account if an account with `accountId` already exists.


# withdraw <accountId> <amount>
# Should withdraw the given `amount` of money to the specified account `accountId`
# Returns a string representing the total amount of money in the account after the query has been processed.
# If the specified balance of the account is lower than the `amount` to be withdrawn, it should return an empty string.
# If the specified account doesn't exist, it should return an empty string.

# Example:
# The example below shows how these operations should work:

# Queries
# Explanations
# operations = [
#   ["DEPOSIT", "account1", "1000"],
#   ["DEPOSIT", "account1", "500"],
#   ["DEPOSIT", "account2", "1000"],
#   ["WITHDRAW", "non-existing", "2700"],
#   ["WITHDRAW", "account1", "2000"],
#   ["WITHDRAW", "account1", "500"]
# ]

# returns "1000"
# returns "1500"; an account with this identifier already exists
# returns "1000";
# returns ""; an account with this identifier doesn't exist
# returns ""; withdrawal amount exceeds the account balance
# returns "1000"


# the output should be ["true", "1500", "true", "", "", "1000"].


class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.output = []

    def operate(self, args):
        if args[0] == "DEPOSIT":
            operation, account_id, balance = args
            # print(f"{operation}, {account_id}, {balance}")
            self.__deposit(account_id, balance)
        elif args[0] == "WITHDRAW":
            operation, account_id, balance = args
            # print(f"{operation}, {account_id}, {balance}")
            self.__withdraw(account_id, balance)
        elif args[0] == "TRANSFER":
            operation, from_id, to_id, trnasfer_amount = args
            # print(f"{operation}, {account_id}, {balance}, {trnasfer_amount}")
            self.__transfer(from_id, to_id, trnasfer_amount)
        return ""

    def __deposit(self, account_id, balance):
        # check if the account exists or not then either add or create
        # print(f"account_id {account_id} balance: {balance}, all: {self.accounts} ")
        if account_id not in self.accounts:
            self.output.append("true")
            self.accounts[account_id] = int(balance)
        else:
            self.accounts[account_id] = int(self.accounts[account_id]) + int(balance)
            self.output.append(str(self.accounts[account_id]))

    def __transfer(self, from_id, to_id, amount):
        if from_id not in self.accounts or to_id not in self.accounts:
            self.output.append("")
            return
        from_balance = int(self.accounts[from_id])

        if int(amount) > from_balance:
            self.output.append("")
            return

        self.accounts[from_id] = from_balance - int(amount)
        self.accounts[to_id] = str(int(self.accounts[to_id]) + int(amount))
        self.output.append(self.accounts[from_id])

    def __withdraw(self, account_id, amount):
        if account_id not in self.accounts:
            self.output.append("")
            return

        # get the account balance
        existing_balance = int(self.accounts[account_id])
        # print(f"existing balance: {existing_balance}, withdraw {int(amount)}")

        new_balance = ""
        if existing_balance > int(amount):
            new_balance = existing_balance - int(amount)
            print(f"new balance {new_balance}")
            self.accounts[account_id] = str(new_balance)
            self.output.append(str(new_balance))
        else:
            self.output.append("")


bs = BankingSystem()
bs.operate(["DEPOSIT", "account_1", "1000"])
bs.operate(["DEPOSIT", "account_1", "500"])
bs.operate(["DEPOSIT", "account_2", "1000"])

bs.operate(["WITHDRAW", "account_na", "1000"])
bs.operate(["WITHDRAW", "account_1", "5000"])
bs.operate(["WITHDRAW", "account_1", "500"])

bs.operate(["TRANSFER", "account_1", "account_2", "1001"])
bs.operate(["TRANSFER", "account_1", "account_2", "200"])
print(bs.output)


"""
Ask: 
On your existing implementation, please implement a new functionality that would support the transferring of funds from one account to another. This operation is defined below, feel free to approach the implementation in a way that is comfortable for you.

Operation:
transfer <fromId> <toId> <amount>
Should transfer the given amount of money from account with fromId to account with toId. 
Returns a string representing the balance of fromId if the transfer was successful, or an empty string otherwise.
Returns an empty string if fromId or toId doesn't exist.
Returns an empty string if fromId and toId are the same.
Returns an empty string if funds on the account fromId are insufficient to perform the transfer.

Example:
The example below shows how these operations should work:
Queries
Explanations
operations = [
  ["DEPOSIT", "account1", "1000"],
  ["DEPOSIT", "account1", "500"],
  ["DEPOSIT", "account2", "1000"],
  ["WITHDRAW", "non-existing", "2700"],
  ["WITHDRAW", "account1", "2000"],
  ["WITHDRAW", "account1", "500"],
  ["TRANSFER", "account1", "account2", "1001"],
  ["TRANSFER", "account1", "account2", "200"]
]

returns "1000"
returns "1500"; an account with this identifier already exists
returns "1000";
returns ""; an account with this identifier doesn't exist
returns ""; withdrawal amount exceeds the account balance
returns "1000"
returns ""; this account has insufficient funds
returns "800"


the output should be ["true", "1500", "true", "", "", "1000", "", "800"].

"""
