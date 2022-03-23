# Information Retrieval

In this project Information Retrieval techniques were applied on speeches of the Greek Parliament for the University Course “Information Retrieval”. The dataset that was used contains 1.280.918 speeches, is 2.3 GB and the speeches are from 1989 till 2020. The dataset can be found on this Github repository https://github.com/iMEdD-Lab/Greek_Parliament_Proceedings. 

The goal of this project was the organization and the process of the data to extract useful information out of those speeches. 

More specifically this project focused on: 

a) Keywords extraction. Keywords can be found for each speech, for each politician, and for each politician party and how those change every year. When top-15 keywords were searched (and how they change every year) from 378.000 speeches, keywords were found after 98 sec. Also, when top-15 keywords were searched from 23.569 speeches, they were found after 32 sec. 

b) Top-k politician’s pairs that have the highest similarity on their speeches can be found (TF-IDF method). The average execution time that is needed in order for top-k pairs to be found is 65 sec. 

c) Top-k concepts of all the speeches can be found (using Latest Semantic Analysis method). The average execution time of this process is 250 sec. A web-based applicaton was created so that the extraction of these information can be much more easily accesible and user friendly.
