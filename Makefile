test:
	./pyiets.py tests/sampleinput

clean: 
	rm -rf ./tests/sampleinput/*dissortions* ./tests/sampleinput/*pyiets.restart*
