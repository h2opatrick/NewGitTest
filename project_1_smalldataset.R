######start###############
getwd()
setwd('C:/Users/cch2owater/Desktop/KALO/P1')

mydat <- read.csv('SELECT___FROM_rakuten_app_brand.csv',header = F)
names(mydat)
mydat <- data.frame(
                    Brand_ID = mydat[,1],
                    Brand_Name = mydat[,2],
                    Stem = mydat[,3],
                    is_stand_alone = mydat[,4],
                    Parent_ID = mydat[,5],
                    Parent_ID2 = mydat[,6]
                    
                    )
class(mydat)
head(mydat,n = 5)
tail(mydat,n = 5)
names(mydat)
str(mydat)

mydat$Brand_Name<- as.character(mydat$Brand_Name)
mydat$Stem <- as.character(mydat$Stem)



parent <- mydat$is_stand_alone == TRUE & is.na(mydat$Parent_ID2)


###Version 1: complicated version: has three situations#####
subbrand <- (mydat$is_stand_alone == FALSE & is.null(mydat$Parent_ID) == F)
  | (mydat$is_stand_alone == TRUE & is.na(mydat$Parent_ID2) == FALSE) 
  | (mydat$is_stand_alone == TRUE & is.null(mydat$Parent_ID) == F)

###version 2: only care about it has a parent ID#####
subbrand <- is.na(mydat$Parent_ID) == F



dat_length <- nrow(mydat)#know how many rows are in database
####create a dataframe with only parent names 
branddf <- data.frame(stringsAsFactors = F,
  Brand_Index = mydat$Brand_ID[parent],
  
  Parent_Brand = mydat$Brand_Name[parent],
  
  stem = mydat$Stem[parent]
)

str(branddf)

branddf[,"Sub_Brand_Name"] <- paste(branddf$stem,',',sep = '')

names(branddf)
head(branddf, n = 10)

#[1] "Brand_ID"       "Brand_Name"     "Stem"           "is_stand_alone" "Parent_ID"      "Parent_ID2"  
#if one brand is not parent brand, then need to find its parent brand by brand index
#extract its name and put into the sub brand list of that parent brand. 

sub_brand_df <- mydat[subbrand,c(1,2,3,5,6)]
str(sub_brand_df)
head(sub_brand_df, n = 15)
#column Brand_ID        Brand_Name Parent_ID Parent_ID2

for (i in 1:nrow(sub_brand_df)) {
  row <- sub_brand_df[i,]
  
  parentID <- as.integer(row[4])
  
  parentID2 <- row[5]
  #select this row information from branddf, add the name and stem from the row in sub_brand_df to the sub_brand_name 
  #in branddf.
  branddf[branddf$Brand_Index == parentID,4] <- paste(branddf[branddf$Brand_Index == parentID,4],
                                                      row[2],
                                                      row[3],
                                                      sep = ',')
  #if there is second parent ID, all add this row to the other parent sub brand group 
  if (is.na(parentID2) == F) {
    
    parentID2 <- as.integer(parentID2)
    
    branddf[branddf$Brand_Index == parentID2,4] <- paste(branddf[branddf$Brand_Index == parentID,4],
                                                         row[2],
                                                         row[3],
                                                         sep = ',')
                                                        
  }
}
#branddf[branddf$Brand_Index == parentID,3] good way to select something in particular in a data frame

###checking for error####
head(branddf,n =5)
branddf[branddf$Brand_Index == 2211,]

######output data frame to csv#####
write.csv(branddf,'outputfile.csv')




