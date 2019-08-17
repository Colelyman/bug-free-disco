#include <stdio.h> 
#include <string.h>
#include <stdlib.h>

size_t UP = 1, LEFT = 2, DIAG = 3, NONE = 4;
size_t MARRAY = 1, IARRAY = 2, JARRAY = 3;


int matrix[15][15] = { { 5,  -4,  -4,  -4,  -4,   1,   1,  -4,  -4,   1,  -4,  -1,  -1,  -1,  -2},
  				   				 {-4,   5,  -4,  -4,  -4,   1,  -4,   1,   1,  -4,  -1,  -4,  -1,  -1,  -2},
  				   				 {-4, -4,   5,  -4,   1,  -4,   1,  -4,   1,  -4,  -1,  -1,  -4,  -1,  -2},
			  				     {-4,  -4,  -4,   5,   1,  -4,  -4,   1,  -4,   1,  -1,  -1,  -1,  -4,  -2},
			  				     {-4,  -4,   1,   1,  -1,  -4,  -2,  -2,  -2,  -2,  -1,  -1,  -3,  -3,  -1},
			   				     {1,   1,  -4,  -4,  -4,  -1,  -2,  -2,  -2,  -2,  -3,  -3,  -1,  -1,  -1},
			   				     {1,  -4,   1,  -4,  -2,  -2,  -1,  -4,  -2,  -2,  -3,  -1,  -3,  -1,  -1},
			  				     {-4,   1,  -4,   1,  -2,  -2,  -4,  -1,  -2,  -2,  -1,  -3,  -1,  -3,  -1},
			  				     {-4,   1,   1,  -4,  -2,  -2,  -2,  -2,  -1,  -4,  -1,  -3,  -3,  -1,  -1},
			   				     {1,  -4,  -4,   1,  -2,  -2,  -2,  -2,  -4,  -1,  -3,  -1,  -1,  -3,  -1},
			  				     {-4,  -1,  -1,  -1,  -1,  -3,  -3,  -1,  -1,  -3,  -1,  -2, -2,  -2,  -1},
			  				     {-1,  -4,  -1,  -1,  -1,  -3,  -1,  -3,  -3,  -1,  -2,  -1,  -2,  -2,  -1},
			  				     {-1,  -1,  -4,  -1,  -3,  -1,  -3,  -1,  -3,  -1,  -2,  -2,  -1,  -2,  -1}, 
			  				     {-1,  -1,  -1,  -4,  -3,  -1,  -1,  -3,  -1,  -3,  -2,  -2,  -2,  -1,  -1},
			  				     {-2,  -2,  -2,  -2,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1} };
char codons[] = {'A','T','G','C','S','W','R','Y','K','M','B','V','H','D','N'};
int charint[90];
void setup(void) {
	for (int i=0; i < sizeof(codons); i++){
	     charint[codons[i]] = i;
	}
}
// charint maps bases to ints: A:0, T:1, G:2, etc...



char* global_align(char* seqj, char* seqi, int* gap_incentive){ //gap open, gap extend both -1
	int gap_open = -1;
	int gap_extend = -1;


	size_t max_j = strlen(seqj);
	size_t max_i = strlen(seqi);


	//dont know how to find length of gap_incentive in c.
	// if you pass it from the python, whats the point?
	//len gap_incentive is defined by the length of seqi

	if (gap_incentive[max_i-1] != 0){ // this isnt comprehensive, but it at least will detect if gap_incentive is short...
	    printf("\nERROR: Mismatch in gap_incentive length"); //(gap_incentive: %lu ref: %lu)\n", max_i+1, max_j+1);
        return NULL;
    }


    size_t i = 0, j = 0, seqlen, align_counter = 0, p;
    int diag_score, up_score, left_score, tscore;

    char *align_j;
    char *align_i;
    char ci;
    char cj;
    // PyObject pointers ai and aj... dont think we need anything here in c.



    // create 3 arrays of scores and 3 arrays of pointers
    // M array - best alignment so far ending with a match
    // I array - best alignment so far ending with a gap in Read (J) (insertion in ref, deletion in read)
    // J array - best alignment so far ending with a gap in Ref (I) (deletion in ref, insertion in read)
    int mScore[max_i+1][max_j+1];
    int iScore[max_i+1][max_j+1];
    int jScore[max_i+1][max_j+1];
    int mPointer[max_i+1][max_j+1];
    int iPointer[max_i+1][max_j+1];
    int jPointer[max_i+1][max_j+1];


    int min_score = gap_open * max_j * max_i;


    // Initializing match matrix
    for (int j = 1; j<max_j+1; j++) mScore[0][j] = min_score;
    for (int i = 1; i<max_i+1; i++) mScore[i][0] = min_score;
	for (int j = 1; j<max_j+1; j++) mPointer[0][j] = IARRAY;
    for (int i = 1; i<max_i+1; i++) mPointer[i][0] = JARRAY;
    mScore[0][0] = mPointer[0][0] = 0;

	
	// Initializing i matrix
	for (int j = 1; j < max_j+1; j++) iScore[0][j] = gap_extend * j;
	for (int i = 0; i < max_i+1; i++) iScore[i][0] = min_score;
	for (int j = 1; j < max_j+1; j++) iPointer[0][j] = IARRAY;


	// Initializing J matrix
	for (int i = 1; i < max_i+1; i++) jScore[i][0] = gap_extend * i;
	for (int j = 0; j < max_j+1; j++) jScore[0][j] = min_score;
	for (int i = 1; i < max_i+1; i++) jPointer[i][0] = JARRAY;


	int iFromMVal, iExtendVal, jFromMVal, jExtendVal, mVal, iVal, jVal;


	// Apply NW algorithm for inside squares (not last row or column)
	for(int i = 1; i < max_i; i++){
		ci = seqi[i-1];

		for(int j = 1; j < max_j; j++){
			cj = seqj[j-1];

			iFromMVal = gap_open + mScore[i][j-1] + gap_incentive[i];
			iExtendVal = gap_extend + iScore[i][j-1] + gap_incentive[i];

			if (iFromMVal > iExtendVal){
				iScore[i][j] = iFromMVal;
				iPointer[i][j] = MARRAY;
			} else {
				iScore[i][j] = iExtendVal;
				iPointer[i][j] = IARRAY;
			}

			jFromMVal = gap_open + mScore[i-1][j] + gap_incentive[i-1];
			jExtendVal = gap_extend + jScore[i-1][j];

			if (jFromMVal > jExtendVal) {
				jScore[i][j] = jFromMVal;
				jPointer[i][j] = MARRAY;
			} else {
				jScore[i][j] = jExtendVal;
				jPointer[i][j] = JARRAY;
			}

			mVal = mScore[i-1][j-1] + matrix[charint[ci]][charint[cj]];
			iVal = iScore[i-1][j-1] + matrix[charint[ci]][charint[cj]];
			jVal = jScore[i-1][j-1] + matrix[charint[ci]][charint[cj]];


			if (mVal > jVal){
				if (mVal > iVal){
					mScore[i][j] = mVal;
					mPointer[i][j] = MARRAY;
				} else {
					mScore[i][j] = iVal;
					mPointer[i][j] = IARRAY;
				}
			} else {
				if (jVal > iVal) {
					mScore[i][j] = jVal;
					mPointer[i][j] = JARRAY;
				} else {
					mScore[i][j] = iVal;
					mPointer[i][j] = IARRAY;
				}

			}

		}
	}

	for(int i = 0; i < max_i; i++){
		for(int j = 0; j < max_j; j++){
			printf("%i ", mScore[i][j]);
		} printf("\n");
	}


    return NULL;

} 



















