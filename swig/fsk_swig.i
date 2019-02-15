/* -*- c++ -*- */

#define FSK_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "fsk_swig_doc.i"

%{
#include "fsk/clock_recovery_mm_ff.h"
%}


%include "fsk/clock_recovery_mm_ff.h"
GR_SWIG_BLOCK_MAGIC2(fsk, clock_recovery_mm_ff);
