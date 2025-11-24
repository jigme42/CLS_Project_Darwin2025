library(ggspatial)
library(raster)
library(sf)
library(sp)


setwd('C:/francis/jigme/Mataranka/Red_Lily/Water')
dir()
mndwiFiles <- list.files(pattern = "\\.tif$") 


mndwi_stack <- stack(mndwiFiles)


#years <- seq(2015, 2024)  
#names(mndwi_stack) <- years 


years <-  c("2015", "2016", "2017", "2018","2020","2021", "2022", "2023","2024")

names(mndwi_stack) <- paste("water", years)


par(mfrow = c(3, 3),mar=c(0.1, 0.1, 0.1, 0.1) ,mai = c(.1, 0.2, 0.2, 0.2)) 
color_palette <- colorRampPalette(c("white","lightblue", "darkblue"))(3)

#plots
for (i in 1:nlayers(mndwi_stack)) {
  plot(mndwi_stack[[i]], 
       col = "blue",  # Apply blue gradient color palette,
       legend = FALSE,
       main = names(mndwi_stack)[i],
       axes = FALSE)  # Set the main title
}


