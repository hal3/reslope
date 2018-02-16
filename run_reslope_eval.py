from __future__ import division
import numpy as np
import random
import sys
import json
import re
from matplotlib.pyplot import *

def bandit_curve(run):
    return np.array([x[0][0] / run['length'] for x in run['history']])

def dev_curve(run):
    return np.array([x[1][0] / run['length'] for x in run['history']])

def bandit_best(run):
    return bandit_curve(run).min()

def dev_best(run):
    return dev_curve(run).min()

bandit_threshold = 0.3
dev_threshold = 0.6

def plot1(data, fn=bandit_curve, **kwargs):
    data_ = [run for run in data \
             if all([run[k] == v for k, v in kwargs.iteritems()])]
    Y = np.stack([fn(run)[:16] for run in data_], axis=1)
    N = Y.shape[0]
    errorbar(np.arange(1,17),
             Y.mean(axis=1),
             yerr=1.96 * Y.std(axis=1) / np.sqrt(N))
    xlabel('log_2(amount of data)')
    ylabel('error')
    show(False)

def plot_many(data, fn=bandit_curve, **kwargs):
    vary_k = [k for k, v in kwargs.iteritems() if isinstance(v, list)]
    assert len(vary_k) >= 1
    num_vary_k = len(kwargs[vary_k[0]])
    assert all([len(kwargs[v]) == num_vary_k for v in vary_k])
    vary_v = [kwargs[k][:] for k in vary_k]
    for v_list in zip(*vary_v):
        for k, v in zip(vary_k, v_list):
            del kwargs[k]
            kwargs[k] = v
        plot1(data, fn=fn, **kwargs)
    legend([', '.join(['%s=%s' % (k, v) for k, v in zip(vary_k, v_list)]) for v_list in zip(*vary_v)])
    for k, v in zip(vary_k, v_list):
        del kwargs[k]
    title(' | '.join(['%s=%s' % (k, v) for k, v in kwargs.iteritems()]))
    show(False)

def plot_blols_vs_reinforce(data):
    figure()
    for x, n_labels in enumerate([4, 8, 16]):
        for y, length in enumerate([5, 10, 20]):
            subplot(3,3,x*3+y+1)
            plot_many(data, bandit_curve, n_types=160, n_labels=n_labels, length=length, learning_method=[0,2], exploration=0, reinforce=[True,False])
    show(False)
    
def bandit_success(run):
    return bandit_best(run) <= bandit_threshold

def dev_success(run):
    return dev_best(run) <= dev_threshold

def bandit_first_success(run):
    curve = bandit_curve(run)
    try:
        return list(curve < bandit_threshold).index(True)
    except ValueError:
        return len(curve)+1

def fraction(f, me):
    n = sum(map(f,me))
    d = len(me)
    return '%g%% [%d/%d]' % (100*n/d, n, d)

def print_stats(data):
    all_vals = dict(n_labels=set(), length=set(), n_types=set(),
                    exploration=set(), learning_method=set())
    for run in data:
        for k in all_vals.iterkeys():
            all_vals[k].add(run[k])

    print '#key\tval\tbandit_suc\tdev_suc'
    for k in all_vals.iterkeys():
        for v in sorted(all_vals[k]):
            me = [run for run in data if run[k] == v]
            print '%s\t%s\t%s\t%s' % \
                (k, v,
                 fraction(bandit_success, me),
                 fraction(dev_success, me),
                 )
        print ''

def read_reslope(s):
    m = re.match('reslope/res.([0-9]+).([0-9]+).([0-9]+).([0-9]+).([0-9]+).([0-9]+)\.?([^:]*):(.+)', s)
    #$lm.$exp.$n_types.$n_labels.$length.$rs
    length = int(m.groups()[4])
    j = json.loads(m.groups()[7])
    j['length'] = length
    j['bow'] = 'bow' in s
    j['reinforce'] = 'reinforce' in s
    if len(m.groups()[6]) > 0 and m.groups()[6].isdigit():
        j['temperature'] = int(m.groups()[6])
    else:
        j['temperature'] = 1
    return j
        
if __name__ == '__main__' and len(sys.argv) == 2:
    data = map(read_reslope, open(sys.argv[1]))

    print '\n### OVERALL\n'
    print_stats(data)

    print '\n### BIASED ESTIMATOR ONLY\n'
    print_stats([run for run in data if run['learning_method'] == 0])

    print '\n### IPS ESTIMATOR ONLY\n'
    print_stats([run for run in data if run['learning_method'] == 1])

    print '\n### DR ESTIMATOR ONLY\n'
    print_stats([run for run in data if run['learning_method'] == 2])
    
