# CS690-MiniProj1
Authored by Pukar: 
Three Folders AM, PM and low_traffic_flow
Each have their own config files which will contain the detector, route and net files as input, and output a tripinfo.xml file that the script will parse to get us the data. 

Need to run each script in each folder 6 times under different conditions. Change sumo phase timing to 70, 90 and 110. These are three runs, and then again 70, 90, 110 but this time turn on Actuated signals in the traffic light using the traci command. 

NOTE: on each run output it into a different CSV file otherwise data will be overwritten. Name each CSV file accordingly and at the end group the data into a main CSV file, there should be 72 data points by the end. 

Then, analytics and paper writing will be done. We will be submitting the entire lyons file, with data and CSV will be submitted separately along with the overleaf paper on latex.

