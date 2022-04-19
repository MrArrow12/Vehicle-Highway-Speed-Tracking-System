# Vehicle-Highway-Speed-Tracking-System
Detects vehicle speeding on a highway using OpenCV written in Python.

In this project, the main objective is to calculate the speed of cars on the road and display them as the output. The system will display the last known speed of the vehicle in an area along with the maximum speed limit of the area. The point of this system is to help the user gauge the speed of vehicles for multiple purposes such as ensuring the safety of the area, vehicle passing by and many more. Each vehicle has a unique ID in order to track them and calculate their speed. Theres two lanes which will track the vehicle speed when entering the lane and the tracker will stop tracking the speed when the vehicle leaves the end of the lane.

![SpeedImage](https://user-images.githubusercontent.com/98644709/151963032-872ddc11-d072-4401-8216-f4f85a762cbb.PNG)
![image](https://user-images.githubusercontent.com/98644709/164021915-30262ca0-a83f-4134-9943-6726f28d7a96.png)
![image](https://user-images.githubusercontent.com/98644709/164022064-072a695c-677a-4ed3-ae09-ded8f172306d.png)

So for estimateSpeed function we need to calculate the speed distance between two lanes and a vehicle that drives between it. We pass our carID as our parameter. In order to track the vehicle ID.
Basically we use the speed distance formula which is 

![image](https://user-images.githubusercontent.com/98644709/164022132-61ce45e6-ba9e-4d6b-99ea-7cbb8ee50467.png)

We also need to factor our frame rate per second because that will also affect the speed of the car depending on our video FPS. We multiply by the constant 1. And we round off by 2 decimal places. So basically the formula will be like this:

![image](https://user-images.githubusercontent.com/98644709/164022214-fd0f699a-ac73-431d-822e-755cb00bee7e.png)

So basically inside this function, we calculate the time difference between the end point and the starting point. When a vehicle enters the starting lane the time will be tracked and once the vehicle went past the ending lane. It will stop tracking and the time will stop. And then we calculate the time difference between the final time and the initial time. The program will then return the value of the speed.

![image](https://user-images.githubusercontent.com/98644709/164022258-40bf9a7b-49a9-4462-a725-4236a919d4da.png)


HOW TO INSTALL DLIB LIBRARY:

WATCH THIS VIDEO TO INSTALL:
https://www.youtube.com/watch?v=pHrgi8QLcKk&ab_channel=ImportPyeidetic
