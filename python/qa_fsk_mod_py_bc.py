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
from fsk_mod_py_bc import fsk_mod_py_bc

class qa_fsk_mod_py_bc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
    	src_data = (0,1,1,0,1,1)
    	expected_result = (3+0j,2+0j,1+0j,0j,0j,1+0j,2+0j,3+0j,0j,1+0j,2+0j,3+0j,3+0j,2+0j,1+0j,0j,0j,1+0j,2+0j,3+0j,0j,1+0j,2+0j,3+0j)
    	src = blocks.vector_source_b(src_data)
    	fsk_mod = fsk_mod_py_bc(4)
    	snk = blocks.vector_sink_c()
    	self.tb.connect(src, fsk_mod)
    	self.tb.connect(fsk_mod, snk)
        
        self.tb.run ()
        
        result_data = snk.data()
        self.assertComplexTuplesAlmostEqual(expected_result, result_data, 6)



if __name__ == '__main__':
    gr_unittest.run(qa_fsk_mod_py_bc, "qa_fsk_mod_py_bc.xml")
