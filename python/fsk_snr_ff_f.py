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

class fsk_snr_ff_f(gr.sync_block):
    """
    docstring for block fsk_snr_ff_f
    """
    def __init__(self, omega):
        self.omega = omega

        self.d_min = 0
        self.d_plus = 0

        gr.sync_block.__init__(self,
            name="fsk_snr_ff_f",
            in_sig=[numpy.float32, numpy.float32],
            out_sig=[numpy.float32])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]

        for i in range(0,len(in0)):

            #self.d_min = (1-self.omega) * self.d_min + self.omega * abs(in0[i]*in0[i] - in1[i]*in1[i])
            #self.d_plus = (1-self.omega) * self.d_plus + self.omega * (in0[i]*in0[i] + in1[i]*in1[i])

            self.d_min = (1-self.omega) * self.d_min + self.omega * abs(in0[i] - in1[i])
            self.d_plus = (1-self.omega) * self.d_plus + self.omega * (in0[i] + in1[i])

            x = (self.d_plus - self.d_min)

            if x != 0:
                snr = 2* self.d_min / x
            else:
                out[i] = 0
                continue
            if snr != 0:
                out[i] = 10 * numpy.log10(snr)
            else:
                out[i] = 0

        return len(output_items[0])

