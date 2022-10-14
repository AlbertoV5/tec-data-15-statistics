- [Statistical Analysis with R](#orgabd6043)
  - [Linear Regression to Predict MPG](#org8a2aa8d)
  - [Summary Statistics on Suspension Coils](#org30cc2e9)
  - [T-Tests on Suspension Coils](#orgda37555)
  - [Study Design: MechaCar vs Competition](#orgf08e999)



<a id="orgabd6043"></a>

# Statistical Analysis with R


<a id="org8a2aa8d"></a>

## Linear Regression to Predict MPG

The first linear regression gives us the following results.

![img](./resources/_r_1.png)

When we call the summary we get our **p-value** and **multiple r-square**.

![img](./resources/_r_1b.png)

1.  The coefficients that provide a non-random amount of variance are: vehicle\_length and ground\_clearance (as well as the Intercept) because their **Pr(>|t|)** value is very small.
2.  The slope is not considered zero because the **r-squared** value is 0.7149, which means the relationship is linear. If we were to plot a line, it would be almost completely perpendicular to both axis.
3.  This model is effective on showing us which variables have the most impact (greater correlation) on the **Milles per Gallon** and which do not affect it as much, so now we can make decisions based on those predictions.


<a id="org30cc2e9"></a>

## Summary Statistics on Suspension Coils

These are both summaries on the suspension coils.

![img](./resources/_r_2.png)

We can see that the total variance on the suspension coils is under 100 pounds per square inch, as per the design specifications. However, when we look at the lots **individually**, we can see that there is a problem with `Lot3`.

![img](./resources/_r_2b.png)

`Lot3` doesn&rsquo;t comply with the variance specification, as it&rsquo;s value is `170`, much higher than the required 100.


<a id="orgda37555"></a>

## T-Tests on Suspension Coils

The following tests are made to assert that the mean of each sample is apoximates the population mean. We can verify the measure in our summary table that we have already calculated.

If we compare the mean of the population against itself, we will get a **p-value** of `1` because the ratio is perfect.

![img](./resources/_r_3a.png)

However, when doing **one-sample-t-test** for each of the lots, we get a more revealing picture.

Lot1 T-Test

![img](./resources/_r_3b.png)

Lot2 T-Test

![img](./resources/_r_3c.png)

Lot3 T-Test

![img](./resources/_r_3d.png)

We can see that the **p-value** on `Lot1` and `Lot2` are within the confidence interval, but the value for `Lot3` which is equal to `0.1589` is not, which means this sample deviates from the mean of the population more than we would like it to be.

If our alternative hypothesis is the following:

> If we measure the mean of the Lot3, it should not deviate from the mean of the population considerably.

Then we can&rsquo;t validate it, so the null hypothesis would still stand.

> The mean of the Lot3 will deviate from the population mean considerably when measured.


<a id="orgf08e999"></a>

## Study Design: MechaCar vs Competition

We want to test the MechaCar product at a larger scale so we should develop a set of tests to help us obtain insight and make predictions about the performance of the product in the market. This means that we have to compare against competitors and include on the consumer as a source for measurements.

We can start with a test to measure safety rating, which would consist of a controlled environment to perform tests on both the MechaCar and its competitors. The null hypothesis will be the following:

> Given a set of terrains and crash scenarios, the MechaCar won&rsquo;t protect the passengers of the vehicle better than its competitors.

And the alternative hypothesis will be the following:

> If we measure damages to test to dummy mannequins and interior of the MechaCar in different crash situations, it will perform better than its competitors in the majority of the tests.

The measurements we can perform are speed of the vehicles, which will be continuous data, then ordinal data can be severity of the damage in mannequins and interior of the car. We can also measure the PSI on the tires as numerical data.

Given that the number of tests can be scarce, we can do a multiple linear regression on the severity of the interior damage v.s. all the other variables.

For example, given a few numerical variables and a few ordinal variables, we can find a relationship of how much each numerical data affects it. Then we can compare the MechaCar data to other vehicles and look for differences on variance and how consistent each sample is against the population.

```R
library(tidyverse)
```

```R
# mock data
data <- tibble(severity = 1:5, psi = 31:35, speed = 60 + 20*log(severity))
```

<div class="org" id="org4755e05">
<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">severity</th>
<th scope="col" class="org-right">psi</th>
<th scope="col" class="org-right">speed</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">31</td>
<td class="org-right">60</td>
</tr>


<tr>
<td class="org-right">2</td>
<td class="org-right">32</td>
<td class="org-right">73.8629436111989</td>
</tr>


<tr>
<td class="org-right">3</td>
<td class="org-right">33</td>
<td class="org-right">81.9722457733622</td>
</tr>


<tr>
<td class="org-right">4</td>
<td class="org-right">34</td>
<td class="org-right">87.7258872223978</td>
</tr>


<tr>
<td class="org-right">5</td>
<td class="org-right">35</td>
<td class="org-right">92.188758248682</td>
</tr>
</tbody>
</table>

</div>

The previous data is just a mock to demonstrate how we could perform the tests with R and then use linear regression to find correlation and variance.

```R
summary(lm(severity ~ psi + speed, data=data))
```

    
    Call:
    lm(formula = severity ~ psi + speed, data = data)
    
    Residuals:
             1          2          3          4          5
    -2.408e-16  8.565e-16 -6.017e-16 -4.030e-16  3.890e-16
    
    Coefficients:
                  Estimate Std. Error    t value Pr(>|t|)
    (Intercept) -3.000e+01  2.777e-14 -1.080e+15   <2e-16 ***
    psi          1.000e+00  1.180e-15  8.473e+14   <2e-16 ***
    speed        5.456e-16  1.468e-16  3.716e+00   0.0654 .
    ---
    Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    
    Residual standard error: 8.566e-16 on 2 degrees of freedom
    Multiple R-squared:      1,	Adjusted R-squared:      1
    F-statistic: 6.815e+30 on 2 and 2 DF,  p-value: < 2.2e-16
    
    Warning message:
    In summary.lm(lm(severity ~ psi + speed, data = data)) :
      essentially perfect fit: summary may be unreliable

The test will gain relevance if we measure more variables of the environment and the state of the cars as well as including the competition.

The null hypothesis will be negated if the MechaCar performs better and there is less interior damage than its competitors in a majority of the scenarios.
