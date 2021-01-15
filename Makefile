
all: python3/CRISPResso2Align.so python2/CRISPResso2Align.so c/libfun.so

python3/CRISPResso2Align.so: python3/setup.py python3/CRISPResso2Align.pyx
	python3 python3/setup.py build_ext --inplace

python2/CRISPResso2Align.so: python2/setup.py python2/CRISPResso2Align.pyx
	python2 python2/setup.py build_ext --inplace

c/libfun.so: c/CRISPResso2Align.c
	gcc -fPIC -O3 -shared -o $@ $<
