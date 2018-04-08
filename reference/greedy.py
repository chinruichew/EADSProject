def take_input(infile):
    f_open = open(infile, 'r')
    lines = []
    for line in f_open:
        lines.append(line.strip())
    f_open.close()
    return lines

def set_weight(weight):
    bag_weight = weight
    return bag_weight

def jewel_list(lines):
    jewels = []
    for item in lines:
        jewels.append(item.split())
    jewels = sorted(jewels, reverse= True)
    jewel_dict = {}
    for item in jewels:
        jewel_dict[item[1]] = item[0]
    return jewel_dict

def greedy_grab(weight_max, jewels):
    #first, we get a list of values
    values = []
    weights = []
    for keys in jewels:
        weights.append(jewels[keys])
    for item in jewels.keys():
        values.append(item)
    values = sorted(values, reverse= True)
    #then, we start working
    max = int(weight_max)
    running = 0
    i = 0
    grabbed_list = []
    string = ''
    total_haul = 0
    # pick the most valuable item first. Pick as many of them as you can.
    # Then, the next, all the way through.
    while running < max:
        next_add = int(jewels[values[i]])
        if (running + next_add) > max:
            i += 1
        else:
            running += next_add
            grabbed_list.append(values[i])
    for item in grabbed_list:
        total_haul += int(item)
    string = "The greedy approach would steal $" + str(total_haul) + " of jewels."
    return string

infile = "JT_test2.txt"
lines = take_input(infile)
#set the bag weight with the first line from the input
bag_max = set_weight(lines[0])
#once we set bag weight, we don't need it anymore
lines.pop(0)

#generate a list of jewels in a dictionary by weight, value
value_list = jewel_list(lines)
#run the greedy approach
print(greedy_grab(bag_max, value_list))