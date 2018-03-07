package application.algo;

import java.util.StringTokenizer;
import static application.algo.Utilities.evaluate;
public class InverseQuadraticInterpolation implements RootAlgorithm{
	private String exp;
	private double[] initGuess;
	
	//<tradeoffs>
	private long runTime = 0;
	private long memory = 0;
	private int numIterations = 0;
	private double accuracy = 0;
	private double convergenceRate = 0;
	//</tradeoffs>
	//tradeoff helper:
	private double errorSum = 0;
	//end tradeoffhelper
	
	
	private double root;
	public final static int REQUIRED_INITGUESS = 3;
	public final static int DIVERGENT_LIMIT = 1000;
	private static RootAlgorithm This;
	
	public static RootAlgorithm getAlgo() {
		if(This==null) {
			This = new InverseQuadraticInterpolation();
		}
		return This;
	}	
	//set inaccessible constructor:
	private InverseQuadraticInterpolation() {
		
	}	
	@Override
	public long getRunTime() {
		return runTime;
	}

	@Override
	public double getMemory() {
		return memory;
	}

	@Override
	public double getRoot() {
		computeRoot();		
		return root;
	}
	
	//computes root. updates numOf iterations. updates Memory usage
	private void computeRoot() {
		System.gc();
		long startMem = Runtime.getRuntime().freeMemory();
		numIterations = 0;
		memory = 0;
		runTime = 0;	
		double xnMinus2 = 0;
		double xnMinus1 = initGuess[0]; 
		double xn = initGuess[1];
		double xnPlus1 = initGuess[2];
		long start = System.nanoTime();
		
		do {	
			xnMinus2 = xnMinus1;
			xnMinus1 = xn;
			xn = xnPlus1;			 
			double ynM1 = evaluate(exp, xnMinus1);
			double yn = evaluate(exp, xn);
			double ynM2 = evaluate(exp, xnMinus2);
			
			double first = xnMinus2 * (ynM1*yn)/((ynM2-ynM1)*(ynM2-yn));
			double second = xnMinus1 * (ynM2*yn)  /  ((ynM1-ynM2)*(ynM1-yn));
			double third = xn * (ynM1*ynM2)  /  ((yn-ynM2)*(yn-ynM1));
			
			xnPlus1 = first + second + third;
			System.out.println(xnPlus1);
			numIterations++;
		}while(notStopping(xn, xnPlus1) && numIterations<=DIVERGENT_LIMIT);		
		root = xnPlus1;
		runTime = System.nanoTime() - start;
		memory = startMem - Runtime.getRuntime().freeMemory();
	}

	private boolean notStopping(double x, double xPrevious) {
		return Math.abs(x-xPrevious)>= 0.0000001;
	}

	@Override
	public void setInitialGuesses(double... x) {
		if(x.length!=REQUIRED_INITGUESS) throw new IllegalArgumentException(
				String.format("There must be %d initial guesses", REQUIRED_INITGUESS));
		initGuess = x;
	}
	
	
	@Override
	public void setExpression(String exp) {
		
		this.exp = processExp(exp);
		System.out.println(this.exp);
	}
	
	//processExp returns the right side of the equation when left side is 0
	private String processExp(String exp) {
		String[] expArr = exp.split("=");
		return expArr[1] + "-(" + expArr[0] + ")";
	}

	@Override
	public int getNumIterations() {
		return numIterations;
	}

	@Override
	public String toString() {
		return "Inverse Quadratic Interpolation";
	}

	@Override
	public int getInitGuessNumber() {
		return REQUIRED_INITGUESS;
	}


}
