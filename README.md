# 1010+
This project is a CPU emulator that interprets 24-bit binary instructions, based off of x86 Assembly and the SRC that you do in Computer Organization & Architecture at OC. It simulates basic CPU behavior with general-purpose registers, memory, labels, and simple I/O.

## Overview
This emulator provides:

- 16 general-purpose registers (r0–r15)

- 256 bytes of memory

- A binary instruction set with 16 unique operations

- Label-based control flow and conditional looping

- Input and output handling (numbers, strings, binary)

This project allows for those interested in low-level programming to have their own machine code that they can interact with and edit.

## Architecture
Registers
r0 to r15: 8-bit general-purpose registers

Special usage:
r1 → ax
r2 → cx
r15 → di (often used as a memory pointer)

Memory
256 bytes (indexed 0 to 255)

Addressable using registers or direct addressing

Program Counter
pc keeps track of the current instruction

## Instruction Format
Each instruction is 24-bits wide, in the following format:

[ 4-bit opcode ][ 4-bit destination & value register (r1) ][ 4-bit value register (r2) ][ 8-bit unused or immediate ]
Some instructions interpret this differently based on operation.

## Opcodes
| **Binary** | **Mnemonic** | **Description**                                  |
|------------|--------------|--------------------------------------------------|
| 0000       | nop          | No operation                                     |
| 0001       | ld           | Load from memory into register                   |
| 0010       | st           | Store register value into memory                 |
| 0011       | add          | Add r2 to r1                                     |
| 0100       | mov          | Copy value from r2 to r1                         |
| 0101       | ldri         | Load from memory address in r15                  |
| 0110       | label        | Define a label with ID = imm8                    |
| 0111       | and          | Bitwise AND between r1 and r2                    |
| 1000       | or           | Bitwise OR between r1 and r2                     |
| 1001       | inc          | Increment register                               |
| 1010       | dec          | Decrement register                               |
| 1011       | print        | Output value of register (char or int)           |
| 1100       | ldi          | Load immediate 8-bit value into register         |
| 1101       | sti          | Store immediate into memory                      |
| 1110       | loop         | Conditional loop to label                        |
| 1111       | read         | Input value into memory at pointer `r15`         |

## Input Format
The read instruction accepts:

- val \<number\> → store number as byte

- binary strings like 01010101

- regular strings → each character stored individually

- r15 is auto-incremented as input is stored.

## Labels and Control Flow
label imm8: Marks the current instruction with ID = imm8

loop cond r2 imm8: Jumps to label if condition is true for r2

cond = 0 → jump if r2 == 0

cond = 2 → jump if r2 > 0

## Example Program File
Program files (e.g., repeater.txt) are plain text files containing 24-bit binary instructions. Comments and extra characters are ignored.

0001 0001 0000 0000 0000 0000   ; ld r1, mem[0]
1100 1100 0000 0000 0000 0101   ; ldi r3, 5

## Usage
- Add your binary instructions into a file (e.g. repeater.txt).
- Pass that filename into the "load_program" function
- Run the emulator

python3 1010+.py

## Notes
All values are 8-bit (0–255); arithmetic wraps around.

Instructions are pure binary strings (24 bits each).
