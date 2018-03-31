from enum import Enum
import scipy.stats as stat
import numpy as np



class HealthStat(Enum):
    """ health status of patients  """
    ALIVE = 1
    DEAD = 0

class Patient(object):
    def __init__(self, id, mortality_prob):
        """ initiates a patient
        :param id: ID of the patient
        :param mortality_prob: probability of death during a time-step (must be in [0,1])
        """
        self._id = id
        self._rnd = np.random       # random number generator for this patient
        self._rnd.seed(self._id)    # specifying the seed of random number generator for this patient
        self._mortalityProb = mortality_prob
        self._healthState = HealthStat.ALIVE  # assuming all patients are alive at the beginning
        self._survivalTime = 0

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        t = 0  # simulation current time

        # while the patient is alive and simulation length is not yet reached
        while self._healthState == HealthStat.ALIVE and t < n_time_steps:
            # determine if the patient will die during this time-step
            if self._rnd.sample() < self._mortalityProb:
                self._healthState = HealthStat.DEAD
                self._survivalTime = t + 1  # assuming deaths occurs at the end of this period

            # increment time
            t += 1

    def get_survival_time(self):
        """ returns the patient survival time """

        # return survival time only if the patient has died
        if self._healthState == HealthStat.DEAD:
            return self._survivalTime
        else:
            return None



class Cohort:
    def __init__(self, id, pop_size, mortality_prob):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param mortality_prob: probability of death for each patient in this cohort over a time-step (must be in [0,1])
        """
        self._initialPopSize = pop_size # initial population size
        self._patients = []      # list of patients
        self._survivalTimes = []    # list to store survival time of each patient
        self._survivefiveyear = 0

        # populate the cohort
        for i in range(pop_size):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id * pop_size + i, mortality_prob)
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        :returns simulation outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            # simulate
            patient.simulate(n_time_steps)
            # record survival time
            value = patient.get_survival_time()
            if not (value is None):
                self._survivalTimes.append(value)

    def get_survival_times(self):
        """ returns the survival times of the patients in this cohort"""
        return self._survivalTimes

    def get_initial_pop_size(self):
        return self._initialPopSize

    def per_after_five_year(self):
        for i in range(0,len(self._survivalTimes)-1):
            if self._survivalTimes[i] > 5:
                self.fiveyear += 1
            self.fiveyear = self.fiveyear/len(self._survivalTimes)
        return self.fiveyear




# problem 1
data = Cohort(2, 573, 0.1)
data.simulate(1000)
print("the percent is about", data.per_after_five_year())

# problem 2
print("if the probability of 5 year survival is q, then the number of participants that"
      "survived beyond 5 years in a cohort follows Binomial distribution with the parameter (N,q)")

# problem 3
likelihood = stat.binom.pmf(k=400, n=573, p=0.5, loc=0)
print("the likelihood should be", likelihood)

