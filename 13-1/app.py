def compare_lists(list1, list2):
    for index in range(0, max(len(list1), len(list2))):
        if index >= len(list1):
            return True
        elif index >= len(list2):
            return False

        cmp1 = list1[index]
        cmp2 = list2[index]

        if type(cmp1) == type(cmp2):
            if type(cmp1) is int:
                if cmp1 == cmp2:
                    continue
                else:
                    result = cmp1 < cmp2
            elif type(cmp1) is list:
                if cmp1 == cmp2:
                    continue
                result = compare_lists(cmp1, cmp2)
        elif type(cmp1) is int:
            result = compare_lists([cmp1], cmp2)
        elif type(cmp2) is int:
            result = compare_lists(cmp1, [cmp2])

        if result is None:
            continue
        else:
            return result


with open("input.txt") as file:
    lines = list(map(eval, [l.strip() for l in file.readlines() if l.strip() != ""]))

    # Part 1
    list_index = 0
    indicies = []
    for i in range(0, len(lines), 2):
        list_index += 1

        result = compare_lists(lines[i], lines[i + 1])
        if result:
            indicies.append(list_index)

    print(sum(indicies))

    # Part 2
    delimiters = [[[2]], [[6]]]
    lines.extend(delimiters)
    sorted_packets = [lines[0]]
    for i in range(1, len(lines)):
        for j in range(0, len(sorted_packets)):
            if compare_lists(lines[i], sorted_packets[j]):
                sorted_packets.insert(j, lines[i])
                break
            else:
                if j == len(sorted_packets) - 1:
                    sorted_packets.append(lines[i])

    decoder_key: int = 1
    for delimiter in delimiters:
        decoder_key *= (sorted_packets.index(delimiter) + 1)

    print(decoder_key)
