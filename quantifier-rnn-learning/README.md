## Quantifier RNN learning (NLU project)

### Run on HPC

First, follow the instructions on ["Logging in to the NYU HPC Clusters"](https://wikis.nyu.edu/display/NYUHPC/Logging+in+to+the+NYU+HPC+Clusters) to log into the Prince cluster.

If you already have an account and just want to run things, you should be able to log into Prince like this:

```
$ ssh -L 8026:prince:22 netID@gw.hpc.nyu.edu
netID@hpc-bastion1~>$ ssh prince
```

Next, clone the GitHub repository and load the following modules:

```
[netID@log-0 ~]$ git clone https://github.com/mvishwali28/quantifier-rnn-learning
[netID@log-0 ~]$ module load anaconda3/4.3.1 cuda/9.0.176 cudnn/9.0v7.0.5
[netID@log-0 ~]$ module list  # Check currently loaded modules
```

Create a new `conda` environment, activate it, and install the required dependencies using `pip`:

```
[netID@log-0 ~]$ conda create -n nlu python=3.6
[netID@log-0 ~]$ source activate nlu
(nlu) [netID@log-0 ~]$ pip install pandas tensorflow-gpu
```

#### Interactive

Use `srun` to request a bash command shell session with 1 GPU node:

```
(nlu) [netID@log-0 ~]$ srun --gres=gpu:1 --pty /bin/bash
```

Run the training script:

```
(nlu) [netID@gpu-xx ~]$ cd quantifier-rnn-learning
(nlu) [netID@gpu-xx quantifier-rnn-learning]$ python quant_verify.py --exp one_a --out_path data/<dir>  # Replace <dir> with the name of your desired output directory
```

#### Using `sbatch`

Alternatively, modify and run the bash script using `sbatch`:

```
(nlu) [netID@log-0 quantifier-rnn-learning]$ sbatch run-exp_x_x.sh
Submitted batch job 123
```

Slurm will then generate a log file containing all the output called `slurm-123.out` in the same directory.
An output file will be generated in the same directory that would have the results from the terminal.
Once you have a job running on HPC, here are some useful commands:

- `squeue -u <user_ID>`: list all your jobs and allocated resources
- `scancel <job_ID>`: end/cancel a job
- `scancel -u <user_ID>`: cancel all your jobs
- `sinfo`: get current status of all GPUs and CPUs

You can also `ssh` into the GPU node your job is running on and check how much processing power you are using:

```
(nlu) [netID@log-0 quantifier-rnn-learning]$ ssh gpu-xx
(nlu) [netID@gpu-xx ~]$ nvidia-smi
Sun Apr 15 21:15:43 2018
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 384.81                 Driver Version: 384.81                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           On   | 00000000:0F:00.0 Off |                    0 |
| N/A   34C    P0    75W / 149W |  10896MiB / 11439MiB |      0%   E. Process |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      3483      C   python                                     10883MiB |
+-----------------------------------------------------------------------------+
```

Other useful Linux commands:

- `watch`
- `top`
- `htop`
- `pstree`

When you're done, exit the GPU node, deactivate the environment, and log out of Prince:

```
(nlu) [netID@gpu-xx quantifier-rnn-learning]$ exit
(nlu) [netID@log-0 ~]$ source deactivate
[netID@log-0 ~]$ logout
```

### Divide and conquer

**Double check your bash script before you run it.**

**!** Make sure to replace `netID` with your actual ID so you can receive email notifications when your jobs are finished.

**!** Make sure you used `module load` to load the Anaconda/CUDA modules, otherwise TensorFlow will not actually run on the GPU.

**run-exp_1_x.sh trains with 10k training samples.**
**run-exp_1_2_x.sh trains with 30k training samples.**
**results files in both the bash scripts are different, so can be directly run.**
- `run-exp_1_a.sh` : Melanie
- `run-exp_1_b.sh` : Ildi
- `run-exp_1_c.sh` : Sheng-Fu
- `run-exp_1_d.sh` : Vishwali
- `run-exp_1_e.sh` : Melanie or Vishwali

The results are in two folders. 'Plots' only has the two test quantifiers over the 30 trials. 'Plots1' has the 6 quantifiers used in the experiment.
