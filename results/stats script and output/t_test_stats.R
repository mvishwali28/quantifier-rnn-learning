
#setwd("C:\\Users\\Sheng-Fu\\local_codebase\\quantifier-rnn-learning\\results\\")
library(tidyverse)


t_test_at_step_x <- function(folder_path = "", step = 1, q1 = "all", q2 = "only") {
  file_list_1 <- list.files(path=paste(folder_path, "\\run_1\\", sep = ""), pattern="*.csv")
  data1 <- 
    do.call("rbind", 
            lapply(file_list_1, 
                   function(x) 
                     read.csv(paste(paste(folder_path, "\\run_1\\", sep = ""), x, sep=''), 
                              stringsAsFactors = FALSE)))
  
  file_list_2 <- list.files(path=paste(folder_path, "\\run_2\\", sep = ""), pattern="*.csv")
  data2 <- 
    do.call("rbind", 
            lapply(file_list_2, 
                   function(x) 
                     read.csv(paste(paste(folder_path, "\\run_3\\", sep = ""), x, sep=''), 
                              stringsAsFactors = FALSE)))
  file_list_3 <- list.files(path=paste(folder_path, "\\run_3\\", sep = ""), pattern="*.csv")
  data3 <- 
    do.call("rbind", 
            lapply(file_list_2, 
                   function(x) 
                     read.csv(paste(paste(folder_path, "\\run_3\\", sep = ""), x, sep=''), 
                              stringsAsFactors = FALSE)))
  
  data = rbind(data1, data2, data3)
  data_50 = filter(data, global_step == step) 
  result = list()
  result[[1]] = t.test(data_50[[paste(q1, "_accuracy", sep = "")]],data_50[[paste(q2, "_accuracy", sep = "")]], paired=TRUE)
  result[[2]] = data_50
  return(result)
}

t_test_sweep_steps <- function(folder_path = "", step_start = 1, step_end = 51, 
                               q1 = "all", q2 = "only", group = "none", output_file = "stats_output.csv"){
  steps = seq(step_start, step_end, 50)
  for (step in steps){
    output = t_test_at_step_x(folder_path, step, q1=q1, q2=q2)
    #print(output[[1]]$p.value)
    if (output[[1]]$p.value < 0.05){
      if (output[[1]]$estimate > 0){
        #print(paste(paste(q1, ">", q2), step, ',', output[[1]]$p.value))
        cat(group, step, paste(q1, ">", q2), 
            mean(output[[2]][[paste(q1, "_accuracy", sep="")]]), mean(output[[2]][[paste(q2, "_accuracy", sep="")]]),  
            output[[1]]$statistic, paste(output[[1]]$p.value, "\n", sep = ""),
            file=output_file, sep = ",", append = T)
      }
      else {
        #print(paste(paste(q1, "<", q2), step, ',', output[[1]]$p.value))
        cat(group, step, paste(q1, "<", q2), 
            mean(output[[2]][[paste(q1, "_accuracy", sep="")]]), mean(output[[2]][[paste(q2, "_accuracy", sep="")]]),  
            output[[1]]$statistic, paste(output[[1]]$p.value, "\n", sep = ""),
            file=output_file, sep = ",", append = T)
      }
    }
  }
}

cat("group","step", "direction", "all_acc", "only_acc", "t", "p\n", file="stats_output_All_vs_Only.csv", sep = ",")

t_test_sweep_steps("30k\\exp-1-a", 
                   1, 3001, group = "30k-4c:0nc", output_file = "stats_output_All_vs_Only.csv")

t_test_sweep_steps("30k\\exp-1-b", 
                   1, 3001, group = "30k-3c:1nc",  output_file = "stats_output_All_vs_Only.csv")

t_test_sweep_steps("30k\\exp-1-c", 
                   1, 3001, group = "30k-2c:2nc",  output_file = "stats_output_All_vs_Only.csv")

t_test_sweep_steps("30k\\exp-1-d", 
                   1, 3001, group = "30k-1c:3nc", output_file = "stats_output_All_vs_Only.csv")

t_test_sweep_steps("30k\\exp-1-e", 
                   1, 3001, group = "30k-0c:4nc", output_file = "stats_output_All_vs_Only.csv")


cat("group","step", "direction", "most_AB", "not_all", "t", "p\n", file="stats_output_Most_AB_vs_Not_All.csv", sep = ",")

t_test_sweep_steps("30k\\exp-1-a", 
                   1, 3001, group = "30k-4c:0nc", output_file = "stats_output_Most_AB_vs_Not_All.csv", q2 = "not_all", q1 = "most_AB")

t_test_sweep_steps("30k\\exp-1-b", 
                   1, 3001, group = "30k-3c:1nc",  output_file = "stats_output_Most_AB_vs_Not_All.csv", q2 = "not_all", q1 = "most_AB")

t_test_sweep_steps("30k\\exp-1-c", 
                   1, 3001, group = "30k-2c:2nc",  output_file = "stats_output_Most_AB_vs_Not_All.csv", q2 = "not_all", q1 = "most_AB")


cat("group","step", "direction", "most_BA", "not_only", "t", "p\n", file="stats_output_Most_BA_vs_Not_Only.csv", sep = ",")

t_test_sweep_steps("30k\\exp-1-c", 
                   1, 3001, group = "30k-2c:2nc", output_file = "stats_output_Most_BA_vs_Not_Only.csv", q2 = "not_only", q1 = "most_BA")

t_test_sweep_steps("30k\\exp-1-d", 
                   1, 3001, group = "30k-1c:3nc",  output_file = "stats_output_Most_BA_vs_Not_Only.csv", q2 = "not_only", q1 = "most_BA")

t_test_sweep_steps("30k\\exp-1-e", 
                   1, 3001, group = "30k-0c:4nc",  output_file = "stats_output_Most_BA_vs_Not_Only.csv", q2 = "not_only", q1 = "most_BA")



cat("group","step", "direction", "most_AB", "all", "t", "p\n", file="stats_output_Most_AB_vs_All.csv", sep = ",")

t_test_sweep_steps("30k\\exp-1-a", 
                   1, 3001, group = "30k-4c:0nc", output_file = "stats_output_Most_AB_vs_All.csv", q2 = "all", q1 = "most_AB")

t_test_sweep_steps("30k\\exp-1-b", 
                   1, 3001, group = "30k-3c:1nc",  output_file = "stats_output_Most_AB_vs_All.csv", q2 = "all", q1 = "most_AB")

t_test_sweep_steps("30k\\exp-1-c", 
                   1, 3001, group = "30k-2c:2nc",  output_file = "stats_output_Most_AB_vs_All.csv", q2 = "all", q1 = "most_AB")


cat("group","step", "direction", "most_BA", "only", "t", "p\n", file="stats_output_Most_BA_vs_Only.csv", sep = ",")

t_test_sweep_steps("30k\\exp-1-c", 
                   1, 3001, group = "30k-2c:2nc", output_file = "stats_output_Most_BA_vs_Only.csv", q2 = "only", q1 = "most_BA")

t_test_sweep_steps("30k\\exp-1-d", 
                   1, 3001, group = "30k-1c:3nc",  output_file = "stats_output_Most_BA_vs_Only.csv", q2 = "only", q1 = "most_BA")

t_test_sweep_steps("30k\\exp-1-e", 
                   1, 3001, group = "30k-0c:4nc",  output_file = "stats_output_Most_BA_vs_Only.csv", q2 = "only", q1 = "most_BA")

##pull out mean and median for all and only


exps = c("exp-1-a\\", "exp-1-b\\", "exp-1-c\\", "exp-1-d\\", "exp-1-e\\")
runs = c("run_1\\", "run_2\\", "run_3\\")




overall_data <- data.frame(
  all_accuracy=numeric(),
  only_accuracy=numeric(),
  global_step = numeric(),
  stringsAsFactors=FALSE
)


for (exp in exps){
  for (run in runs){
    file_list = list.files(path = paste(exp, run, sep = ""), pattern="*.csv")
    data_temp <- 
      do.call("rbind", 
              lapply(file_list, 
                     function(x) 
                       read.csv(paste(paste(exp, run, sep = ""), x, sep=''), 
                                stringsAsFactors = FALSE)))

    data_temp = select(data_temp, all_accuracy, only_accuracy, global_step)
    overall_data = rbind(overall_data, data_temp)
    
  }
}

dim(overall_data)

final_stage = filter(overall_data, global_step == 12701)
dim(final_stage)

print('range: all')
print(range(final_stage$all_accuracy))
print('mean: all')
print(mean(final_stage$all_accuracy))
print('median: all')
print(median(final_stage$all_accuracy))
print('range: only')
print(range(final_stage$only_accuracy))
print('mean: only')
print(mean(final_stage$only_accuracy))
print('median: only')
print(median(final_stage$only_accuracy))

