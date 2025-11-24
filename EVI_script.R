library(ggspatial)
library(raster)
library(sf)
library(sp)


setwd('C:/francis/jigme/Mataranka/Red_Lily/EVI')
dir()
eviFiles <- list.files(pattern = "\\.tif$") 
eviFiles

evi_stack <- stack(eviFiles)


years <- seq(2015, 2024)  
names(evi_stack) <- years 

names(evi_stack) <- paste("evi", years)


par(mfrow = c(3, 4),mar=c(0.1, 0.1, 0.1, 0.1) ,mai = c(.1, 0.2, 0.2, 0.2)) 
color_palette <- colorRampPalette(c("brown","yellow", "darkgreen"))(5)

#plots
for (i in 1:nlayers(evi_stack)) {
  plot(evi_stack[[i]], 
       col = color_palette,  # Apply blue gradient color palette
       main = names(evi_stack)[i],
       axes = FALSE)  # Set the main title
}

#plot plot
for (i in 1:nlayers(evi_stack)) {
  hist(evi_stack[[i]], 
       col = "grey",  # Apply blue gradient color palette
       main = names(evi_stack)[i])  # Set the main title
}

