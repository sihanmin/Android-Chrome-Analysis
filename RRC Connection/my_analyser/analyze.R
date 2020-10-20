
data <- read.csv("Desktop/test1/dl_bytes1.csv")
comp_data <- read.csv("Desktop/test1/dl_comp1.csv")
status_data <- read.csv("Desktop/test1/rrc_status1.csv")
#data$Timestamp <- as.POSIXct(data$Timestamp)
data2 <- aggregate(. ~Timestamp, data=data, sum, na.rm=TRUE)

all_data <- merge(x = comp_data, y = data2, by = "Timestamp", all.x = TRUE)
all_data[ , 3][is.na(all_data[ , 3] ) ] = 0 
all_data$init.bytes <- NULL

all_data$log_dl.bytes <- log(all_data$dl.bytes+1)
all_data$sqrt_dl.bytes <- sqrt(all_data$dl.bytes)
all_data$cbrt_dl.bytes <- sign(all_data$dl.bytes) * abs(all_data$dl.bytes)^(1/3)

all_data <- merge(x = all_data, y = status_data, by = "Timestamp", all.x = TRUE)
all_data[1, "Status"] = 0
rows <- nrow(all_data)
for (i in 1:rows) {
  if (is.na(all_data[i, "Status"] )) {
    all_data[i, "Status"] = all_data[i-1, "Status"]
  }
}

write.csv(all_data, "Desktop/test1/dl_result1.csv")
rm(data)
rm(comp_data)
rm(data2)
rm(all_data)
rm(status_data)

summary <- read.csv("Desktop/summary.csv")
hist(summary$Setup.Time1..s., breaks = 28)
hist(summary$Setup.Time2..s., breaks = 16, col="gray", xlab="RRC Connection Setup Time (s)",xlim=c(0.14,0.24),ylim=c(0,30), main="RRC Connection Latency")
rm(summary)

all_data <- read.csv("Desktop/total.csv")
release <- data.frame(Timestamp=character(),
                 total_dl=numeric(), 
                 interval=integer()) 

t = 10
rows <- nrow(all_data)-1
for (i in 1:rows){
  if ((all_data[i, "Status"] == 1) & (all_data[i+1, "Status"] == 0)) {
    record = TRUE
    temp = 0
    for (j in 1:t) {
      if (all_data[i+1-j, "Status"] == 0) {
        record = FALSE
        break
      }
      temp = temp + all_data[i+1-j, "dl.bytes"]
    }
    if (record) {
      release$Timestamp = as.character(release$Timestamp)
      release[nrow(release) + 1,] = list(Timestamp=toString(all_data[i, "Timestamp"]),total_dl=temp, interval = t)
      release$Timestamp = as.factor(release$Timestamp)
    }
  }
}

rm(release)

release2 <- data.frame(Timestamp=character(),
                      last=numeric(), 
                      limit=integer()) 

l = 350
rows <- nrow(all_data)-1
for (i in 1:rows){
  if ((all_data[i, "Status"] == 1) & (all_data[i+1, "Status"] == 0)) {
    record = TRUE
    j = 1
    while(all_data[i+1-j, "dl.bytes"] < l) {
      if (all_data[i+1-j, "Status"] == 0) {
        record = FALSE
        break
      }
      j = j + 1
    }
    if (record) {
      release2$Timestamp = as.character(release2$Timestamp)
      release2[nrow(release2) + 1,] = list(Timestamp=toString(all_data[i, "Timestamp"]),last=j, limit = l)
      release2$Timestamp = as.factor(release2$Timestamp)
    }
  }
}
hist(release2$last, breaks = 20, col="gray", xlab="Time (s)", main="Inactive Time before Releasing
     - Boundary: 350 Bytes")


rm(release)
rm(release2)

release3 <- data.frame(Timestamp=character(),
                       total=numeric(), 
                       time=integer()) 
rows <- nrow(all_data)-1
for (i in 1:rows){
  if ((all_data[i, "Status"] == 1) & (all_data[i+1, "Status"] == 0)) {
    record = TRUE
    j = 1
    sum = 0
    while(all_data[i+1-j, "Status"] != 0) {
      sum = sum + all_data[i+1-j, "dl.bytes"]
      j = j + 1
    }
    if (record) {
      release3$Timestamp = as.character(release3$Timestamp)
      release3[nrow(release3) + 1,] = list(Timestamp=toString(all_data[i, "Timestamp"]),total=sum, time = j)
      release3$Timestamp = as.factor(release3$Timestamp)
    }
  }
}


trigger <- data.frame(Timestamp=character(),
                       total=numeric(), 
                       time=integer()) 
rows <- nrow(all_data)-1
t = 10
for (i in 1:rows){
  if ((all_data[i, "Status"] == 0) & (all_data[i+1, "Status"] == 1)) {
    record = TRUE
    sum = 0
    for(j in 1:t) {
      if (i+j < rows){ 
        sum = sum + all_data[i+j, "dl.bytes"]
      }
    }
    if (record) {
      trigger$Timestamp = as.character(trigger$Timestamp)
      trigger[nrow(trigger) + 1,] = list(Timestamp=toString(all_data[i, "Timestamp"]),total=sum, time = t)
      trigger$Timestamp = as.factor(trigger$Timestamp)
    }
  }
}
hist(release2$last)
hist(release2$last, breaks = 20, col="gray", xlab="RRC Connection Setup Time (s)",xlim=c(0,25), main="Histogram of RRC Connection Latency")



rm(all_data)
