# Age Distribution of Cases and Trends
## Naive Time Complexity
The question has parameters PHU id, begin and end. Checking if an entry matches our PHU is $O(n)$, checking if an entry is within the dates of intrest is $O(n)$. Since our data is large (65.4MiB), this is ripe for big O notations. $O(n) + O(n) = O(n)$. We can't do better than $O(n)$.

## Naive Time Complexity is Our Best Time Complexity*
Can we do better than $O(n)$? Not if we want to mostly perserve the original structure. We cannot remove any entries that isn't in PHU of our interest since the PHU of interest is not known until run time. We cannot remove any entries based on dates either since that is also not known until runtime. 

## How to do better than O(n)
We can do it in O(m) (where m is the number of cases within a PHU, m < n) by pre-processing. We could calculate the age distribution of all PHU regions from dates begin to end, sort them by dates within a PHU region, store each PHU in different sections of a file and offer a jump table. However, this would effectively means we complete all the work during the pre-processing stage and the final program is nothing but a fancy grapher. 

# Lag between Test Report Time and Specimen Collection Time
## The Number of Parameters is Variadic
This question offers the user to enter 2..k (where k is the total number of PHU) parameters for PHU regions. Meaning our naive time complexity is $O(mn)$. 

## Can we do Better?
If we group all cases with the same PHU together and sort them by dates within it. We can do it in $O(mk)$ (where m is the number of PHU of our interest, and k is the average number of cases within one PHU). Assume n is large, $(mk)$ will be much smaller. But this is similar to the question above where effectively all the heady work is done during pre-processing and the final program is just a fancy grapher. 

# Re question prototype
[link](https://imgur.com/bnBpmca)