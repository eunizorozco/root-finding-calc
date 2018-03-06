package application.algo;


public interface RootAlgorithm {	
	
	//return number of required init guess
	int getInitGuessNumber();
	
	//returns runtime in ms of last run algo
	long getRunTime();
	
	//returns memory used of last ran algo
	double getMemory();
	
	//returns root found
	double getRoot();
	
	//x either has 1, 2, or 3 values depending on the algo
	void setInitialGuesses(double... x);
	
	/*exp is the String input in calculator. exp has form: str1=str2.
	 *  must be converted by this method to 0=str2-str1
	 * */
	void setExpression(String exp);	
	
	//returns number of iterations
	int getNumIterations();
	
	String toString();	
}
