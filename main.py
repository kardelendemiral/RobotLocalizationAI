walls="x xx  xx x"
sensors=["on","on","off","on"]
# your code starts

import numpy as np

def getObservationProb(a):
    if walls[a] == 'x':
        return 0.7
    else:
        return 0.2

def getTransmissionProb(a, b): #transmission probability from a to b
    if (a+1)%2 == 0 and b == a+1:
        return 0.8
    if (a+1)%2 == 0 and b == a:
        return 0.2
    if (a+1)%2 == 1 and b == a+1:
        return 0.6
    if (a+1)%2 == 1 and b == a:
        return 0.4
    else:
        return 0

def filtering(T, probs, obs_matrix): # bunu yaparsak oldu
    print("bi şekilde filter")
    new_state = np.dot(obs_matrix, np.dot(T, probs))
    new_state_normalized = new_state / np.sum(new_state)
    return new_state_normalized

def filter(N, prev_probs, E, T, s):
    probs = np.zeros(N)
    for l in range(N):
        transmisson_probs = 0
        for lprev in range(N):
            transmisson_probs = transmisson_probs + T[lprev][l]*prev_probs[lprev]*E[s][lprev]

        probs[l] = transmisson_probs

    probs = probs / np.sum(probs) #normalize

    return probs


def create_observation_matrix(error_rate, no_discrepancies):
    sensor_list = []
    for number in no_discrepancies:
        probability = (1 - error_rate) ** (4 - number) * error_rate ** number
        sensor_list.append(probability)
        observation_matrix = np.zeros((len(sensor_list), len(sensor_list)))
        np.fill_diagonal(observation_matrix, sensor_list)
    return observation_matrix




probs = np.array([1/len(walls)]*len(walls))

l = len(walls)
T = np.zeros(shape = (l,l))
E = [[],[]]
for i in range(l):
    E[0].append(getObservationProb(i))
    E[1].append(1-getObservationProb(i))
    for j in range(l):
        T[i][j] = getTransmissionProb(i, j)

T[l-1][l-1] = 1 #at last grid, cannot move anymore
E = np.array(E)

sensor_readings = []
for s in sensors:
    if s == "on":
        sensor_readings.append(0)
    else:
        sensor_readings.append(1)


probs = [1/len(walls)]*len(walls)

for s in sensor_readings:
    probs = filter(l,probs, E, T ,s)

#print(probs)
probabilities = probs.tolist()
robot_pos_prob = max(probabilities)
robot_pos = probabilities.index(robot_pos_prob) + 1

# your code ends
print('The most likely current position of the robot is', robot_pos, 'withprobability',robot_pos_prob)
