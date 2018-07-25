Illustrative simulation of the stochastic effects of racial bias over time in place-based predictive policing.

The setup is as follows: 144 citizens—half labeled as “white” and half as “black”—are randomly laid out in a 12x12 grid (“city”). Each citizen remains in the same location for an entire game, which consists of 200 rounds. Each citizen has an identical 1/3 probability of being a criminal, and there is necessarily an identical number of criminals per race. Each criminal citizen commits a crime each round. Each city has a segregation score, which is calculated as the difference between the number of black citizens in the highest-number-black quadrant and the number of black citizens in the lowest-number-black quadrant.

There are 36 police officers. The police department divides the city into four quadrants of equal size, and initially assigns an equal number of police officers to each quadrant. Within a quadrant, in each round, each police officer assigned to that quadrant randomly picks a cell (with no duplications) and attempts to detect whether the citizen in that cell has committed a crime. If the citizen has not committed a crime, the officer never thinks they have (there are no false positives—an extremely charitable assumption). If the citizen has committed a crime, the officer detects it with a probability of .5 + F, where F is the *racial distrust factor*, a number that is always 0 if the citizen is white, and ranges from 0 to .4 if the citizen is black. F can be seen to represent the most charitable possible interpretation of the underlying level of racial bias in the community, understanding that level of bias as distrust that *merely increases the true positive rate* for subordinated racial groups. (Of course, in real racist societies, it also increases the false positive rate, so I’m really putting a thumb on the scale for the police here.) The police have no memory of which citizens committed crimes, they just remember in which quadrant the crimes were committed.

Each round after the first, the police naively produce a “heat map” by simply estimating the relative risk of crime in a given quadrant as the proportion of total police-discovered crimes in that quadrant in all previous rounds of the game. They then allocate a minimum of 3 officers to each quadrant, and a proportion of their remaining officers to each quadrant equal to the crime risk of that quadrant, rounded down (with any remaining officers after rounding allocated to the highest-risk quadrant). 

The simulation generates 1000 discrete “cities,” and each city is then simulated 5 times at each level of F, for a total of 50,000 simulation runs of 200 rounds each. The final “racial disparity score” (RDS) of each simulation run is the ratio of detected crimes by black citizens to detected crimes by white citizens.

Obviously, the expected value for the RDS of any simulation run with nonzero F should be above 1, however, the racial distrust feedback loop that this simulation expresses generates two further hypotheses: 

1.  RDS should increase disproportionately over time with F—-that is, the RDS of a 100 round simulation run with nonzero F should be higher than the one-round, non-segmented (into quadrants) expected value for that F. 

2.  RDS should increase with segregation scores for values of F above 0.

The expected one-round, non-segmented RDS values for each level of F (which represent the organic level of racial disparity given the level of racial bias in the community, where police departments don’t carve up the city into grids and attempt to predict criminality from past detection) are as follows: 

F = 0, expected RDS = 1, because the police have the same probability of detecting a crime from either race.
F = .1, expected RDS = 1.2, calculated as follows: 

There are 48 criminals per round. The police officer/citizen selection process is equivalent to a selection without replacement of 36 citizens from 144, so expected number of criminals who will be investigated is equal to the expected value of the hypergeometric distribution, in this case (36 * 44)/ 144, or 11. Of those, on average, 5.5 will be black and 5.5 will be white, but the police will detect 2.75 white criminals and 3.3 black criminals on average, thanks to F, leading to a predicted RDS of 1.2.

F = .2, expected RDS = 1.4, by the same method
F = .3, expected RDS = 1.6
F = .4, expected RDS = 1.8.

As expected, segregation does increase the disparate effect of policing bias in this simulation, and the self-reinforcing nature of these biases entails that the impact of increases in bias level cause a greater increase in inequality than would be expected in the absence of a feedback loop, although under the specifications of the model these effects are slight. 

Realistically, of course, we have reason to believe that the racial distrust factor is also endogenous to observed crime rates—police officers are likely to have any latent racial bias they hold reinforced by observing a disproportionate amount of crime by subordinated racial groups, even if the actual amount of crime across racial groups is equal. So, in a realistic system, we would expect this distrust factor to increase through a game, making the racially disparate effects thus demonstrated even worse. 
