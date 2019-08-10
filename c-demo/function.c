#include <stdio.h> 
#include <string.h>
#include <stdlib.h>

// int myFunction(int num,const char *mystr) 
// { 
//     printf("str is %s",mystr);
//     if (num == 0) 
  
//         // if number is 0, do not perform any operation. 
//         return 0; 
//     else
// 	return 5;   
// } 

char* myFunction(int num,char *mystr) 
{ 
	//char* p = malloc(sizeof(*mystr));
	//strcpy(p, mystr);
    //return p;
    return mystr;
} 

// void freeMem(char* p){
// 	free(p);
	
// }




// might need to start worrying about memory allocation
