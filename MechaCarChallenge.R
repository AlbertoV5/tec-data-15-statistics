## [[file:challenge.org::rscript][rscript]]
library(dplyr)
library(ggplot2)
library(tidyverse)
mpgcar <-
  read.csv(
    'MechaCar_mpg.csv',
    check.names = F,
    stringsAsFactors = F
)
head(mpgcar)
lm(
  mpg ~ vehicle_length +
  vehicle_weight +
  spoiler_angle +
  ground_clearance +
  AWD,
  data = mpgcar
)
summary(
  lm(
    mpg ~ vehicle_length +
    vehicle_weight +
    spoiler_angle +
    ground_clearance +
    AWD,
    data = mpgcar
  )
)
coildata <-
   read.csv(
    'Suspension_Coil.csv',
    check.names = F,
    stringsAsFactors = F
)
head(coildata)
total_summary <-
  coildata %>%
  summarize(
    Mean=mean(PSI),
    Median=median(PSI),
    Variance=var(PSI),
    SD=sd(PSI)
)
lot_summary <-
  coildata %>%
  group_by(Manufacturing_Lot) %>%
  summarize(
    Mean=mean(PSI),
    Median=median(PSI),
    Variance=var(PSI),
    SD=sd(PSI),
    .groups='keep'
  )
t.test(
  coildata$PSI,
  mu=mean(coildata$PSI)
)
t.test(
  subset(
    coildata$PSI,
    coildata$Manufacturing_Lot == "Lot1"
  ),
  mu=mean(coildata$PSI)
)
t.test(
  subset(
    coildata$PSI,
    coildata$Manufacturing_Lot == "Lot2"
  ),
  mu=mean(coildata$PSI)
)
t.test(
  subset(
    coildata$PSI,
    coildata$Manufacturing_Lot == "Lot3"
  ),
  mu=mean(coildata$PSI)
)
## rscript ends here
