#!/bin/bash

mkdir reslope_sup

for opt in adam rmsprop adagrad ; do
    for lr in 0.001 0.004 0.01 0.04 0.1 0.4 1.0 4.0 ; do
	for alg in dagger aggrevate ; do
	    for p_rin in 0.0 0.999 0.99999 1.0 ; do
		for task in pos-tweet dep-tweet ctb-nw ; do
		    fname="$opt"_"$lr"_"$alg"_"$p_rin"_"$task"_"noembed"
		    slush \
			PYTHONPATH=/fs/clip-ml/hal/projects/macarico \
		        /fs/clip-ml/hal/pyd/bin/python run_reslope.py \
			$task \
			$alg::p_rin=$p_rin \
			$opt \
			$lr \
			reps=5 \
			save=reslope_sup/$fname.model \
                        supervised \
			\> reslope_sup/$fname.err 2\>\&1

		    fname="$opt"_"$lr"_"$alg"_"$p_rin"_"$task"
		    slush \
			PYTHONPATH=/fs/clip-ml/hal/projects/macarico \
		        /fs/clip-ml/hal/pyd/bin/python run_reslope.py \
			$task \
			$alg::p_rin=$p_rin \
			$opt \
			$lr \
			reps=5 \
			embed=yes \
			save=reslope_sup/$fname.model \
                        supervised \
			\> reslope_sup/$fname.err 2\>\&1
		done
	    done
	done
    done
done
