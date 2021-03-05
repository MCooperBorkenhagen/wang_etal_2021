

# standard error of the mean
# calculate the mean, and y coordinates associated with the se of the mean
mean_se<- function(x) {
  m <- mean(x)
  se_min <- m-sqrt(var(x)/length(x))
  se_max <- m+sqrt(var(x)/length(x))
  return(c(m, se_min, se_max))
}









