#THOMSON
#Import libraries
import numpy as np 
import matplotlib.pyplot as plt 
import random 

#CONFIGURE PARAMETERS
N = 10000 # customer (samples)
d = 9 #number of strategies

# Creation of the simulation

conversion_rates = [0.03, 0.14, 0.07, 0.18, 0.12, 0.05, 0.21, 0.09, 0.01]
X = np.zeros((N,d))

for i in range(N):
    for j in range(d):
        if np.random.rand() <= conversion_rates[j]:
         X[i,j] = 1


# Implementing random selection and Thompson's sampling
strategies_selected_rs = []
strategies_selected_ts = []
total_reward_rs = 0 
total_reward_ts = 0
number_of_rewards_1  = [0] * d 
number_of_rewards_0  = [0] * d 
repentance_rs = []
repentance_ts = []
best_choice = np.argmax(conversion_rates) #So we can change the ratios as we wish. 
#By this I am assuming that the best decision in each round is not the one of 1 in that round, but the best strategy to try to get to the sale.

for n in range(0, N):
     # Random Selection
    strategy_rs = random.randrange(d)
    strategies_selected_rs.append(strategy_rs)
    reward_rs = X[n,strategy_rs]
    total_reward_rs += reward_rs
    best_reward_choice = X[n,best_choice]
    repentance_rs.append(best_reward_choice - reward_rs) if n == 0 else repentance_rs.append(repentance_rs[n-1] + best_reward_choice - reward_rs) 
    
    #Thompson sampling 
    strategy_ts = 0
    max_random = 0
    for i in range(0, d):
        random_beta = random.betavariate(number_of_rewards_1[i]+1, 
                                         number_of_rewards_0[i]+1)
        if random_beta > max_random:
            max_random = random_beta
            strategy_ts = i
    
    reward_ts = X[n,strategy_ts]
    if reward_ts == 1:
         number_of_rewards_1[strategy_ts] += 1
    else:
        number_of_rewards_0[strategy_ts] += 1
    strategies_selected_ts.append(strategy_ts)
    total_reward_ts += reward_ts
    repentance_ts.append(best_reward_choice - reward_ts) if n == 0 else repentance_ts.append(repentance_ts[n-1] + best_reward_choice - reward_ts) 
            
        
# Calculate relative and absolute return 
suscription_price = 100 # is the price of the subscription
absolute_return = (total_reward_ts - total_reward_rs) * suscription_price 
relative_return = ( total_reward_ts - total_reward_rs ) / total_reward_rs * 100 # a percentage
print("Absolute Return: {:.2f} €".format(absolute_return))
print("Relative Return: {:.0f} %".format(relative_return))


# Representation of the histogram of selections
plt.hist(strategies_selected_ts)
plt.title("Histogram of Selections")
plt.xlabel("Strategy")
plt.ylabel("Number of times the marketing strategy has been selected")
plt.show()

# Plot random regret curve
plt.figure(figsize=(12, 8))
plt.plot(range(0, N), repentance_rs, label='Random Selection')
plt.xlabel('Rounds')
plt.ylabel('Accumulated Repentance')
plt.title('Repentance Curve')
plt.legend()
plt.show()

# Graphing the Thompson regret curve
plt.figure(figsize=(12, 8))
plt.plot(range(0, N), repentance_ts, label='Thompson sampling')
plt.xlabel('Rounds')
plt.ylabel('Accumulated Repentance')
plt.title('Repentance Curve')
plt.legend()
plt.show()


# Graphing regret curves together
plt.figure(figsize=(12, 8))
plt.plot(range(0, N), repentance_rs, label='Random Selection')
plt.plot(range(0, N), repentance_ts, label='Thompson sampling')
plt.xlabel('Rondas')
plt.ylabel('Accumulated Repentance')
plt.title('Repentance Curve')
plt.legend()
plt.show()