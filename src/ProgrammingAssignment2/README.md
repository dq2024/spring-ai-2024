#### Instruction to Run: 
My frontend.py takes a file called Test (this is the inputfile with the puzzle encodings) \
It writes to a file called frontendOutput.txt \ 
DPLL.py takes frontendOutput.txt as input and writes to a file called DPLLoutput.txt \ 
My backend.py takes DPLLoutput.txt as input and writes the valid solution to the peg game to the command line \ 

I could not figure out a way around having the grader change my code in frontend.py if they are not testing with an inputfile called Test \ 
Since the instructions specify to not submit a Test file, I apologize if the inputFile (that my frontend.py takes as input) is named something other than Test. 

#### INSTRUCTIONS TO RUN (everything is in the same directory): 
python frontend.py \
python DPLL.py \
python backend.py 