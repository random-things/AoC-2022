def determine_start_position(stream_line: str, unique_sequence_length: int = 4) -> int:
    for i in range(0, len(stream_line)):
        chars: set = set(stream_line[i:i + unique_sequence_length])

        if len(chars) == unique_sequence_length:
            return i + unique_sequence_length


with open("input.txt") as file:
    contents = file.read()

    if "\n" in contents:
        for line in contents.split("\n"):
            print(determine_start_position(line, 14))
    else:
        print(determine_start_position(contents, 14))
