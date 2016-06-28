# This script scatter-plots solar radiation data over time
# Authored by Sean Hendryx

library(ggplot2)

# SET WORKING DIRECTORY
#setwd("/your/path/here")

df<- read.csv("Solar_Radiation_Wunderground_Data.csv", header=TRUE, sep = ",")

#TIMESTAMP DATA
df$timeStamped <- strptime(df$timeStamp, "%Y%m%d%H%M", tz="MST")

p <- ggplot(df, aes(x = timeStamped, y = solarRadiation)) + geom_point(colour = "coral", alpha=.25) + theme_bw() + labs(x = "Date", y = expression("Solar Radiation (W"*m^"-2"*")")) + ggtitle("Solar Radiation Near Mt. Bigelow, AZ (Station MQSLA3)")
p