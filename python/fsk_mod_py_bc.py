#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Tim Horst.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class fsk_mod_py_bc(gr.interp_block):
    """
    docstring for block fsk_mod_py_bc
    """
    def __init__(self, sampPerSym):

        self.sampPerSym = sampPerSym

        self.pattern = numpy.zeros((2,2,self.sampPerSym),dtype = complex)

        piPerSamp = numpy.pi / self.sampPerSym
        piRange = numpy.arange(0, numpy.pi, piPerSamp) + piPerSamp
        #print piRange
        self.pattern[0,0] = numpy.cos(piRange) + numpy.sin(piRange + numpy.pi)* 1j
        self.pattern[0,1] = numpy.cos(piRange + numpy.pi) + numpy.sin(piRange) * 1j
        self.pattern[1,0] = numpy.cos(piRange) + numpy.sin(piRange[::-1] - piPerSamp)* 1j
        self.pattern[1,1] = numpy.cos(piRange + numpy.pi) + numpy.sin(piRange[::-1] + numpy.pi - piPerSamp) * 1j
        #rint self.pattern
        self.phase = 0

        gr.interp_block.__init__(self,
            name="fsk_mod_py_bc",
            in_sig=[numpy.uint8],
            out_sig=[numpy.complex64], interp = self.sampPerSym)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for i in range(0,len(in0)):
            if in0[i] == 1:
                out[i*self.sampPerSym:(i+1)*self.sampPerSym] = self.pattern[1,self.phase]
            else:
                out[i*self.sampPerSym:(i+1)*self.sampPerSym] = self.pattern[0,self.phase]

            if self.phase == 0:
                self.phase = 1
            else:
                self.phase = 0

        return len(output_items[0])

