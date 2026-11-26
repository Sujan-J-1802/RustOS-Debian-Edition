class VirtualMachine:

    def __init__(self):

        self.registers = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0
        }

        self.memory = [0] * 16
        self.program = []
        self.pc = 0
        self.running = False

    def load_program(self, program):

        self.program = program
        self.pc = 0

        print("Program loaded successfully")

    def execute(self, instruction):

        opcode = instruction[0]

        if opcode == "LOAD":

            register, value = instruction[1:]
            self.registers[register] = value

        elif opcode == "ADD":

            destination, source = instruction[1:]

            self.registers[destination] += \
                self.registers[source]

        elif opcode == "SUB":

            destination, source = instruction[1:]

            self.registers[destination] -= \
                self.registers[source]

        elif opcode == "MUL":

            destination, source = instruction[1:]

            self.registers[destination] *= \
                self.registers[source]

        elif opcode == "STORE":

            register, address = instruction[1:]
            self.memory[address] = self.registers[register]

        elif opcode == "READ":

            register, address = instruction[1:]
            self.registers[register] = self.memory[address]

        elif opcode == "PRINT":

            register = instruction[1]

            print("Output:", self.registers[register])

        elif opcode == "HALT":

            self.running = False
            print("Virtual machine halted")

        else:

            print("Invalid instruction:", opcode)
            self.running = False

    def run(self):

        self.running = True

        print("\n===== PROGRAM EXECUTION =====")

        while self.running and self.pc < len(self.program):

            # Fetch instruction
            instruction = self.program[self.pc]

            print(f"\nPC = {self.pc}")
            print("Instruction:", instruction)

            # Increment program counter
            self.pc += 1

            # Decode and execute instruction
            self.execute(instruction)

            print("Registers:", self.registers)

    def display(self):

        print("\n===== FINAL VM STATE =====")

        print("Program Counter:", self.pc)
        print("Registers:", self.registers)
        print("Memory:", self.memory)


if __name__ == "__main__":

    vm = VirtualMachine()

    print("Toy Virtual Machine Simulation")
    print("=" * 55)

    program = [
        ("LOAD", "R0", 10),
        ("LOAD", "R1", 5),
        ("ADD", "R0", "R1"),
        ("LOAD", "R2", 2),
        ("MUL", "R0", "R2"),
        ("SUB", "R0", "R1"),
        ("STORE", "R0", 0),
        ("READ", "R3", 0),
        ("PRINT", "R3"),
        ("HALT",)
    ]

    vm.load_program(program)
    vm.run()
    vm.display()

    print("\nSimulation completed successfully.")
