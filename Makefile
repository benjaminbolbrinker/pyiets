fold=./tests/sampleinput_michael
h2O=./tests/sampleinput


test:
	make clean && ./pyiets.py ${fold}

testh2O:
	make clean && ./pyiets.py ${h2O}

clean: 
	rm -rf ${fold}/*dissortions* ${fold}/*.restart ${fold}/output ${h2O}/*dissortions* ${h2O}/*.restart ${h2O}/output
