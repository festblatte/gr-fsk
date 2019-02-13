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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fsk_demod_c_ff import fsk_demod_c_ff
import math

class qa_fsk_demod_c_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        src_data = [0,0,0,0,0,0,0,0,0,0]
        for i in range(10):
            src_data[i] = math.cos(1*math.pi/5 * i) + math.sin(1*math.pi/5 * i) * 1j

        print(src_data)
        src_data = tuple(src_data)
        #print(src_data)
        #src_data = (3+2j,-2+1j,5-2j,0j)
        expected_result1 = (1, 2, 3, 4, 5)
        expected_result2 = (1, 1.61803, 1.61803, 1, 0)
        src = blocks.vector_source_c(src_data)
        fsk_demod = fsk_demod_c_ff(5,10,30,100)
        snk1 = blocks.vector_sink_f()
        snk2 = blocks.vector_sink_f()
        self.tb.connect(src, fsk_demod)
        self.tb.connect((fsk_demod,0), snk1)
        self.tb.connect((fsk_demod,1), snk2)

        self.tb.run ()
        
        result_data1 = snk1.data()
        result_data2 = snk2.data()
        self.assertFloatTuplesAlmostEqual(expected_result1, result_data1, 4)
        self.assertFloatTuplesAlmostEqual(expected_result2, result_data2, 4)


if __name__ == '__main__':
    gr_unittest.run(qa_fsk_demod_c_ff, "qa_fsk_demod_c_ff.xml")
