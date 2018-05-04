#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#define S 256

#ifndef __ECA__
#define __ECA__
	
class ECA{
	
	public:
		std::bitset<8> rule;
		int* t0;
		int* t1;
		int cells;
		int gens;
		int den;
		int freq;

		ECA(std::bitset<8> rule, int cells, int gens, int den){
			for(int i=0; i<8; i++){
				this->rule[i]=rule[i];
			}
			this->cells=cells;
			this->gens=gens;
			this->den=den;
			this->freq=0;
		}

		ECA(std::bitset<8> rule, int cells, int gens, std::string t0){
			int i;
			std::string str("1");
			for(i=0; i<8; i++){
				this->rule[i]=rule[i];
			}
			this->cells=cells;
			this->gens=gens;
			this->freq=0;
			this->t0=(int*) malloc(cells*sizeof(int));
			for(i=0; i<(t0.size()); i++){
				if((str.compare(t0.substr(i, 1)))==0){
					this->t0[i]=1;	
				}
				else{
					this->t0[i]=0;		
				}
				
			}
		}

		int mod(int a){
			if(a>0){
				return a;
			}
			else{
				return (this->cells)+a;
			}	
		}

		int binToInt(int* bin){
			int num=0;
			for(int i=0; i<(this->cells); i++){
				if(bin[i]){
					num+=(int) pow(2.0, 0.0+i);
				}
			}
			return num;
		}

		void setRandomFirstGen(){
			this->t0=(int*) malloc(cells*sizeof(int));
			int dens=((this->den)*(this->cells))/100;
			int n, x, d=0;
			for(int i=0; i<(this->cells); i++){
				n=3214847 + (rand()%static_cast<int>(52178912397 - 3214847 + 1));
				x=n%2;
				if(x){
					this->t0[i]=1;
					this->freq+=1;
					d+=1;
				}
			}
			while(this->freq>dens){
				n=0+(rand()%static_cast<int>(((this->cells)-0)+1));
				//n=rand()%((this->cells)-1);
				if(t0[n]){
					t0[n]=0;
					this->freq-=1;
				}
			}
		}

		void setOneCellFirstGen(){
			this->t0=(int*) malloc(cells*sizeof(int));
			this->freq=1;
			int x=(this->cells)/2;
			for(int i=0; i<(this->cells); i++){
				if(i==x){
					this->t0[i]=1;
				}
				else{
					this->t0[i]=0;
				}
			}
		}

		void getNextGen(){
			this->t1=(int*) malloc(cells*sizeof(int));
			this->freq=0;
			int n;
			std::bitset<3> next;
			for(int i=0; i<(this->cells); i++){
				next[0]=(this->t0[mod(i-1)]);
				next[1]=(this->t0[i]);
				next[2]=(this->t0[mod(i+1)]);
				n=0;
				if(next.test(2)){
					n+=4;
				}
				if(next.test(1)){
					n+=2;
				}
				if(next.test(0)){
					n+=1;
				}
				if(this->rule.test(n)){
					freq+=1;
					this->t1[i]=1;
				}
				else{
					this->t1[i]=0;
				}
			}
			this->t0=this->t1;
		}

		void printGen(){
			for(int i=0; i<(this->cells); i++){
				if(this->t0[i]){
					std::cout << "*" << std::ends;
				}
				else{
					std::cout << " " << std::ends;		
				}
				
			}
			std::cout << "" << std::endl;
		}
};

#endif