#Capture the input and convert to list of string number
string_numbers = input("Input:")

is_negative = string_numbers.startswith('-')
best_index_to_remove = None
temp = []
# Iterate to find the best '5' to remove
# I use chatGPT to correct my logic when deal with negative numbers
for i, digit in enumerate(string_numbers):
    if digit == '5':
        if is_negative:
            # For negative numbers, remove the first '5' after '-'
            best_index_to_remove = i
            break
        elif best_index_to_remove is None or int(string_numbers[i+1:i+2] or '0') > 5:
            # For positive numbers, remove the '5' which gives a smaller number
            best_index_to_remove = i
new_number_str = string_numbers[:best_index_to_remove] + string_numbers[best_index_to_remove+1:]
print("Output:",int(new_number_str))
