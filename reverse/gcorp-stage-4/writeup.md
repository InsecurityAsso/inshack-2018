# G-Corp - stage 4: source code analysis and cracking (rev/cracking)

Now that you have the code source of the emergency override and the value of the
port on which the service is running you can try to find a key satisfying the
test.

You have to solve the following problem: find a 3D matrice of 4x4x4 resulting in
64 unknown values which once passed to the algorithm validates the result vector.

I think that this problem can solved with Z3prover but I didn't try. I'm interested 
in seeing how you hacked this stage.
