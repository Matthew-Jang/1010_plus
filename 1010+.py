REG_COUNT    = 16
MEMORY_SIZE  = 256

# CPU state
registers = [0] * REG_COUNT
memory    = [0] * MEMORY_SIZE
pc         = 0
#ax = register 1
#cx = register 2
#di = register 15

# label → instruction‑index map
labels = {}

# Opcodes
OPCODES = {
    '0000': 'nop',      # no operation
    '0001': 'ld',       # load from memory
    '0010': 'st',       # store to memory
    '0011': 'add',      # add registers
    '0100': 'mov',      # move register→register
    '0101': 'ldri',     # load indirect from [r15]
    '0110': 'label',    # declare a label
    '0111': 'and',      # bitwise AND
    '1000': 'or',       # bitwise OR
    '1001': 'inc',      # increment register
    '1010': 'dec',      # decrement register
    '1011': 'print',    # print (char or number)
    '1100': 'ldi',      # load immediate into register
    '1101': 'sti',      # store immediate into memory
    '1110': 'loop',     # conditional loop jump
    '1111': 'read'      # user input read
}

def binary_to_int(bs): return int(bs, 2)

def load_program(fn):
    raw   = open(fn).read()
    clean = ''.join(c for c in raw if c in '01')
    return [ clean[i:i+24] for i in range(0, len(clean), 24) ]

def execute_instruction(instr):
    global pc
    op    = instr[:4]
    r1    = binary_to_int(instr[4:8])
    r2    = binary_to_int(instr[8:12])
    imm8  = binary_to_int(instr[16:24])
    addr  = binary_to_int(instr[4:12])  # for ld/st/sti

    cmd = OPCODES.get(op)
    if   cmd == 'nop':
        pass

    if   cmd == 'mov':
        registers[r1] = registers[r2]

    elif cmd == 'ldri':
        # r2 holds the address pointer, r1 is the target register
        addr = registers[15]            # grab the pointer from
        registers[r1] = memory[addr]    # load that memory cell into r1

    # --- read: write into memory at [r15], then bump r15 ---
    elif cmd == 'read':
        line = input().strip()
        parts = line.split(maxsplit=1)
        length = 0

        # --- keyword 'val': parse a number into register r1 ---
        if parts[0].lower() == 'val' and len(parts) > 1:
            try:
                num = int(parts[1])
            except ValueError:
                num = 0
            memory[registers[15]] = num & 0xFF
            registers[15] = (registers[15] + 1) & 0xFF

        elif all(c in '10' for c in ''.join(line.split())):
            line = ''.join(line.split())
            num = int(line, 2)
            memory[registers[15]] = num
            registers[15] = (registers[15] + 1) & 0xFF

        # --- otherwise, string‐mode: store each char into memory at [r15] ---
        else:
            for ch in line:
                memory[registers[15]] = ord(ch)
                # advance buffer pointer
                registers[15] = (registers[15] + 1) & 0xFF
                length += 1
            registers[2] = length

    # --- label: record this pc under ID = imm8 ---
    elif cmd == 'label':
        labels[imm8] = pc

    # --- loop: if condition(r2) true, jump to labels[imm8] ---
    elif cmd == 'loop':
        # interpret register value as signed 8‑bit
        v = registers[r2]
        # if v & 0x80: v -= 0x100
        cond = r1
        take = (
            (cond == 0 and v == 0) or
            # (cond == 1 and v <  0) or
            (cond == 2 and v >  0)
        )
        if take:
            pc = labels.get(imm8, pc)
            return

    # --- the rest unchanged ---
    elif cmd == 'ld':
        registers[r1] = memory[addr]
    elif cmd == 'ldi':
        registers[r1] = imm8
    elif cmd == 'st':
        memory[addr] = registers[r1]
    elif cmd == 'sti':
        memory[addr] = imm8
    elif cmd == 'add':
        registers[r1] = (registers[r1] + registers[r2]) & 0xFF
    elif cmd == 'and':
        registers[r1] &= registers[r2]
    elif cmd == 'or':
        registers[r1] |= registers[r2]
    elif cmd == 'inc':
        registers[r1] += 1 & 0xFF
    elif cmd == 'dec':
        registers[r1] -= 1 & 0xFF
    elif cmd == 'print':
        if r2 == 1:
            print(registers[r1])
        else:
            print(chr(registers[r1]), end='')
    else:
        print(f"Unknown opcode {op}")

    pc += 1

def run_program(instrs):
    global pc
    while pc < len(instrs):
        execute_instruction(instrs[pc])

if __name__ == "__main__":
    prog = load_program("repeater.txt")
    run_program(prog)
