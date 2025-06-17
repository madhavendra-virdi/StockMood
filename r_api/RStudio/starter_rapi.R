library(plumber)
pr("rstudioapi.R") %>%
  pr_run(host = "0.0.0.0", port = 8000)

getwd()
setwd("C:/Users/command centre/Desktop/RStudio")
