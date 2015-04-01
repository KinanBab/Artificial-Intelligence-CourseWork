/*
 * @author Kinan Dak Al Bab
 * @date 06/10/2013
 * ID: 201205052
 * Description: This file contains static methods for solving the nQueens problem. each Method uses a different
 * 				local search algorithm.
 */

import java.util.ArrayList;

public class NQueens {
	//CONSTANTS:
	//MODIFY THESE TO CHANGE THE TUNE OF SIMULATED ANNEALING ALGORITHM, OR GENETIC ALGORITHM.
	//AFTER TESTING I CHOSE THESE CONSTANTS BECAUSE THEY BALANCE A GOOD
	//SUCCESS PERCETANGE WITH AN ACCEPTABLE RUNNING TIME FOR THE ALGORITHMS
	private final static double RATIOANN = 75; //the ratio to use to generate temperature in respect to time
	private final static int RATIOPOPSIZE = 10; //size of problem * ratioPopSize = the size of population for genetic algorithm
	
	/*
	 * @param args the command line arguments:
	 * @param args[0] the board size
	 * @param args[1] number of times to repeat the algorithm
	 * @param args[2] the algorithm to be used: 1 for HillClimbing, 2 for Random Restart, 3 for Simulated Annealing, 4 for Genetic Algorithm.
	 * 
	 */
	public static void main(String[] args) {
		//The main method (entry point for the project).
		//Reads the board size, number of times to repeat the algorithm, the algorithm to be used from the command line.
		//It outputs the following:
		//	1-) the success percentage.
		//	2-) the average number of moves when it succeeds.
		//	3-) the average number of moves when it fails.
		
		double percentage = 0; //declaring variables to store results
		double suc = 0;
		double fail = 0;
		
		int size = Integer.parseInt(args[0]); //reading user input via command line arguments
		int n = Integer.parseInt(args[1]);
		int a = Integer.parseInt(args[2]);
		
		String alg;	//To store the name of the algorithm used
		
		if(a == 1) { //algorithm is HillClimbing
			alg = "HillClimbing";
			for(int i = 0;i < n;i++) {	//executing the algorithm n times
				ArrayList<Object> res = hillClimb(size);
				if(((State)res.get(0)).isGoal(false)) {	//storing the results of this execution
					percentage++;
					suc += (Integer) res.get(1);
				} else {
					fail += (Integer) res.get(1);
				}
			}
		} else if(a == 2) { //algorithm is Random Restart
			alg = "Random Restart";
			System.out.print("Do you want to draw each iteration (Y/N): "); //asking user for input
			char d = StdIn.readString().toLowerCase().charAt(0);
			for(int i = 0;i < n;i++) {	//executing the algorithm n times
				ArrayList<Object> res = randomHillClimb(size, d == 'y');
				if(((State)res.get(0)).isGoal(false)) {	//storing the results of this execution
					percentage++;
					suc += (Integer) res.get(1);
				} else {
					fail += (Integer) res.get(1);
				}
			}
		} else if(a == 3) { //algorithm is Simulated Annealing
			alg = "Simulated Annealing";
			for(int i = 0;i < n;i++) {	//executing the algorithm n times
				ArrayList<Object> res = SimulatedAnnealing(size);
				if(((State)res.get(0)).isGoal(false)) {	//storing the results of this execution
					percentage++;
					suc += (Integer) res.get(1);
				} else {
					fail += (Integer) res.get(1);
				}
			}
		} else { //algorithm is Genetic Algorithm
			alg = "Genetic Algorithm";
			for(int i = 0;i < n;i++) {	//executing the algorithm n times
				ArrayList<Object> res = GA(size);
				if(((State)res.get(0)).isGoal(false)) {	//storing the results of this execution
					percentage++;
					suc += (Integer) res.get(1);
				} else {
					fail += (Integer) res.get(1);
				}
			}
		}
		
		suc = suc/percentage;	//finalizing results
		fail = fail / (n - percentage);
		percentage = percentage / n;
		
		System.out.println("Algorithm: "+alg);	//Producing Output
		System.out.println("\tSize: "+size+", Number of Repetitions: "+n+".");
		System.out.println("Results:");
		System.out.println("\tSuccess Percentage: "+(percentage*100)+"%.");
		System.out.println("\tAvergae moves count on success: "+suc+", Average moves count on failure: "+fail+".");		
	}
	
	public static ArrayList<Object> hillClimb(int size) {
		//REQUIRES: size > 1.
		//EFFECTS:	returns an ArrayList, the first element is the final state, the second element is the number of steps to get result.
		//			the final state is acquired via the HillClimg search algorithm. the final state might be a goal state or not.
		//CLAUSES:	14% success rate, Average of 4 steps for success and 3 steps for failure.
		
		/*
		 *  IMPLEMENTATION SKETCH:
		 *		s <- random initial state.
		 *		counter <- 0
		 *		WHILE True DO
		 *			neighbor <- successor of s with minimum cost (break ties randomly).
		 *			IF neighbor.cost >= s.cost THEN
		 *				break.
		 *			ELSE
		 *				s <- neighbor.
		 *			counter++.
		 *		Return {s, counter}.
		 *
		 */
		
		State s = new State(size); //the initial state
		int counter = 0;
		while(true) {
			State neighbor = getMinCost(s.getSuccessor()); //Calling helper method to get the minimum-cost successor
			if(neighbor.getCost() >= s.getCost()) 
				break;
			
			s = neighbor;
			counter++;
		}
		
		ArrayList<Object> res = new ArrayList<Object>(); //storing the result
		res.add(s);
		res.add(counter);
		return res;
	}
	
	public static ArrayList<Object> randomHillClimb(int size,boolean draw) {
		//REQUIRES: size > 1.
		//EFFECTS:	returns an ArrayList, the first element is the final state, the second element is the number of steps to get result.
		//			the final state is acquired via the random restart hill climb search algorithm.
		//CLAUSES:	100% success rate, Average of 22 steps.
		
		/*
		 *  IMPLEMENTATION SKETCH:
		 *		counter <- 0
		 *		DO
		 *			call hillClimb and save result.
		 *			s <- result.
		 *			counter <- counter + result[1].
		 
		 *			IF draw is true THEN
		 *				draw s.
		 *		WHILE s is not a goal state. 
		 *
		 *		Return {s, counter}.
		 *
		 */
		State s; //the initial State
		int counter = 0;
		
		do {
			ArrayList<Object> result = hillClimb(size); //calling hillClimb
			s = (State) result.get(0);
			counter += (Integer) result.get(1);
			
			if(draw) { //draw the last state in the iteration if draw is true
				s.Draw();
			}
		} while(!s.isGoal(false));	//restart if s is not a goal State
		
		ArrayList<Object> res = new ArrayList<Object>(); //storing the result
		res.add(s);
		res.add(counter);
		return res;
	}
	
	public static ArrayList<Object> SimulatedAnnealing(int size) {
		//REQUIRES: size > 1.
		//EFFECTS:	returns an ArrayList, the first element is the final state, the second element is the number of steps to get result.
		//			the final state is acquired via the Simulated Annealing search algorithm. the final state might be a goal state or not.
				
		/*
		 *  IMPLEMENTATION SKETCH:
		 *		s <- random initial state.
		 *		counter <- 0
		 *		WHILE s is not goal DO
		 *			t <- schedule(counter).
		 *			successors[] <- s.getSucessors().	
		 *			WHILE true DO (*)
		 *				neighbor <- random element from successors.
		 *				delta <- s.cost - neighbor.cost
		 *				IF delta > 0 THEN
		 *					s <- neighbor.
		 *					break.
		 *				ELSE
		 *					s <- neighbor with a probability of e^(delta/t)
		 *					break.
		 *			counter++.
		 *		Return {s, counter}.
		 *
		 *			(*) : 	keep looping until you pick a neighbor of s, counter should represent
		 *					the number of swaps (steps), so for each time we finish executing the inner
		 *					loop we increment the counter. (not on every iteration of the inner loop).
		 */
				
		State s = new State(size); //the initial state
		int counter = 0;
		while(!s.isGoal(false)) {
			double t = schedule(counter); //getting the Temperature from the schedule
				
			State[] successors = s.getSuccessor();
			while(true) {
				int i = (int) (Math.random() * successors.length);
				State neighbor =  successors[i]; //neighbor is equal to a random successor of s
					
				int delta = s.getCost() - neighbor.getCost(); //calculate the difference in cost
				if(delta > 0) { //if neighbor has less cost then s, set s to neighbor
					s = neighbor;
					break;
				} else { //set s to neighbor only with a probability of e^(delta/t)
					double p = Math.E;
					p = Math.pow(p, delta/t);
					if(Math.random() < p) {
						s = neighbor;
						break;
					}
				}
			}
			
			counter++;
		}
				
		ArrayList<Object> res = new ArrayList<Object>(); //storing the result
		res.add(s);
		res.add(counter);
		return res;
	}
	
	public static ArrayList<Object> GA(int size) {
		//REQUIRES: size > 1.
		//EFFECTS:	returns an ArrayList, the first element is the final state, the second element is the number of steps to get result.
		//			the final state is acquired via the Genetic algorithm. the final state might be a goal state or not.
		//FINE TUNING:
		//			The success percentage depends on the size of the population, and the number
		//			of iterations.
		//			The higher the size is the higher the percentage, because more sizable population gives more chance to mutations
		//			that will be preserved if they yielded a State with a higher number of queens not attacking each other, I.e. higher
		//			Probability in the natural selection section.
		//			The more iterations we provide the algorithm the more natural selections it will do, thus it will keep
		//			discarding States with low number of queens not attacking each other, and keep moving towards 
		//			higher percentages.
		//			With a population of 8 * 10, and a 200 Iterations, the 8 queen problem has a success percentage of 38%.
		
		/*
		 * IMPLEMENTATION SKETCH:
		 * 		counter <- 0.
		 * 		generate population of a specific size.
		 * 		WHILE no p in population is fit enough (is goal) DO
		 * 			create new_population of the same size.
		 * 			WHILE i < newpopulation.size DO
		 * 				new_population[i] <- some state : population according to the probability table.
		 * 				i <- i + 1.
		 * 
		 * 			population <- new_population			
		 * 
		 * 			WHILE i < population.size DO
		 * 				index <- random[1, size].
		 * 				crossover at index between population[i], population[i+1].
		 * 
		 * 			IF random < 0.1 (random event of 10% probability) THEN
		 * 				mutation_index <- random[0, size-1].
		 * 				mutation_value <- random[0, size-1].
		 * 				population[i].mutation_index = mutation_value.
		 * 
		 *			IF random < 0.1 (random event of 10% probability) THEN
		 * 				mutation_index <- random[0, size-1].
		 * 				mutation_value <- random[0, size-1].
		 * 				population[i+1].mutation_index = mutation_value.		 * 
		 * 
		 * 			counter <- counter + 1.
		 * 		return {fittest(population), counter}.
		 * 
		 */
		int counter = 0;
		
		State[] population = new State[size*RATIOPOPSIZE]; //generating a population of size (size * 10)
		for(int i = 0;i < population.length;i++) {
			population[i] = new State(size);
		}
		
		while(true) { 
			State[] newpop = new State[population.length]; //natural selection
			double[] probs = getProbobilityList(population); //getting the probability list (helper method)
			for(int i = 0;i < population.length;i++) {
				double r = Math.random() * 100; //getting a number between 0 and 99
				for(int j = 0;j < probs.length;j++) {
					if(r < probs[j]) { 
						newpop[i] = population[j]; //selecting a member of population randomly according to the probability list
						break;
					}
				}
			}
			population = newpop;
		
			for(int i = 0;i+1 < population.length;i+=2) { //cross over
				int index = (int)(Math.random() * size) + 1 ; //generating a random cross over point
			
				String sub1 = population[i].toString().substring(0, index);
				String s1 = population[i].toString().substring(index);
			
				String sub2 = population[i+1].toString().substring(0, index);
				String s2 = population[i+1].toString().substring(index);
			
				String new1 = sub1 + s2;
				String new2 = sub2 + s1;
			
				int[] arr1 = new int[size];
				int[] arr2 = new int[size];
				for(int j = 0;j < size;j++) {
					arr1[j] = Integer.parseInt(new1.charAt(j)+"");
					arr2[j] = Integer.parseInt(new2.charAt(j)+"");
				}
			
				if(Math.random() < 0.1) { // 10% Probable mutation for the (i)th state 
					index = (int) (Math.random() * size);
					int newVal = (int) (Math.random() * size);

					arr1[index] = newVal;
				}

				if(Math.random() < 0.1) { // 10% Probable mutation for the (i+1)th state 
					index = (int) (Math.random() * size);
					int newVal = (int) (Math.random() * size);
				
					arr2[index] = newVal;
				}		
			
				population[i] = new State(arr1); //saving the new cross-over mutated states 
				population[i+1] = new State(arr2); 
			}
			
			boolean flag = false;
			for(State s : population) { //break if one state is fit enough
				if(s.isGoal(true)) {
					flag = true;
					break;
				}
			}
			
			if(flag) break;
			counter++;
		}
				
		
		ArrayList<Object> res = new ArrayList<Object>();
		res.add(null);
		
		int max = Integer.MIN_VALUE;
		for(int i = 0;i < population.length;i++) {
			if(population[i].getPerf() > max) { //returning the state with max number of queens not attacking each other
				max = population[i].getPerf();
				res.set(0, population[i]);
			}
		}
		
		res.add(counter);
		return res;
	}

	private static State getMinCost(State[] states) {
		//REQUIRES: ...
		//EFFECTS:	return the state with minimum cost in states, null if states is empty.
		int min = Integer.MAX_VALUE;
		State s = null; //stores the result
		
		if(states != null) {
			for(State i : states) {
				if(i.getCost() < min) {
					min = i.getCost();
					s = i;
				}
			}
		}
		
		return s;
	}

	private static double schedule(double t) {
		//REQUIRES: t is not negative.
		//EFFECTS:	returns a number, this number must gradually become smaller as t gets bigger.
		if(t == 0) return RATIOANN;
		
		return RATIOANN/t; //RATIOANN is a constant defined above
	}

	private static double[] getProbobilityList(State[] population) {
		//REQUIRES:	population is not null.
		//EFFECTS:	returns the probability of each state of population being selected,
		//			such that p[i] = actualP[i] + p[i-1]. the last probability = 100, and each 
		//			state's probability is proportional to the states number of queens not 
		//			attacking each other.
		double[] probs = new double[population.length];
		
		double sum = 0; //stores the sum of all queens not attacking each other from all states (represents a probibility of 10
		for(State s : population) {
			sum += s.getPerf();
		}
		
		double parsum = 0; //partial sum (the sum of probabilities of states 0 -> i-1) 
		for(int i = 0;i < population.length;i++) {
			probs[i] = (population[i].getPerf() / sum) * 100; //calculating probability out of 100
			probs[i] += parsum; //p[i] = actualP[i] + p[i-1]
			parsum = probs[i];
			
		}
		
		return probs;
	}

}
