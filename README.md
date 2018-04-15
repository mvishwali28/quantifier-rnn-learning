## Quantifier RNN learning (NLU project)

### Run on HPC

First, follow the instructions on ["Logging in to the NYU HPC Clusters"](https://wikis.nyu.edu/display/NYUHPC/Logging+in+to+the+NYU+HPC+Clusters) to log into the Prince cluster.

If you already have an account and just want to run things, you should be able to do so like this:

```
$ ssh -L 8026:prince:22 netID@gw.hpc.nyu.edu
$ ssh prince
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
(nlu)[netID@log-0 ~]$ pip install tensorflow-gpu
(nlu)[netID@log-0 ~]$ pip install pandas
```

Use `srun` to request a new GPU node for interactive use:

```
(nlu)[netID@log-0 ~]$ srun --gres=gpu:1 --pty bash
```

Run the training script on the GPU node:

```
(nlu)[netID@gpu-24 quantifier-rnn-learning]$ python quant_verify.py --exp one_a --out_path data/<dir>
```
