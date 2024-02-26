item_dict:dict = {"1":"apple", "2":"orange"}
first_key, first_value = next(iter(item_dict.items()))
print(first_key, first_value)

for key in item_dict:
    print(key)