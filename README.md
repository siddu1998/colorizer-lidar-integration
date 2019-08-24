# Traffic sign LiDAR insight generation tool

![Image of Yaktocat](https://github.com/siddu1998/colorizer-lidar-integration/blob/master/gt.png)

Author  :  Sai Siddartha Maram

Lab     :  Research Assistant Transportation Lab, GeorgiaTech

Professor and Supervisor : Dr. Yi-Chang (James) Tsai

contact : smaram7@gatech.edu
## Summary
The insight tool provides an opportunity to analyse and study the behaviour of retro-intensity captured form LiDAR on traffic signs. Prominent features of the tool as for the latest push include 
1. Statistical analysis and sign replacement strategies
2. 3D visualiation of the LiDAR signs based on retro
3. Identifying areas of damage on the sign
4. Relation between color and its effect on retro intensity
5. Study specific areas of the sign using Lasso selection technique
6. Behaviour of sign and its relation with retro intensity with age and persistent energy absorbtion


## Metric 

From various statistic distributions the tool uses median to give recommendations, this is because of spurious points on the boundary will disturb the mean. 


## Tool Description

The tool loads the data (user selected sign id) from the lidar inventory and populates histogram and the corresponding 3D heights based on the retro values


![Image of Yaktocat](https://github.com/siddu1998/colorizer-lidar-integration/blob/master/images/first_page.PNG)


The tool allows us to get insight on the spurious points and also generate insight into different points based on retro values

![Image of Yaktocat](https://github.com/siddu1998/colorizer-lidar-integration/blob/master/images/user_click.PNG)

The lasso analysis allows user to draw ovIndia1983er certain points they are interested to study, this allows us to study the behaviour and trends of retrointensity based on age, color and region

![Image of Yaktocat](https://github.com/siddu1998/colorizer-lidar-integration/blob/master/images/draw.PNG)

Analysis of the choosen points are based on the weight they carry in the net histogram
![Image of Yaktocat](https://github.com/siddu1998/colorizer-lidar-integration/blob/master/images/finsih.PNG)
--



### Instructions on how to use the tool
Place your data in the Data folder. Data consists of an .csv sheet named signs.csv. The GUI tool uses pX,pY,Retro,Color values for each sign_id. Make sure you fill these coloumns correctly as per the data you have collected.

In the code section, you will find the UI_with_lasso.py, this is the core algorithm and has the GUI code within. Install the dependencies required and run the 
                ```python UI_with_lasso.py```
