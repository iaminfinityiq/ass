from json import load
import time

# Errors section
class ConvertError(Exception):
    pass

# Functions section
def convert_number(num, min, max, error, message):
    try:
        num = float(num)
        if min <= num <= max:
            return int(num) if num % 1 == 0 else num

        raise error(message)
    except ValueError:
        raise ConvertError(f"Can't convert '{num}' to a number.")

def EOF_detection(address, instructions, INSTRUCTION_SIZE):
    if address >= len(instructions):
        return False
    
    return instructions[address].lower().strip() != "grounded" and address < INSTRUCTION_SIZE

# Main program
file = input("Which file do you want to run? ")
with open(f"{file}.as") as file:
    instructions = file.read().split("\n")

with open("program-settings.json") as settings:
    settings = load(settings)
    MAX = 2 ** settings["register_size"] - 1
    MIN = -MAX
    INSTRUCTION_SIZE = settings["instruction_size"]
    MEMORY_SIZE = settings["memory_size"]
    OUTER_SIZE = settings["outer_size"]

if len(instructions) > INSTRUCTION_SIZE:
    raise OverflowError(f"Too much instructions. Amount of instructions: {len(instructions)}/{INSTRUCTION_SIZE}.")

registers = [0 for i in range(MEMORY_SIZE)]
outer = [0 for i in range(OUTER_SIZE)]

address = 0
while EOF_detection(address, instructions, INSTRUCTION_SIZE):
    tokens = instructions[address].split()
    if len(tokens) == 0:
        address += 1
        continue

    match tokens[0].lower():
        case "//":
            pass
        case "grounded":
            raise SyntaxError(f"Expected 0 arguments, got {len(tokens) - 1}/0.")
        case "spit":
            if len(tokens) != 2:
                raise SyntaxError(f"Expected 1 argument, got {len(tokens) - 1}/1.")

            register = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")

            print(registers[register])
        case "chugjug":
            if len(tokens) != 3:
                raise SyntaxError(f"Expect 2 arguments, got {len(tokens) - 1}/2.")

            register = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            number = convert_number(tokens[2], MIN, MAX, OverflowError, f"Overflowed the minimum/maximum value: {abs(int(tokens[2]) if float(tokens[2]) % 1 == 0 else float(tokens[2]))}/{MAX}.")

            registers[register] = number
        case "paura":
            if len(tokens) != 4:
                raise SyntaxError(f"Expect 3 arguments, got {len(tokens) - 1}/3.")

            a = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            b = convert_number(tokens[2], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[2]}.")
            dest = convert_number(tokens[3], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[3]}.")

            registers[dest] = registers[a] + registers[b]
            if not MIN < registers[dest] < MAX:
                raise OverflowError(f"Overflowed operation: {registers[a]} + {registers[b]}")
        case "naura":
            if len(tokens) != 4:
                raise SyntaxError(f"Expect 3 arguments, got {len(tokens) - 1}/3.")

            a = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            b = convert_number(tokens[2], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[2]}.")
            dest = convert_number(tokens[3], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[3]}.")

            registers[dest] = registers[a] - registers[b]
            if not MIN < registers[dest] < MAX:
                raise OverflowError(f"Overflowed operation: {registers[a]} - {registers[b]}")
        case "chest":
            if len(tokens) != 3:
                raise SyntaxError(f"Expect 2 arguments, got {len(tokens) - 1}/2.")

            source = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            dest = convert_number(tokens[2], 0, OUTER_SIZE - 1, OverflowError, f"Invalid outer data index value: {tokens[2]}.")

            outer[dest] = registers[source]
        case "fanumtax":
            if len(tokens) != 3:
                raise SyntaxError(f"Expect 2 arguments, got {len(tokens) - 1}/2.")

            source = convert_number(tokens[1], 0, OUTER_SIZE - 1, OverflowError, f"Invalid outer data index value: {tokens[1]}.")
            dest = convert_number(tokens[2], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[2]}.")

            registers[dest] = outer[source]
        case "caseoh":
            if len(tokens) != 2:
                raise SyntaxError(f"Expect 1 argument, got {len(tokens) - 1}/1.")

            instruction = convert_number(tokens[1], 1, INSTRUCTION_SIZE, OverflowError, f"Invalid instruction index: {tokens[1]}.")
            address = instruction - 2
        case "compass":
            if len(tokens) != 5:
                raise SyntaxError(f"Expect 4 arguments, got {len(tokens) - 1}/4.")

            a = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            op = convert_number(tokens[2], 0, 5, OverflowError, f"Invalid operator: {tokens[1]}.")
            b = convert_number(tokens[3], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            instruction = convert_number(tokens[4], 1, INSTRUCTION_SIZE, OverflowError, f"Invalid instruction index: {tokens[4]}.")

            match op:
                case 0:
                    operation = registers[a] == registers[b]
                case 1:
                    operation = registers[a] != registers[b]
                case 2:
                    operation = registers[a] > registers[b]
                case 3:
                    operation = registers[a] < registers[b]
                case 4:
                    operation = registers[a] >= registers[b]
                case 5:
                    operation = registers[a] <= registers[b]

            if operation:
                address = instruction - 2
        case "snore":
            if len(tokens) != 2:
                raise SyntaxError(f"Expect 1 argument, got {len(tokens) - 1}/1.")

            seconds = convert_number(tokens[1], 0, MAX, OverflowError, f"Invalid time as seconds: {tokens[1]}.")
            time.sleep(seconds)
        case "ksmasher":
            if len(tokens) < 2:
                raise SyntaxError(f"Expect 1 arugment, got {len(tokens) - 1}/1.")

            register = convert_number(tokens[1], 0, MEMORY_SIZE - 1, OverflowError, f"Invalid register value: {tokens[1]}.")
            if len(tokens) == 2:
                prompt = ""
            else:
                prompt = instructions[address][len("ksmasher") + len(tokens[2]) - 1::]

            user_inp = input(prompt)
            user_inp = convert_number(user_inp, MIN, MAX, OverflowError, f"Overflowed the minimum/maximum value: {abs(int(user_inp) if float(user_inp) % 1 == 0 else float(user_inp))}/{MAX}.")

            registers[register] = user_inp
        case _:
            raise SyntaxError(f"Invalid instruction: {tokens[0]}")

    address += 1
