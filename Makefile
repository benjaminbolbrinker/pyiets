test:
	make clean && ./pyiets.py tests/sampleinput

clean: 
	rm -rf ./tests/sampleinput/*dissortions* ./tests/sampleinput/*.restart ./tests/sampleinput/output
