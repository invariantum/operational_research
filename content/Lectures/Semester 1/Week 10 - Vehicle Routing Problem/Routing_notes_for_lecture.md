## Traveling Salesman Problem (TSP)
The Traveling Salesman Problem (TSP) is one of the most well-known routing problems. It involves finding the shortest possible tour that visits each city exactly once and returns to the original city. 

### Mathematical Formulation
Let:
- $n$ be the number of cities,
- $c_{ij}$ be the distance between cities $i$ and $j$,
- $x_{ij}$ be a binary decision variable indicating whether to travel directly from city $i$ to city $j$.

The objective is to minimise the total distance traveled:

$$
\text{Minimise} \quad \sum_{i=1}^{n}\sum_{j=1, j\neq i}^{n} c_{ij}x_{ij}
$$

Subject to:
1. Each city is left exactly once (one outgoing edge):

$$
\sum_{j=1, j\neq i}^{n} x_{ij} = 1, \quad \forall i \in \{1,2,...,n\}
$$

2. Each city is visited exactly once (one incoming edge):

$$
\sum_{i=1, i\neq j}^{n} x_{ij} = 1, \quad \forall j \in \{1,2,...,n\}
$$

3. No subtours:

$$
u_i - u_j + 1 \leq (n - 1)(1-x_{ij}), \quad \forall i \in \{2,3,...,n\}, j \in \{2,3,...,n\}, i \neq j
$$

Where $u_i$ is a continuous variable representing the position of city $i$ in the tour and $n$ is the number of cities.

We can write this compactly as follows.

$$
\begin{align*}
&\text{Minmise } \; &\sum_{i \in V}\sum_{j \in V:i \neq j } c_{ij}x_{ij} \\
&\text{Subject to: } \\
& \; & \sum_{j \in V:j\neq i} x_{ij} = 1, \quad &\forall i \in V \\
& \; & \sum_{i\in V:i\neq j} x_{ij} = 1, \quad & \forall j \in V \\
& \; & u_i - u_j + 1 \leq (n - 1)(1-x_{ij}), \quad & \forall i,j \in V \setminus \{1\}: i \neq j \\
& \; & x_{ij} \in \{0,1\}, \quad &  \forall i, j \in V : i \neq j\\
& \; & u_i \in \mathbb{R}, \quad &  \forall i \in V
\end{align*}
$$
Note that $V \setminus \{1\} = \{2,3,\dots n \}$. i.e. it is the set $V$ without element $1$.

### Explaining the MTZ Subtour Constraint

We could have started with this, but I think it is nice to see it working and then to dive deeper into why this works.

The idea behind this constraint is that we wish to store the order of the tour in a variable $u_i \in \mathbb{R}$ where $u_i$ represents the order in which city $i$ is visited.

A key point here is that $u_i$ does not represent position. What we are looking for is some increasing sequence $u_{r_1} < u_{r_2} < \dots < u_{r_n}$, where $r_j$ is the order in which the city is visited (position in the tour). e.g. $r_1=5, r_2=2$ states that the first city visited is $5$ and the second city visited is $2$.

We should consider what this means. If we have a city $i$ visited before city $j$, then we would expect to set $x_{ij}=1$. The above now requires that $u_j > u_i$, we can rewrite this as a constraint using $\geq$, namely $u_j \geq u_i + 1$. Basically, $u_j$ should be larger than $u_i$.

Thus,

$$
\begin{align*}
& \text{If } x_{ij}=1 \\
& \text{then } u_j \geq u_i + 1
\end{align*}
$$

We can represent this by using big $M$.

$$
u_j + M(1-x_{ij}) \geq u_i + 1
$$

Which can be rewritten as the form in the mathematical program. We will show shortly that we can set $M=n-1$.

$$
u_i - u_j + 1 \leq M(1-x_{ij})
$$

When $x_{ij}=0$ then this constraint becomes $u_i - u_j + 1 \leq M$ and for large enough $M$ this is always satisfied, i.e. the constraint is effectively inactive. For a value of $x_{ij}=1$ this constraint becomes $u_i - u_j + 1 \leq 0$, which is exactly $u_j \geq u_i + 1$. 

Now we must consider the subtlety of the above constraint. This shouldn't be active for $i=j$, e.g. $x_{ii}$, so we can exclude that from the set of $i$ and $j$ that we create this constraint for. However, we also need to exclude this for city $1$, or at least one city, we choose city $1$ as it makes sense (remember a tour visits all cities and returns to the start. Any of the cities on a tour could be the starting point).

So why do we need to exclude the first city. Let's first consider what happens if we don't exclude it.

We are free to choose a city to start with, we will refer to this as $r_1$. There must exist for $r_1$ a unique edge (one outgoing edge constraint) which joins it to the next city $r_2$, i.e. $x_{r_1r_2}=1$. Thus $u_{r_1} < u_{r_2}$ as the MTZ constraint becomes $u_{r_2} \geq u_{r_1} + 1$.  We then must have a unique edge which joins the next city $r_3$, thus $u_{r_2} < u_{r_3}$, this continues until we reach the $n$th city. We must have $r_1 \neq r_2 \neq \dots \neq r_n$ otherwise we would have had some sub tour in which some $r_j=r_k$. e.g. the tour $1,2,3,1$ has $r_1=r_4$.


IMAGE

Thus we have unique set of values for $r_i$ and the increasing sequence, 

$$
u_{r_1} < u_{r_2} < \dots < u_{r_n},
$$

which puts us in a bit of a predicament. For this to now be a tour we would need the following sequence.

$$
r_1, r_2, \dots, r_n, r_1
$$

That is we need to visit the starting city $r_1$ from our last city $r_n$. i.e. we need an edge $x_{r_nr_1}=1$.

This leads to the following two constraints needing to be satisfied simultaneously.

$$
\begin{align*}
    u_{r_n} \geq u_{r_1} + 1 \\
    u_{r_1} \geq u_{r_n} + 1 
\end{align*}
$$

This is impossible!

Thus we exclude city $1$, so that we end up with an increasing sequence,

$$
u_{r_2} < u_{r_3} \dots < u_{r_n},
$$

but we are no longer bound by the MTZ constraint for city $1$. Hence we are free to choose $x_{1r_2}=1$, that is city $1$ starts the tour and connects with city $2$. We are also free to choose $x_{r_n1}=1$, city $n$ connects to city $1$ to end the tour.

$$
1, r_2, \dots, r_n, 1
$$

Hence the full constraint is:

$$
u_i - u_j + 1 \leq M(1-x_{ij}), \quad  \forall i \in V \setminus \{1\}, j \in V \setminus \{1\}, i \neq j \\
$$

The last thing to explain is why $M=n-1$.

We need to simultaneously satisfy all the MTZ constraints for our values of $x_{ij}=1$, namely:

$$
\begin{align*}
    u_{r_2} - u_{r_3} + 1 \leq 0 \\
    u_{r_3} - u_{r_4} + 1 \leq 0 \\
    \vdots \\
    u_{r_{n-2}} - u_{r_{n-1}} + 1 \leq 0 \\
    u_{r_{n-1}} - u_{r_n} + 1 \leq 0
\end{align*}
$$

Adding all these constraints together we have $u_{r_2} - u_{r_n} + (n-2) \leq 0$. That is the difference between them must be at least $(n-2)$, i.e. $u_{r_n} - u_{r_2} \geq n-2$. 

Thus for the second city in the sequence $r_2$ and the last city in the sequence $r_n$ we have to satisfy both of the following constraints as $x_{r_2r_n}=0$ and $x_{r_nr_2}=0$ (i.e. there is no edge between them).

$$
\begin{align*}
u_{r_2} - u_{r_n} + 1 \leq M \\
u_{r_n} - u_{r_2} + 1 \leq M \\
\end{align*}
$$

The first constraint is satisfied as long as $M\geq0$ as $u_{r_2} < u_{r_n}$ because of their position in the sequence. i.e. $u_{r_2} - u_{r_n} < 0$.

For the second $u_{r_n} - u_{r_2} \geq n-2 \implies u_{r_n} - u_{r_2} + 1 \geq n-1 \leq M$. 

Thus $M \geq n-1$, that is pick any number $M$ as long as it is greater than or equal to $n-1$.

## Extending the TSP to Allow Multiple Tours

Let's say we wish there to be $k$ tours leaving city 1.

This is actually very easy. All we have to do is relax the incoming and outgoing edge constraint for city 1.

1. Each city is left exactly once. Now we exclude city 1:

$$
\sum_{j \in V:j \neq i} x_{ij} = 1, \quad \forall i \in \{2,...,n\}
$$

2. Each city is visited exactly once. Now we exclude city 1:

$$
\sum_{i \in V:i \neq j} x_{ij} = 1, \quad \forall j \in \{2,...,n\}
$$

3. The number of edges leaving the city 1 is equal the number of desired tours.

$$
\sum_{j \in V: j \neq 1} x_{1j} = m
$$

City 1 is now forced to have $m$ edges leaving and entering.


### Why Does This Work?

The MTZ constraint now has other options than connecting city 1 at the beginning and end of the sequence. In fact, it can create many sub-chains of cities that are still valid for the constraints.

IMAGE

It is then free to connect each of these chains of cities to city one to form a set of sub-tours.

## Vehicle Routing Problem (VRP)
The Vehicle Routing Problem (VRP) extends the TSP by introducing a fleet of vehicles with limited capacity to serve a set of customers with varying demands. The objective is to minimise the total distance traveled by the vehicles while satisfying all customer demands and respecting capacity constraints.

### Model 1
Let:
- $V$ be the set number of customers,
- $m$ be the number of vehicles,
- $q_i$ be the demand of customer $i$,
- $Q$ is the capacity of each vehicle
- $c_{ij}$ be the distance between customer $i$ and customer $j$,
- $x_{ij}$ be a binary decision variable indicating whether a vehicle travels from $i$ to $j$.
- Let $f_{ij}$ be the flow (amount carried by a vehicle) on the edge $i$ to $j$.

#### Minimise Total Distance
Objective:

$$
\text{Minimise} \quad \sum_{i \in V} \sum_{j \in V:j \neq i} c_{ij}x_{ij}
$$

Subject to:

1. Each city is left exactly once (excluding city 1):
 
$$
\sum_{j \in V:j \neq i} x_{ij} = 1, \quad \forall i \in V \setminus \{1\}
$$

2. Each city is visited exactly once (excluding city 1):

$$
\sum_{i \in V:i \neq j} x_{ij} = 1, \quad \forall j \in V \setminus \{1\}
$$

3. Vehicles leaving depot

$$
\sum_{j \in V} x_{1j} \leq m 
$$

4. Flow conservation maintained

$$
\sum_{j \in V} f_{ji} - \sum_{j \in V} f_{ij} = d_i, \quad \forall i \in V \setminus \{1\}
$$

5. Route capacity less than $Q$

$$
0 \leq f_{ij} \leq Qx_{ij}
$$


$$
x_{ij} \in \{0,1\}
$$

$$
f_{ij} \in \mathbb{R}
$$


#### Some Key Points
* We require $m \geq \sum_{i \in V:i\neq 1} q_i$. i.e. we need enough vehicles to cover the demand.
* If we set $q_i = 1$ for all $i:i\neq1$ then we can use this each location is visited or put another way we could use it for a pickup model.
* If we let $q_i \in \mathbb{R}$ then we can have negative demands (supply) and positive demands (supply).
  * You should recognise this from the multi-commodity flow Problem (MCFP)

#### The Main Issue with this Model

* We are minimising the total distance, thus we will select a route to be as large as the capacity of a van. 
  * In the extreme case if the capacity is large enough we will select a single vehicle and get the TSP solution 

This is problematic as most logistics companies would probably want to deliver as quickly as possible!

### Model 2

We will extend our model to now attempt to solve the following objective.

* Deliver all orders as quickly as possible

We can reframe this objective as minimising the maximum route length of any vehicle. This is known as a minimax formulation.

To do this we will need to know the length of each of the routes for the vehicles, to do this we will introduce another dimension to the problem to represent each vehicle $k$.

A nice way to visualise this idea is to imagine we are creating a copy of the network for each vehicle, we can then track which edges are used in each of the networks.

IMAGE

Let:
- $V$ be the set of customers,
- $K$ be the set of vehicles,
- $q_i$ be the demand of customer $i$,
- $Q$ is the capacity of each vehicle
- $c_{ij}$ be the distance between customer $i$ and customer $j$,
- $x_{ijk}$ be a binary decision variable indicating whether vehicle $k$ travels from $i$ to $j$.
- Let $f_{ijk}$ be the flow (amount carried by vehicle) on the edge $i$ to $j$ for vehicle $k$.


$$
\begin{align*}
&\text{Minimise } \; &Q_{Max} \\
&\text{Subject to: } \\
& \; & \sum_{k \in K} \sum_{j \in V:j\neq i} x_{ijk} = 1, \quad &\forall i \in V \setminus \{1\} \quad & \text{A single vehicle enters a location}  \\
& \; & \sum_{k \in K} \sum_{i\in V:i\neq j} x_{ijk} = 1, \quad & \forall j \in V \setminus \{1\} & \quad \text{A single vehicle leaves a location} \\
& \; & \sum_{j \in V} x_{1j} \leq m \quad & & \text{No more than $m$ vehicles leave the depot} \\
& \; & \sum_{i\in V} \sum_{j\in V:i\neq j} f_{ijk} \leq Q_{Max}, \quad & \forall k \in K \quad & \text{Length of route for a vehicle is less than $Q_{max}$} \\
& \; & \sum_{k \in K} \sum_{j \in V} f_{jik} - \sum_{k \in K} \sum_{j \in V} f_{ijk} = d_i, \quad & \forall i \in V \setminus \{1\} \quad & \text{Enough demand is delivered to a location} \\
& \; & 0 \leq f_{ijk} \leq Qx_{ijk}, \quad & \forall i,j \in V, k \in K \quad & \text{Length of a route is less than vehicle capacity}\\
& \; & x_{ijk} \in \{0,1\}, \quad &  \forall i,j \in V : i \neq j\\
\end{align*}
$$


## NP-Hard Problems and Heuristic Solutions
Both TSP and VRP are NP-Hard problems, meaning that no known polynomial-time algorithm can solve them optimally. Therefore, heuristic methods are commonly employed to find near-optimal solutions in a reasonable amount of time. Some popular heuristics include:
- Nearest Neighbor
- Clarke-Wright Savings Algorithm
- Simulated Annealing
- Genetic Algorithms


## Conclusion
Routing problems are fundamental in operations research and have significant real-world applications. While optimal solutions may be elusive due to their NP-Hard nature, heuristic approaches such as simulated annealing offer practical means of finding near-optimal solutions. Understanding and effectively solving routing problems are crucial for efficient resource allocation and logistics management in various industries.
