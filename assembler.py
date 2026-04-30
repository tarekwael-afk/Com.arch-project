# ============================================================
# Simple Two-Pass Assembler
# Project: Assembler Design
# Purpose: Convert Assembly Code into Hexadecimal Machine Code
# ============================================================


class SimpleAssembler:
    def __init__(self):
        # Opcode table
        # Each assembly instruction has a hexadecimal opcode
        self.opcodes = {
            "LOAD": "1",
            "STORE": "2",
            "ADD": "3",
            "SUBT": "4",
            "INPUT": "5",
            "OUTPUT": "6",
            "HALT": "7",
            "JUMP": "9",
            "CLEAR": "A"
        }

        # Symbol table stores labels and their memory addresses
        # Example: X -> 5
        self.symbol_table = {}

        # This list stores the final machine code
        self.machine_code = []

    def clean_line(self, line):
        """
        This function removes comments and extra spaces.

        Example:
        LOAD X / this is a comment

        Becomes:
        LOAD X
        """

        # Remove anything after /
        if "/" in line:
            line = line.split("/")[0]

        # Remove spaces from beginning and end
        return line.strip()

    def first_pass(self, program_lines):
        """
        First Pass:
        The assembler scans the whole program and finds labels.

        Example:
        X, DEC 5

        Label = X
        Address = current memory location
        """

        address = 0

        for line in program_lines:
            line = self.clean_line(line)

            # Ignore empty lines
            if line == "":
                continue

            # If line contains comma, then it has a label
            if "," in line:
                label = line.split(",", 1)[0].strip()

                # Check duplicate label
                if label in self.symbol_table:
                    raise Exception(f"Duplicate label found: {label}")

                # Store label address
                self.symbol_table[label] = address

            # Increase memory address after each valid line
            address += 1

    def second_pass(self, program_lines):
        """
        Second Pass:
        Convert each assembly instruction into machine code.

        Example:
        LOAD X

        LOAD opcode = 1
        X address = 005

        Machine code = 1005
        """

        for line in program_lines:
            original_line = line
            line = self.clean_line(line)

            # Ignore empty lines
            if line == "":
                continue

            # Remove label part if it exists
            # Example: X, DEC 5 -> DEC 5
            if "," in line:
                line = line.split(",", 1)[1].strip()

            # Split line into instruction and operand
            parts = line.split()

            if len(parts) == 0:
                continue

            instruction = parts[0].upper()
            operand = parts[1] if len(parts) > 1 else None

            # ----------------------------
            # Handle DEC directive
            # ----------------------------
            if instruction == "DEC":
                if operand is None:
                    raise Exception(f"Missing value for DEC at line: {original_line}")

                value = int(operand)

                # Convert decimal value to 4-digit hexadecimal
                hex_value = format(value & 0xFFFF, "04X")
                self.machine_code.append(hex_value)

            # ----------------------------
            # Handle HEX directive
            # ----------------------------
            elif instruction == "HEX":
                if operand is None:
                    raise Exception(f"Missing value for HEX at line: {original_line}")

                # Convert value to uppercase and make it 4 digits
                hex_value = operand.zfill(4).upper()
                self.machine_code.append(hex_value)

            # ----------------------------
            # Handle normal instructions
            # ----------------------------
            elif instruction in self.opcodes:
                opcode = self.opcodes[instruction]

                # Some instructions do not need an address
                if instruction in ["INPUT", "OUTPUT", "HALT", "CLEAR"]:
                    address_part = "000"

                else:
                    if operand is None:
                        raise Exception(f"Missing operand at line: {original_line}")

                    # If operand is a label, replace it with its address
                    if operand in self.symbol_table:
                        address_part = format(self.symbol_table[operand], "03X")

                    # If operand is already a number, use it directly
                    elif operand.isdigit():
                        address_part = format(int(operand), "03X")

                    else:
                        raise Exception(f"Undefined label '{operand}' at line: {original_line}")

                # Final machine code = opcode + address
                machine_instruction = opcode + address_part
                self.machine_code.append(machine_instruction)

            # ----------------------------
            # Unknown instruction error
            # ----------------------------
            else:
                raise Exception(f"Unknown instruction '{instruction}' at line: {original_line}")

    def assemble(self, program_lines):
        """
        Main assembler function.
        It runs first pass and second pass.
        """

        # Clear old data before every run
        self.symbol_table = {}
        self.machine_code = []

        # First pass: build symbol table
        self.first_pass(program_lines)

        # Second pass: generate machine code
        self.second_pass(program_lines)

        return self.machine_code


# ============================================================
# Main Program
# ============================================================

def main():
    input_file = "sample.asm"
    output_file = "output.hex"

    try:
        # Read assembly code from sample.asm
        with open(input_file, "r") as file:
            program_lines = file.readlines()

        # Create assembler object
        assembler = SimpleAssembler()

        # Convert assembly code into machine code
        machine_code = assembler.assemble(program_lines)

        # Save machine code inside output.hex
        with open(output_file, "w") as file:
            for code in machine_code:
                file.write(code + "\n")

        # Print symbol table
        print("Symbol Table:")
        print("-------------")
        for label, address in assembler.symbol_table.items():
            print(f"{label} = {address}")

        # Print machine code
        print("\nMachine Code:")
        print("-------------")
        for code in machine_code:
            print(code)

        print(f"\nOutput saved successfully in {output_file}")

    except FileNotFoundError:
        print("Error: sample.asm file not found.")

    except Exception as error:
        print("Error:", error)


# Run the program
if __name__ == "__main__":
    main()