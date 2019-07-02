account1 = "jorge"
account2 = "steve"

db_accounts = [ {'name': 'jorge'}, {'name': 'steve'} ]

def test(name):
    for item in db_accounts:
        if name == item['name']:
            # do nothing
        elif name != item['name']:
            #insert new to db
    return "world"


# Step 1
{'name': 'jorge'}
if account1 == "jorge"

# step 2
{'name': 'steve'}