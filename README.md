# Spatial-Statistics
***
###The repository contains methods of spatial-statistics, so far especially Kernel Density Estimation(KDE) methods.
***
More specifically, four bandwidth selection methods of KDE are included:  
* two fixed KDE bandwidth selection methods : ***rule of thumb*** & ***corss-validation based fixed KDE***  
* two adaptive KDE bandwidth selection methods: ***cross-validation based adaptive KDE*** & ***QFA-KDE***  
***
Further more, two kinds of datasets are included for experiments:  
* POI dataset: regional clustered data/Hubei enterprise registration data POI (Li et al.,2018)  
* GPS trajectory dataset: linear clustered data
***
### **for introduction and more details** of the KDE bandwodth calculation methods  
Please refer to the upcoming paper of Yuan on the journal of "International Journal of Geographical Information Science" (IJGIS)  
***
A demonstration of the spatial segmentation result computed by QFA-KDE:  
![spatial segmentation result](https://github.com/FaLi-KunxiaojiaYuan/Spatial-Statistics/raw/master/Figures/Figure_7.png) 
***
The comparison results of the estimated density distribution of GPS points using four different KDE bandwidth selection methods:  
![ comparison results using four different KDE bandwidth selection methods](https://github.com/FaLi-KunxiaojiaYuan/Spatial-Statistics/raw/master/Figures/Figure_6.png)  
***note:*** the bandwidths are calculated using the contained python scripts, and the heat-maps are generated using QGIS software  
***References:***
Li, F., Gui, Z., Wu, H., Gong, J., Wang, Y., Tian, S., & Zhang, J. (2018). Big enterprise registration data imputation: Supporting spatiotemporal analysis of industries in China. Computers, Environment and Urban Systems, 70, 9-23.
