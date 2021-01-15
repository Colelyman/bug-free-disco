
all: python3/CRISPResso2Align.cpython-37m-darwin.so python2/CRISPResso2Align.so c/libfun.so \
	p3time p2time ctime

.PHONY: p3time p2time ctime

# Compile libraries

python3/CRISPResso2Align.cpython-37m-darwin.so: python3/setup.py python3/CRISPResso2Align.pyx
	cd python3 && \
	python3 setup.py build_ext --inplace

python2/CRISPResso2Align.so: python2/setup.py python2/CRISPResso2Align.pyx
	cd python2 && \
	python2 setup.py build_ext --inplace

c/libfun.so: c/CRISPResso2Align.c
	gcc -fPIC -O3 -shared -o $@ $<

# Run time tests
p3time: python3/CRISPResso2Align.cpython-37m-darwin.so python3/time_nw.py
	echo "Python 3 Times"
	cd python3 && \
	python3 time_nw.py

p2time: python2/CRISPResso2Align.so python2/time_nw.py
	echo "Python 2 Times"
	cd python2 && \
	python time_nw.py

ctime: c/libfun.so c/time_function.py
	echo "C called from Python 3 Times"
	cd c && \
	python3 time_function.py
