def reduction_of_price(lst):
    # Set current min
    min_current = int(lst[0])
    #Iterate through the list, comparing each price with the previous one.
    for i in range(1, len(lst)):
        current = int(lst[i])
        if current < min_current :
            return i  # Return the index of the price reduction
        min_current = min(min_current,current)

    return 0  # Return 0 if no reduction is found

#Capture the input and convert to list of string number
lst = input("Input:").split()
print("Output:",reduction_of_price(lst))

