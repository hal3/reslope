# Residual Loss Prediction: Reinforcement Learning with No Incremental Feedback


An implemntation for our [paper](https://openreview.net/pdf?id=HJNMYceCW): residual loss prediction: reinforcement learning with no intermediate feedback. If you find this code useful in your research, please consider citing:

        @article{daume2018residual,
          title={Residual Loss Prediction: Reinforcement Learning With No Incremental Feedback},
          author={Daum{\'e} III, Hal and Langford, John and Sharaf, Amr},
          journal={International Conference on Learning Representations (ICLR)},
          year={2018}
        }

To run:


        python run_reslope.py grid::0.05::0.9::0.99 blols::mtr::multidev::bootstrap adam 0.01 bag_size=3 --dynet-seed 3
        
This command will run relope on the grid world enviroment with the following parameters:

1) Run relope in multiple deviation model
2) Use Multi-task regression (MTR) contextual bandit oracle, MTR reduces contextual bandit costs directly to importance-weighted regression.
3) Use bootrap exploration for the contexual bandit oracle with a bag size of three policies.

The code has a dependency on the macarico github repo, and the dynet branch is required to run this code base.
