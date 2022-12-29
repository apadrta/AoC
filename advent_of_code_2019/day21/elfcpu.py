#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Elf CPU Mk2010-15A
"""


class ElfCPU():
    """
    Class for running ELF CPU
    """

    def __init__(self):
        """
        Constructor
        """
        self.code = {}
        self.output = []
        self.inputs = []
        self.inputindex = 0
        self.ptr = 0
        self.offset = 0

    def read_code(self, filename):
        """
        Read program code from file
        """
        data = []
        with open(filename, "r") as fileh:
            data = fileh.read()
        rcode = [int(x) for x in data.strip().split(',')]
        i = 0
        self.code = {}
        for num in rcode:
            self.code[i] = num
            i += 1

    def reset(self):
        """
        Reset computer
        """
        self.code = {}
        self.output = []
        self.inputs = []
        self.inputindex = 0
        self.ptr = 0
        self.offset = 0

    def get_state(self):
        """
        Print CPU state (debug purpose)
        """
        return "PTR: {}, InputIndex = {}, Inputs: {}, Output: {}".format(
            self.ptr,
            self.inputindex,
            self.inputs,
            self.output)

    def get_output(self):
        """
        Provide output
        """
        return self.output

    def add_inputs(self, new_inputs):
        """
        Add new input array to current one
        """
        self.inputs = self.inputs + new_inputs

    def set_inputs(self, new_inputs):
        """
        Add input array
        """
        self.inputs = new_inputs
        self.inputindex = 0

    def init_var(self, index, mode):
        """
        Initialize variable
        """
        if mode == 1:
            # mode 1 = use number directly
            addr = self.ptr + index + 1
        if mode == 0:
            # mode 0 = use number as pointer
            addr = self.code[self.ptr + index + 1]
        elif mode == 2:
            # mode 2 = use number as pointer with offset
            addr = self.code[self.ptr + index + 1] + self.offset
        if addr not in self.code:
            self.code[addr] = 0
        return self.code[addr]

    def run(self):
        """
        Run the elf processor (or continue running when previously stopped)
        """
        maxparams = 3    # maxparams for instructions
        while True:
            # prepoces mode and opcode
            istr = "0" * (maxparams + 1) + str(self.code[self.ptr])
            opcode = int(istr[-2:])
            mode = [int(x) for x in istr[:-2][::-1]]

            # prepare mode parameters
            params = [0] * 3
            if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
                params[0] = self.init_var(0, mode[0])
            if opcode in [1, 2, 5, 6, 7, 8]:
                params[1] = self.init_var(1, mode[1])
            if opcode in []:
                params[2] = self.init_var(2, mode[2])

            if opcode == 99:
                # print("program completed")
                return 99
            if opcode == 1:
                # add
                if mode[2] == 2:
                    self.code[self.code[self.ptr + 3] + self.offset] = params[0] + params[1]
                else:
                    self.code[self.code[self.ptr + 3]] = params[0] + params[1]
                self.ptr += 4
            elif opcode == 2:
                # multiply
                if mode[2] == 2:
                    self.code[self.code[self.ptr + 3] + self.offset] = params[0] * params[1]
                else:
                    self.code[self.code[self.ptr + 3]] = params[0] * params[1]
                self.ptr += 4

            elif opcode == 3:
                # input
                if self.inputindex >= len(self.inputs):
                    # not enough inputs
                    return 3
                indata = self.inputs[self.inputindex]
                self.inputindex += 1
                if mode[0] == 2:
                    self.code[self.code[self.ptr + 1] + self.offset] = indata
                else:
                    self.code[self.code[self.ptr + 1]] = indata
                self.ptr += 2

            elif opcode == 4:
                # output
                self.output.append(params[0])
                self.ptr += 2

            elif opcode == 5:
                # jump-if-true
                if params[0] == 0:
                    self.ptr += 3
                else:
                    self.ptr = params[1]

            elif opcode == 6:
                # jump-if-false
                if params[0] == 0:
                    self.ptr = params[1]
                else:
                    self.ptr += 3

            elif opcode == 7:
                # less than
                if params[0] < params[1]:
                    val = 1
                else:
                    val = 0
                if mode[2] == 2:
                    self.code[self.code[self.ptr + 3] + self.offset] = val
                else:
                    self.code[self.code[self.ptr + 3]] = val
                self.ptr += 4

            elif opcode == 8:
                # equals
                if params[0] == params[1]:
                    val = 1
                else:
                    val = 0
                if mode[2] == 2:
                    self.code[self.code[self.ptr + 3] + self.offset] = val
                else:
                    self.code[self.code[self.ptr + 3]] = val
                self.ptr += 4

            elif opcode == 9:
                # change offset
                self.offset += params[0]
                self.ptr += 2

            else:
                print("ERROR: unknown instruction")
                return 666

# EOF
