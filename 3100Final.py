import random
import math

#For part 1-(c)
def runTest(N, p, nstar) :
    numTests = []
    for i in range(1000) :
        numTests.append(0)
        for k in range(math.floor(N/nstar)) :
            if (random.random() > (1-(1-p)**nstar)) :
                numTests[i] += 1
            else :
                numTests[i] += 1 + nstar
        leftovers = N%nstar
        if (leftovers > 0 ) :
            if (random.random() > (1 - (1 - p) ** leftovers)):
                numTests[i] += 1
            else:
                numTests[i] += 1 + leftovers
    avg = sum(numTests)/len(numTests)
    print(f"Average for N={N}, p={p}, and n*={nstar} is {avg}")

N=10000
pvals = [.01, .04, .07, .1]
nstar= [11, 6, 4, 4]
GDPCD = 145.86
#for i in range(len(pvals)) :
 #   runTest(N, pvals[i], nstar[i])



#For part 1-(d)
class Person :
    GDPCD = 172
    infected = False
    days_since_last_test = 10
    days_since_infected = 0
    p = 0
    def __init__(self, p) :
        self.p = p
        self.next_day()

    def test(self):
        if (self.infected) :
            return True
        else :
            self.days_since_last_test = 0
            return False

    def reset_test_days(self):
        self.days_since_last_test = 0

    def get_days(self):
        return self.days_since_last_test

    def next_day(self):
        if (self.infected) :
            if (self.days_since_infected >= 21):
                self.infected = False
            else :
                self.days_since_infected += 1
        else :
            if (random.random() < self.p) :
                self.infected = True
                self.days_since_infected = 0
        self.days_since_last_test += 1

def group_test(group) :
    result = False
    for person in group :
        if (person.infected) :
            result = True
    if (not result) :
        for person in group :
            person.reset_test_days()
    return result

#simulating dorfman group strategy
def simulate_groups(n, p) :
    population = []
    #initialize the population
    for i in range(10000) :
        person = Person(p)
        population.append(person)
    GDP = 0
    next_person = 0
    #simulate for 3 months
    for day in range(90) :
        numtests = 0
        #Testing
        while (numtests < 500) :
            if (next_person + n >= 10000) :
                group = population[next_person:9999]
            else :
                group = population[next_person:next_person+n]
            result = group_test(group)
            numtests += 1
            if (numtests == 500):
                break
            if (result) :
                for person in group :
                    if (numtests == 500):
                        break
                    person.test()
            if (numtests < 500) :
                if (next_person + n >= 10000):
                    next_person = 0
                else :
                    next_person = next_person + n
        #Working and infection
        for person in population :
            if (person.days_since_last_test <= 7 and  not person.infected) :
                GDP += person.GDPCD
            person.next_day()
    return GDP

#simulating an individual testing strategy
def simulate_individual(n, p) :
    population = []
    #initialize the population
    for i in range(10000) :
        person = Person(p)
        population.append(person)
    GDP = 0
    next_person = 0
    #simulate for 3 months
    for day in range(90) :
        numtests = 0
        #Testing
        while (numtests < 500) :
            population[next_person].test()
            numtests += 1
            if (next_person == 9999) :
                next_person = 0
            else :
                next_person += 1
        #Working and infection
        for person in population :
            if (person.days_since_last_test <= 7) :
                GDP += person.GDPCD
            person.next_day()
    return GDP


def expected_dorfman_tests(p, n) :
    return 1 + n*(1-(1-p)**n)

def expected_binary_tests(p, n) :
    if (n < 2) :
        return n
    if (n == 2) :
        return ((1-p)**2)+2*(p*(1-p)) +3*p
    else :
        En_2 = expected_binary_tests(p, n/2)
        return 1 + 2*En_2*(1-(1-p)**(n/2)) + En_2*((1-p)**(n/2))*(1-(1-p)**(n/2))

#for 2-(d)
def optimize_n(p, nvals) :
    tests_person = {}
    for n in nvals :
        avg_tests = n/(expected_binary_tests(p,n))
        tests_person[n] = avg_tests
    return tests_person


n = 4
p = .1
#group_GDP = simulate_groups(n, p)
#individual_GDP = simulate_individual(n, p)
#possible_GDP = 10000*90*172
#print(f"GDP lost using group method is {(possible_GDP - group_GDP)/possible_GDP}")
#print(f"GDP lost using individual method is {(possible_GDP - individual_GDP)/possible_GDP}")



def optimize_set(nvals, pvals) :
    for p in pvals:
        result = optimize_n(p, nvals)
        max = 0
        maxn = 0
        for n in nvals:
            eff = result.get(n)
            if (eff is not None and eff > max):
                max = eff
                maxn = n
        print(
            f"The most efficient group size for p = {p} is n = {maxn}, where the expected number of people cleared per test is {max}")

nvals = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
pvals = [.01, .04, .07, .1]
#print(optimize_set(nvals,pvals)

#for part 2-(e)
def screen_tests(strategy, np_pairs, pvals, population) :
    for p in pvals :
        n = np_pairs.get(p)
        leftovers = population % n
        if (strategy == "binary") :
            leftover_tests = expected_binary_tests(p, leftovers)
        else :
            leftover_tests = expected_dorfman_tests(p, leftovers)
        groups = math.floor(population/n)
        if (strategy == "binary") :
            main_group_tests = groups * expected_binary_tests(p, n)
        else :
            main_group_tests = groups * expected_dorfman_tests(p, n)
        print(f"Expected tests = {main_group_tests + leftover_tests} for the {strategy} strategy, when n = {n} and p = {p}")

dorfman_group_sizes = {.01 : 11, .04 : 6, .07 : 4, .1 : 4}
binary_group_sizes = {.01 : 256, .04 : 64, .07 : 32, .1 : 16}
screen_tests("dorfman", dorfman_group_sizes, pvals, 10000)
screen_tests("binary", binary_group_sizes, pvals, 10000)
