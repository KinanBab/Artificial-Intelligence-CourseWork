/*
 * @author Kinan Dak Al Bab
 * @date 06/10/2013
 * ID: 201205052
 * Description:	This file contains the State class, which represents a State in the nQueens problem.
 * IMPORTANT REMARK:
 *		Please Note That this project was created using Eclipse. Adding the library "stdlib.jar"
 *		was done via Eclipse, and the image file "queen.png" was placed in the root directory of
 *		the eclipse project. In order for this code to run it is preferable that you test it in
 *		eclipse. further more, if you are running it outside eclipse (command line), you are 
 *		responsible for including the library and placing the image in the proper directory.
 *  
 */

import java.awt.Color;
import java.util.ArrayList;
import java.util.Random;

public class State {
   /*
	* OVERVIEW:
	* 		This class represents a state in the (n)queens problem.
	*		The state is represented as an (n) size integer array in which the item at index (i) represents the row on which the queen of 
	* 		column (i) is taking. This representation is similar to that in Section 1.4 in the book.
	* 
	*/

	private int[] queens; //stores the position of each queen
	private int perf;
	
	public State(int size) {
		//REQUIRES: Size > 1.
		//EFFECTS:	Creates a state to represent a queens problem for a size x size chess board.
		//			Queens are placed randomly on the board.
		Random r = new Random();	
		
		queens = new int[size];
		for(int i = 0;i < size;i++) {
			queens[i] = r.nextInt(size);
			perf += i;
		}
	}

	public State(int[] n) throws IllegalArgumentException {
		//REQUIRES: n.size > 1.
		//EFFECTS:	Creates a state to represent a queens problem for a size x size chess board.
		//			Queens are placed on the board according to n.
		//			throws IllegalArgumentException if n contained illegal positions for a queen, I.e. outside the board.
		queens = new int[n.length];
		
		for(int i = 0;i < n.length;i++) {
			if(n[i] > n.length-1 || n[i] < 0)
				throw new IllegalArgumentException();
			
			queens[i] = n[i]; //copy by value
			perf += i;
		}		
	}

	public int getCost() {
		//REQUIRES: ...
		//EFFECTS:	return the number of queens attacking each other.
		//			queens can attack diagonally or horizontally.
		//			the number returned represents the number of distinct pairs of queens that attack each other.
		
		int cost = 0;
		
		for(int i = 0;i < queens.length;i++) {
			for(int j = i+1;j < queens.length;j++) {
				if(queens[i] == queens[j])	cost++;	//increase the counter if queens attack each other horizontally
				else if(Math.abs(queens[j]-queens[i]) == Math.abs(j - i)) cost++;	//increase the counter if queens attack each other diagonally
			}
		}
		
		return cost;
	}

	public int getPerf() {
		//REQUIRES: ...
		//EFFECTS:	return the number of queens not-attacking each other.
		//			queens can attack diagonally or horizontally.
		//			the number returned represents the number of distinct pairs of queens that don't attack each other.
		
		int p = 0;
		
		for(int i = 0;i < queens.length;i++) {
			for(int j = i+1;j < queens.length;j++) {
				if(queens[i] == queens[j])	continue; //if queens attack each other horizontally don't increase the counter
				else if(Math.abs(queens[j]-queens[i]) == Math.abs(j - i)) continue;	//if queens attack each other diagonally don't increase the counter
				p++;
			}
		}
		
		return p;
	}
	
	public boolean isGoal(boolean max) {
		//REQUIRES: ...
		//EFFECTS:	return true if This is a goal state, false otherwise.
		//			max specify if it is a maximization problem (true), or a 
		//			minimization problem (false).
		if(!max) //minimization problem, cost must be minimal.
			return getCost() == 0;
		
		//maximization problem, Perf must be maximum
		return getPerf() == perf;
	}

	public boolean isEqual(State s) {
		//REQUIRES: s is not null.
		//EFFECTS:	returns true if the current state and s are equal
		//			I.e. queens in the same rows are placed in the same columns in both states.
		if(s.queens.length != queens.length)
			return false;
		
		for(int i = 0;i < queens.length; i++) {
			if(s.queens[i] != queens[i])
				return false;
		}
		
		return true;
	}

	public State[] getSuccessor() {
		//REQUIRES:	...
		//EFFECTS:	returns all the successors as an array of States. 
		//			The successors of a state are all possible states generated by moving a single
		//			queen to another square in the same column, so for an n by n board each state
		//			has 56 successors.
		ArrayList<State> result = new ArrayList<State>();
		
		int[] tmp = queens;
		for(int i = 0;i < queens.length;i++) {
			int t = queens[i]; 
			for(int j = 0; j < queens.length;j++) {
				if(t == j)	
					continue;
				
				tmp[i] = j;
				result.add(new State(tmp));
			}
			tmp[i] = t;
		}
		
		return result.toArray(new State[0]); //new array of size 0 is provided as arguments to get an array of type State[]
	}

	public String toString() {
		//REQUIRES: ...
		//EFFECTS:	returns the state as a string of the form (03456345). each number represents
		//			the row of the queen in that column (starting 0 to n-1).
		String res = "";
		for(int i = 0;i < queens.length;i++) {
			res = res + queens[i];
		}
		return res;
	}

	public void Draw() {
		//REQUIRES: ...
		//EFFECTS:	Draws the current state on the board.
		int cons = 400; //defining cons, which will be used as the length of the border square.
		
		StdDraw.setCanvasSize(cons, cons); //setting the canvas size
		StdDraw.clear(Color.WHITE); //clearing previous drawings
		StdDraw.setXscale(0, cons); //scaling the canvas
		StdDraw.setYscale(0, cons);
		
		int side = cons / queens.length;	//getting the length of the side of each square
		double r = side/2.0; 
		for(int i = 0;i < queens.length;i++) {
			double x = side * i + side/2.0;	//calculating the x position for the centers of the squares on this column
			for(int j = 0;j < queens.length;j++) {
				if((i+j) % 2 == 0)	//white squares have even sum of indexes, black have odd.
					StdDraw.setPenColor(Color.WHITE);
				else
					StdDraw.setPenColor(Color.BLACK);
				
				double y = side * j + side/2.0; //calculating the y position of the center of this square
				StdDraw.filledSquare(x, y, r); //drawing the square
				
				if(j == queens[i]) { //if this square has a queen, draw the image of the queen on it
					StdDraw.picture(x, y, "queen.png", side, side); //in eclipse, this would refer to {[ProjectPath]}/queen.png
				}
			}
		}
		
		StdDraw.setPenColor(Color.BLACK);
		StdDraw.square(side*queens.length/2.0, side*queens.length/2.0, side*queens.length/2.0); //drawing an outer border to the board
		
		StdDraw.show(1000); //drawing then waiting for one second before drawing whatever is to be drawn next
	}
	
}
