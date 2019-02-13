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

def expj(phase):
        return numpy.cos(phase) + numpy.sin(phase)*1j


class fsk_demod_c_ff(gr.sync_block):
    """
    docstring for block fsk_demod_c_ff
    """
    def __init__(self, sampPerSym, f1, f2, samp_rate):
        self.sampPerSym = sampPerSym
        self.f1 = f1
        self.f2 = f2
        self.samp_rate = samp_rate
        self.dt = 1./samp_rate
        self.t = 0
        self.integrator = numpy.zeros((2,sampPerSym),dtype = complex)
        self.writeIndex = 0

        gr.sync_block.__init__(self,
            name="fsk_demod_c_ff",
            in_sig=[numpy.complex64],
            out_sig=[numpy.float32, numpy.float32])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]

        for i in range(0,len(in0)):
            freq = numpy.array([expj(-2*numpy.pi * self.f1 * self.t), \
                expj(-2*numpy.pi * self.f2 * self.t)])

            bb = freq * in0[i]
            self.integrator[:,self.writeIndex] = bb

            self.writeIndex = self.writeIndex + 1

            if self.writeIndex == self.sampPerSym:
                self.writeIndex = 0

            integ = numpy.sum(self.integrator, axis = 1)

            sigEnergy = numpy.absolute(integ)

            out0[i] = sigEnergy[0] 

            out1[i] = sigEnergy[1]

            self.t = self.t + self.dt
        
        

        return len(output_items[0])

