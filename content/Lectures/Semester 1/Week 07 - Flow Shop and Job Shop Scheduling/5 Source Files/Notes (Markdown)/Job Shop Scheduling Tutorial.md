<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML-full"></script> <script type="text/x-mathjax-config"> MathJax.Hub.Config({"HTML-CSS": { preferredFont: "TeX", availableFonts:["STIX","TeX"], linebreaks: { automatic:true }, EqnChunk:(MathJax.Hub.Browser.isMobile ? 10 : 50) }, tex2jax: { inlineMath: [ ["$", "$"], ["\\\\(","\\\\)"] ], displayMath: [ ["$$","$$"], ["\\[", "\\]"] ], processEscapes: true, ignoreClass: "tex2jax_ignore|dno", processEnvironments: true }, TeX: { noUndefined: { attributes: { mathcolor: "red", mathbackground: "#FFEEEE", mathsize: "90%" } }, Macros: { href: "{}" } }, messageStyle: "none" });   </script>

# Job Shop Scheduling Tutorial

You should do this tutorial using Google Collabatory and using [Google OR-Tools](https://developers.google.com/optimization/cp).

Note you will need to run the following first to install the ortools python package.

```python
!pip install ortools
```

## Exercises

Solve the following problems by adapting either the Google OR Tools or the LP code.

Sketch out your solution and check that it is indeed feasible and try appears to be optimal. Remember you cannot check optimality (if done correctly it will be optimal), but you can at least eyeball the solution for reasonableness. 

**1. Job Shop Scheduling Problem:**

|Jobs|Operations|Sequence on Machines|Process Time on Machines|
|--|--|--|--|
|$J_0$| $O_{01}$, $O_{02}$, $O_{03}$ | $M_0$, $M_1$, $M_2$ | $3$,$2$,$2$ |
|$J_1$| $O_{11}$, $O_{12}$, $O_{13}$ | $M_0$, $M_2$, $M_1$ | $4$,$3$,$1$ |
|$J_2$| $O_{21}$, $O_{22}$, $O_{23}$ | $M_1$, $M_3$, $M_2$ | $2$,$3$,$2$ |

**2. Job Shop Scheduling Problem:**

|Jobs|Operations|Sequence on Machines|Process Time on Machines|
|--|--|--|--|
|$J_1$| $O_{11}$, $O_{12}$, $O_{13}$, $O_{14}$ | $A$, $B$, $C$, $D$ | $3$,$2$,$4$,$3$ |
|$J_2$| $O_{21}$, $O_{22}$, $O_{23}$ | $B$, $A$, $D$ | $5$,$3$,$2$ |
|$J_3$| $O_{31}$, $O_{32}$, $O_{33}$, $O_{34}$ | $C$, $D$, $A$, $B$ | $2$,$1$,$4$,$4$ |
|$J_4$| $O_{41}$, $O_{42}$, $O_{43}$ | $D$, $C$, $B$ | $4$,$3$,$5$ |

**3. Job Shop Scheduling Problem:**

|Jobs|Operations|Sequence on Machines|Process Time on Machines|
|--|--|--|--|
|$J_A$| $O_{A1}$, $O_{A2}$, $O_{A3}$, $O_{A4}$, $O_{A5}$ | $M_1$, $M_2$, $M_3$, $M_4$, $M_5$ | $4$,$2$,$3$,$5$,$2$ |
|$J_B$| $O_{B1}$, $O_{B2}$, $O_{B3}$, $O_{B4}$ | $M_3$, $M_4$, $M_2$, $M_5$ | $2$,$1$,$3$,$4$ |
|$J_C$| $O_{C1}$, $O_{C2}$, $O_{C3}$, $O_{C4}$ | $M_1$, $M_2$, $M_3$, $M_4$ | $3$,$4$,$2$,$3$ |

**4. N-queens Problem:**

Read through the **N-queens problem** on the [Google OR-Tools site](https://developers.google.com/optimization/cp/queens).

Implement the solution in Google Collabatory and make sure you understand what the model is doing and how it translates to the Python code.

**5. Employee Scheduling Problem:**

Read through the **Employee Scheduling Problem** on the [Google OR-Tools site](https://developers.google.com/optimization/scheduling/employee_scheduling). 

Implement the solution in Google Collabatory and make sure you understand what the model is doing and how it translates to the Python code.
