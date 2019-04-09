# Residual Loss Prediction: Reinforcement Learning with No Incremental Feedback


An implementation for our [paper](https://openreview.net/pdf?id=HJNMYceCW): residual loss prediction: reinforcement learning with no incremental feedback. If you find this code useful in your research, please consider citing:

        @article{daume2018residual,
          title={Residual Loss Prediction: Reinforcement Learning With No Incremental Feedback},
          author={Daum{\'e} III, Hal and Langford, John and Sharaf, Amr},
          journal={International Conference on Learning Representations (ICLR)},
          year={2018}
        }

To run:


        python run_reslope.py grid::0.05::0.9::0.99 blols::mtr::multidev::bootstrap adam 0.01 bag_size=3 --dynet-seed 3
        
This command will run reslope on the grid world environment with the following parameters:

1) Run reslope in multiple deviation mode
2) Use Multi-task regression (MTR) contextual bandit oracle, MTR reduces contextual bandit costs directly to importance-weighted regression.
3) Use bootstrap exploration for the contexual bandit oracle with a bag size of three policies.

The code has a dependency on the macarico github repo, and the dynet branch is required to run this code base.

## Examples

This command will run the reinforce algorithm on the blackjack environment:

        python run_reslope.py blackjack reinforce adam 0.01 --dynet-seed 90210
        
This command will run the PPO algorithm on the cartpole enviroment:

        python run_reslope.py cartpole ppo::k=3::n=20::m=1 adam 0.01 --dynet-seed 3
