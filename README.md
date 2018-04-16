## Quantifier RNN learning (NLU project)

### Run on HPC

First, follow the instructions on ["Logging in to the NYU HPC Clusters"](https://wikis.nyu.edu/display/NYUHPC/Logging+in+to+the+NYU+HPC+Clusters) to log into the Prince cluster.

If you already have an account and just want to run things, you should be able to do so like this:

```
$ ssh -L 8026:prince:22 netID@gw.hpc.nyu.edu
netID@hpc-bastion1~>$ ssh prince
```

Once you're logged into Price, clone the GitHub repository:

```
[netID@log-0 ~]$ git clone https://github.com/mvishwali28/quantifier-rnn-learning
```

Load Anaconda for Python 3, create a new environment, and activate it:

```
[netID@log-0 ~]$ module load anaconda3/4.3.1
[netID@log-0 ~]$ conda create -n nlu python=3.6
[netID@log-0 ~]$ source activate nlu
```

Install the following dependencies using `pip`:

```
(nlu) [netID@log-0 ~]$ pip install tensorflow tensorflow-gpu pandas
```

Use `srun` to request a new GPU node for interactive use:

```
(nlu) [netID@log-0 ~]$ srun --gres=gpu:1 --pty /bin/bash
(nlu) [netID@log-0 ~]$ nvidia-smi
```

Run the training script on the GPU node:

```
(nlu) [netID@gpu-24 ~]$ cd quantifier-rnn-learning
(nlu) [netID@gpu-24 quantifier-rnn-learning]$ python quant_verify.py --exp one_a --out_path data/<dir>
```

When you're done, exit the GPU node, deactivate the environment, and log out of Prince:

```
(nlu) [netID@gpu-24 quantifier-rnn-learning]$ exit
(nlu) [netID@log-0 ~]$ source deactivate
[netID@log-0 ~]$ logout
```
