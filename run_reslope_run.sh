#!/bin/bash

run="PYTHONPATH=/cliphomes/hal/projects/macarico /cliphomes/hal/py/bin/python"

lm=0
exp=0
temp=1
bl=0.0
uni=True
md=None
upc=True
ot=True
rs=20001
num_reps=5

# bandit lols
n=0
method=banditlols
for lm in 0 1 2 3 ; do
    for exp in 0 1 ; do
	for temp in 0.2 0.5 1.0 ; do
	    for upc in True False ; do
		for ot in True False ; do
		    for lr in 0.0005 0.001 0.002 0.005 0.01 0.02 ; do
			for loss in squared huber ; do
			    echo qsh $run run_reslope.py $lm $exp $temp $bl $uni $md $upc $ot $method $lr $loss $rs $num_reps \\\>\\\& reslope_out/lols.$n
			    let n=$n+1
			done
		    done
		done
	    done
	done
    done
done

# reinforce
n=0
method=reinforce
for temp in 0.2 0.5 1.0 2.0 5.0 ; do
    for bl in 0.0 0.8 ; do
	for uni in True False ; do
	    for md in None 1 ; do
		for lr in 0.0005 0.001 0.002 0.005 0.01 0.02 ; do
		    echo qsh $run run_reslope.py $lm $exp $temp $bl $uni $md $upc $ot $method $lr $loss $rs $num_reps \\\>\\\& reslope_out/reinforce.$n
		    let n=$n+1
		done
	    done
	done
    done
done

