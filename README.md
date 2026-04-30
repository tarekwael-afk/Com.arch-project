# Assembler Design Project

## Project Title
Simple Two-Pass Assembler Using Python

## Description
This project is a Python-based assembler that converts assembly language instructions into machine code in hexadecimal format.

The assembler reads an assembly source file (`sample.asm`), analyzes the instructions, detects labels, and generates the corresponding machine code in an output file (`output.hex`).

## Objectives
- Convert assembly language into machine code.
- Understand how assemblers work.
- Implement the two-pass assembler technique.
- Generate hexadecimal output automatically.

## How It Works

### First Pass
The program scans the source code and stores all labels with their memory addresses in a symbol table.

### Second Pass
The program translates instructions into machine code using opcode values and replaces labels with their addresses.

## Supported Instructions

| Instruction | Opcode |
|------------|--------|
| LOAD       | 1      |
| STORE      | 2      |
| ADD        | 3      |
| SUBT       | 4      |
| INPUT      | 5      |
| OUTPUT     | 6      |
| HALT       | 7      |
| JUMP       | 9      |
| CLEAR      | A      |

## Files Included

- `assembler.py` → Main Python program  
- `sample.asm` → Sample assembly input file  
- `output.hex` → Generated machine code output  
- `README.md` → Project documentation

## Example Input (`sample.asm`)

```assembly
LOAD X
ADD Y
STORE Z
OUTPUT
HALT
X, DEC 5
Y, DEC 3
Z, DEC 0
