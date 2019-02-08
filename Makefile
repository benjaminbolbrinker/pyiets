C10H4Au6S2=./tests/sampleinput_michael
H2O=./tests/sampleinput


test_all: test_H2O test_C10H4Au6S2

test_C10H4Au6S2:
	./pyiets.py ${C10H4Au6S2}

test_H2O: 
	./pyiets.py ${H2O}

clean: clean_C10H4Au6S2 clean_H2O

clean_C10H4Au6S2: 
	rm -rf ${C10H4Au6S2}/*distortions* ${C10H4Au6S2}/*.restart ${C10H4Au6S2}/output 

clean_H2O:
	rm -rf ${H2O}/*distortions* ${H2O}/*.restart ${H2O}/output 
