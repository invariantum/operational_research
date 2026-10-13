# SimPy Practice Exercises
## Discrete Event Simulation with M/M/1, M/M/c, and Machine Breakdowns

**Instructions:** Use the code examples from the lecture segments to complete these exercises. Modify the provided code and experiment with different parameters. Try to answer the questions based on your simulation results.

---

## Question 1: Bank Teller Analysis (M/M/1 Queue)

### Scenario
A small bank branch has a single teller serving customers. The bank manager wants to understand customer wait times under different demand levels.

### Given Information
- Customers arrive following a Poisson process
- Service times are exponentially distributed
- Average service time: **3 minutes per customer**
- Simulation time: **8 hours** (480 minutes)

### Tasks

**a)** Implement an M/M/1 queue simulation for this bank using the code from Segment 1 (M/M/1 queue).

**b)** Run simulations with the following arrival rates and calculate the system utilization (ρ) for each:
   - **Scenario 1:** 15 customers per hour
   - **Scenario 2:** 18 customers per hour
   - **Scenario 3:** 20 customers per hour

**c)** For each scenario, collect and report:
   - Average wait time in queue
   - Average total time in system
   - Maximum wait time observed
   - Percentage of customers who had to wait

**d)** Create visualizations (histograms or line plots) showing the distribution of wait times for each scenario.

**e)** Compare your simulation results with the theoretical M/M/1 formulas:
   - Average wait time in queue: **W_q = ρ / (μ(1-ρ))**
   - Average time in system: **W = 1 / (μ - λ)**
   
   Where: λ = arrival rate, μ = service rate, ρ = λ/μ

**f)** Based on your results, which arrival rate(s) lead to acceptable service levels? Why?

---

## Question 2: Supermarket Checkout Optimization (M/M/c Queue)

### Scenario
A supermarket manager needs to decide how many checkout lanes to operate during afternoon hours (2pm-6pm). Operating too many checkouts wastes staff costs, but too few leads to long queues and customer dissatisfaction.

### Given Information
- Customers arrive at an average rate of **48 customers per hour**
- Average checkout time: **4 minutes per customer**
- Staff cost: **£12 per hour per checkout lane**
- Customer dissatisfaction cost: **£0.20 per minute** of wait time
- Simulation time: **240 minutes** (4 hours)

### Tasks

**a)** Using the M/M/c code from Segment 2 (Petrol Station), adapt it to model the supermarket checkout system.

**b)** Run simulations with **2, 3, 4, 5, and 6 checkout lanes**.

**c)** For each configuration, calculate:
   - System utilization (ρ = λ / (c × μ))
   - Average wait time
   - Average queue length
   - Percentage of customers who waited

**d)** For each configuration, calculate the **total cost** for the 4-hour period:
   - **Staff cost** = (Number of lanes) × (£12/hour) × (4 hours)
   - **Wait cost** = (Total customers served) × (Average wait time) × (£0.20/minute)
   - **Total cost** = Staff cost + Wait cost

**e)** Create a visualization showing:
   - Total cost vs number of checkout lanes
   - Breakdown showing staff costs and wait costs (stacked bar chart)

**f)** What is the optimal number of checkout lanes? Why?

---

## Question 3: Call Center Capacity Planning (M/M/c Queue)

### Scenario
A customer service call center operates 24/7. Management wants to maintain a service level where **at least 80% of callers** wait less than 2 minutes before speaking to an agent.

### Given Information
- Average call arrival rate: **12 calls per hour** (varies by time of day)
- Average call handling time: **8 minutes**
- Peak hours have **50% higher** arrival rate (18 calls per hour)
- Off-peak hours have **30% lower** arrival rate (8.4 calls per hour)
- Simulation time for each scenario: **480 minutes** (8 hours)

### Tasks

**a)** Adapt the M/M/c code from Segment 2 to model the call center.

**b)** For **normal hours** (12 calls/hour):
   - Test configurations with 2, 3, 4, and 5 agents
   - Determine the minimum number of agents needed to meet the service level (80% of callers wait < 2 minutes)

**c)** For **peak hours** (18 calls/hour):
   - Test the same configurations (2-5 agents)
   - Determine the minimum number needed to meet the service level

**d)** For **off-peak hours** (8.4 calls/hour):
   - Determine the minimum number of agents needed

**e)** Create a visualization comparing:
   - Average wait time vs number of agents (for all three periods)
   - Percentage of callers waiting < 2 minutes vs number of agents

**f)** Propose a staffing schedule: how many agents for normal, peak, and off-peak hours?

---

## Question 4: Manufacturing Machine Reliability Analysis (Machine Breakdowns)

### Scenario
A factory has a CNC machine that processes metal parts. The machine occasionally breaks down, interrupting production. The factory manager wants to understand how machine reliability affects production output and costs.

### Given Information
- Parts arrive at an average rate of **1 part every 15 minutes**
- Average processing time: **10 minutes per part**
- Repair cost: **£300 per breakdown**
- Delay penalty: **£50 per hour** for each hour a part is delayed beyond its expected processing time
- Part profit: **£500 per completed part**
- Simulation time: **2 shifts** (16 hours = 960 minutes)

### Tasks

**a)** Using the code from Segment 3 (Machine Breakdowns), implement the CNC machine simulation.

**b)** Run simulations with the following reliability scenarios:

| Scenario | MTBF (hours) | MTTR (hours) | Description |
|----------|--------------|--------------|-------------|
| A        | 100          | 2            | New machine |
| B        | 50           | 2            | Good condition |
| C        | 30           | 3            | Average condition |
| D        | 20           | 4            | Poor condition |
| E        | 15           | 5            | Very poor condition |

**c)** For each scenario, collect:
   - Total parts completed
   - Average completion time per part
   - Average interruptions per part
   - Total number of breakdowns
   - Machine availability (MTBF / (MTBF + MTTR))

**d)** Calculate the **total profit** for each scenario:
   - **Revenue** = (Parts completed) × £500
   - **Repair costs** = (Total breakdowns) × £300
   - **Delay costs** = (Parts completed) × (Avg delay per part) × £50/hour
     - Where: Avg delay = max(0, Actual completion time - Expected time)
     - Expected time = 10 minutes
   - **Profit** = Revenue - Repair costs - Delay costs

**e)** Create visualizations showing:
   - Parts completed vs MTBF
   - Total profit vs MTBF
   - Average interruptions per part vs MTBF

**f)** At what MTBF level does the machine become too unreliable? Should it be replaced or refurbished?

---

## Question 5: Hospital Emergency Department (Integrated Challenge)

This question is particularly hard, we will be looking into something similar next week, so don't worry if you find it too challenging to attempt.

### Scenario
A hospital Emergency Department (ED) has two types of patients: **Standard** and **Urgent**. Urgent patients should be prioritized and experience minimal waiting. The hospital wants to optimize staffing while maintaining quality of care.

### Given Information
- **Standard patients:** Arrive at 3 patients/hour, average treatment time 20 minutes
- **Urgent patients:** Arrive at 1 patient/hour, average treatment time 30 minutes
- Urgent patients should be seen with **priority**
- ED doctors can be interrupted to treat urgent patients
- Number of doctors available: **to be determined**
- Cost of doctor: **£40 per hour**
- Target: **90% of urgent patients** wait less than 10 minutes
- Target: **80% of standard patients** wait less than 30 minutes
- Simulation time: **12 hours** (one shift)

### Tasks

**a)** Design a simulation that combines concepts from M/M/c queues and preemptive resources:
   - Two patient arrival processes (standard and urgent)
   - Doctors modeled as PreemptiveResource
   - Urgent patients interrupt standard patients if all doctors busy
   - Collect separate statistics for each patient type

**b)** Test configurations with **2, 3, 4, and 5 doctors**.

**c)** For each configuration, track:
   - For urgent patients: average wait time, % waiting < 10 min
   - For standard patients: average wait time, % waiting < 30 min, average interruptions
   - Total patients treated (both types)
   - Doctor utilization

**d)** Calculate the **total operational cost** for the 12-hour shift:
   - **Doctor costs** = (Number of doctors) × £40/hour × 12 hours
   - **Patient dissatisfaction cost:**
     - Urgent: £5 per minute of wait time
     - Standard: £1 per minute of wait time
   - **Total cost** = Doctor costs + Dissatisfaction costs

**e)** Create visualizations showing:
   - Wait times for both patient types vs number of doctors
   - Percentage meeting service targets vs number of doctors
   - Total cost breakdown

**f)** What is the optimal number of doctors? Do you meet the service level targets? What's the impact of interruptions?

### Hints
- Use `PreemptiveResource` from Segment 3
- Assign priority=0 to urgent patients, priority=1 to standard patients
- Standard patients need to track if they were interrupted and resume treatment

---

## Tips

1. Start with the code from the lecture segments
2. Test with short simulation times first to verify your code works
3. Always check utilization (ρ) - if ρ ≥ 1, the system is unstable!
4. Use visualizations to understand what's happening
5. Compare simulation results with theoretical formulas where possible

