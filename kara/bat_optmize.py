import networkx as nx
import numpy as np
from collections import Counter, defaultdict
import time
#from sklearn import metrics
from sklearn.metrics import normalized_mutual_info_score as NMI
import operator
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import random

class Bats:
	def __init__(self):
		self.bats_fitness_value=[]
		self.bats_fitness_values={}
		#self.best_positions = []
		self.best_p = []
		self.global_best=[]
		self.pos_modularity = 0
		self.velocity = []
		self.G = nx.Graph()
		self.bats = []
		self.file_name = 'kara.txt'
		self.synthetic = 'karateLabel.txt'
		self.pred={}		
		self.number_of_bats = 100
		self.modularity = 0
		self.iteration = 100
		self.R=0.5
		self.A=0.5

	def Input_Graph(self):
		temp=open(self.file_name,'r').read().split('\n')
		graph=[]
		for i in temp:
			t=[]
			for j in i.split():
				if(j):
					t.append(int(j))
			if(t):
				graph.append(tuple(t))
		self.G.add_edges_from(graph)
		j=1
		for i in self.G:
			self.G.node[i]={'pos':j}
			j+=1

		"""temp=open(self.synthetic,'r').read().split('\n')	
		for i in temp:
			m=[]
			for j in i.split():
				if(j):
					m.append(int(j))
			if(m):
				self.pred.update({m[0]:m[1]})"""



	def updatepos(self,graph):    #simple function to update position with base on thier neighbors frequency
		j=0
		#self.new=graph.copy()
		for i in graph:
			n=[]
			if(self.velocity[j]):
				temp=graph.neighbors(i)
				for k in temp:
					n.append(graph.node[k]['pos'])
					#print(n)
				if(len(n)!=len(set(n))):
					p=Counter(n).most_common(1)[0][0]
					graph.node[i]['pos']=p
				else:
					if(graph.node[i]['pos'] in n):
						pass
					else:
						p=np.random.choice(n)
						graph.node[i]['pos']=p
			j+=1
		return graph.copy()

	def updatevelocity(self,graph):
		fmin=0
		fmax=1
		v1=[]
		v2=[]
		v3=[]
		j=0
		p=self.best_positions
		#print('bf',self.best_positions)
		for i in graph:
			beta=round(np.random.uniform(0,1),2)
			f=fmin+(fmax-fmin)*beta
			v1.append(int((p[j]==graph.node[i]['pos']) and '0' or '1'))
			#bf=self.best_positions[j]
			#print('bf',self.best_positions[j])
			#print(self.best_positions[j])
			v2.append((self.velocity[j]+v1[j]*f))
			
			v3.append(1/(1+np.exp(-(v2[j]))))
			#print('af',self.best_positions[j])
			#print('bf',self.velocity)
			self.velocity[j]=int((round(np.random.uniform(0,1),2)<v3[j]) and '1' or '0')
			#print('Af',self.velocity)
			#af=self.best_positions[j]
			#print(bf==af)
			#if(round(np.random.uniform(0,1),2)< v3[j]):
			#	self.velocity[j]=1
			#else:
			#	self.velocity[j]=0
			j+=1
			
			#print('l',self.best_positions)
		#print('af',self.best_positions)	


	def bats_init(self): #based on random neighborhood
		#a=self.G.nodes()
		#l=np.random.randint(1,self.G.number_of_nodes(),self.G.number_of_nodes()).tolist()
		#self.newposition=l
		#self.best_positions=l
		copy=self.G.copy()
		for j in range(self.number_of_bats):
			for i in copy:
				n=[]
				temp=copy.neighbors(i)
				for k in temp:
					n.append(copy.node[k]['pos'])
				if(len(n)!=len(set(n))):
						p=Counter(n).most_common(1)[0][0]
						self.G.node[i]['pos']=p
				else:
						p=np.random.choice(n)
						self.G.node[i]['pos']=p
				#print(self.G.node[i]['pos'])
                                #t1=[]
				#t1.append(self.G.node[i]['pos'])
				#self.best_positions=t1
			#print('\n')
			self.bats.append(self.G.copy())
			#print(self.best_positions)
		
	def fitness(self,graph):
		m=graph.number_of_edges()
		l=1/(2*m)
		temp=0
		for j in graph:	
			for i in graph:
				A=int(i in graph.neighbors(j))
				k1=len(list(graph.neighbors(j)))
				k2=len(list(graph.neighbors(i)))
				gama=int(graph.node[j]['pos']==graph.node[i]['pos'])
				temp+=((A-(k1*k2)/(2*m))*gama)
			
		mod=temp*l
		return np.round(mod,4)
	def rearrange(self,graph):
		pos=[]
		node=list(graph.nodes())
		for i in graph:
			pos.append(graph.node[i]['pos'])
		new_pos=[]
		single=list(set(pos))
		for i in single:
			if(i in node):
				list(node).remove(i)
				#print(node)
				f=True
			else:
				f=False	
			num=np.random.choice(node)
			new_pos.append(num)
			node.remove(num)
			if(f is True):
				node.append(i)
		for i in graph:
			t=graph.node[i]['pos']
			d=single.index(t)
			graph.node[i]['pos']=new_pos[d]
			#print(graph.node[i]['pos'])
		return graph.copy()			


	def eq_4(self):
		new_graph=self.G.copy()           
		k=0
		av=np.mean(self.A)
		av1=round(av,2)
		for i in new_graph:
			e=round(np.random.uniform(0,1),2)
			if(e>av1):
                
				#new_graph.node[i]['pos']=self.best_positions[k]+np.mean(self.A)*e
				
				neighbor=new_graph.neighbors(i)
				temp=np.array(list(neighbor))
				#new_graph[i]['pos']=self.best_positions[k]+np.random.choice(neighbor)
				new_graph[i]['pos']=np.random.choice(temp)
			else:
				new_graph[i]['pos']=self.best_positions[k]
#			if(c>np.mean(self.A))
			k+=1
		return new_graph.copy()
		



	def increase_r(self,itr):
		#if(itr==0):
		r0=0.5
		#else:
		#1	r0=self.R
		gama=0.03
		x=round(float(1-round(np.exp(-gama*itr),2)),2)
		x1=r0*x
		x2=round(float(x1),2)
		self.R=x2
		

	def decrease_a(self):
		alpha=0.98
		a=self.A * alpha
		a1=round(float(a),2)
		self.A=a1

	def best_bats(self):
		fit=-1
		for i in self.bats:
			t=self.fitness(i)
			self.bats_fitness_value.append(t)
			self.best_p.append([i.node[j]['pos'] for j in i])
			#self.bats_fitness_values.update{t:[i.node[j]['pos'] for j in i]}
			if(t>fit):
				fit=t
				#print(i.node)
				self.best_positions = [i.node[j]['pos'] for j in i]

	
	
	def optimize(self):
		it=0
		tm=[]
		md=[]
		nmi=[]
		ittr=[]
		com=[]	
		for itr in range(10):			
			self.__init__()
			startTime = time.time()
			
			self.Input_Graph()
			print('h')
			self.bats_init()
			#for i in self.bats:
			#	print(i.node)
			t=self.G.number_of_nodes()
			vel=[]
			for ll in range(t):
				vel.append(0)

			self.velocity=vel
			#print(self.velocity)
			#self.best_positions=vel;
			#self.best_p=vel
			#print('bf',self.velocity)
			self.best_bats()
			
			#print(self.velocity)
			#print(self.best_positions)
			#print('af',self.velocity)
			print("iteration : ",(itr+1))
			for i in range(self.iteration):
				#print('af',self.velocity)
				#print("Iteration : %d"%(i+1),end='\r')
				#print("iteration : ",(i+1))
				inc=0
				#print('itr',i)
				for p in self.bats:
					#self.velocity=vel
					#print(p.node)
					#print('bf',self.best_positions)
					
					self.updatevelocity(p)
					#print('af',self.best_positions)
					t1=self.updatepos(p)
					
					y=self.rearrange(t1)

					if(round(np.random.uniform(0,1),2)>self.R):
						#t2=self.eq_4()
						#y=self.rearrange(t2)
						y=self.eq_4()
					
					rd=round(np.random.uniform(0,1),2)
					fnew=self.fitness(y)
					
					fi=self.bats_fitness_value[inc]
					bp=[]
					if(rd<self.A and fi<fnew):
						#print("p ",p.node)
						#print("y ",y.node)
						p=y.copy()					
						self.bats_fitness_value[inc] = fnew
						#self.best_p = 
						#self.bats.bats_fitness_values[(self.bats_fitness_values.keys())[inc]]=fnew
						it=i	
						self.best_positions = [y.node[nd]['pos'] for nd in y]
						self.best_p[inc] = [y.node[nd]['pos'] for nd in y] # this is an array of positions
						#self.best_p[inc] = []

						#if (self.pos_modularity<fnew):   # here comparison with old fitness if good then position vector and 
						#	self.pos_modularity=fnew     # modularity is update
							#fit = self.fitness(y)
							#print()
						#	self.best_p = [y.node[nd]['pos'] for nd in y]
							#print(self.best_p)

						#print(self.best_positions)
						#print("communites : ",len(set(self.best_positions)))
						#print(self.best_positions)
						self.increase_r(i)
						self.decrease_a()
					inc+=1
	                        
				fmax=max(self.bats_fitness_value)
				#print(' max ',self.pos_modularity)
				#print(self.best_p)
				#fmax=max(self.bats_fitness_values.keys())
				#print(self.bats_fitness_value)
				#print(self.best_positions)
				pos=self.best_p[self.bats_fitness_value.index(fmax)] 
				self.positions=pos
				#print("communites : ",len(set(pos)))
				#print("Position : ",self.best_positions)
				
			print(fmax)
			#n=NMI(list(self.pred.values()),pos)
			tm.append(float(format(np.round((time.time() - startTime),2))))
			md.append(fmax)
			#nmi.append(n)
			#ittr.append(it)
			com.append(len(set(pos)))
			fig = plt.figure()
			plt.draw()
			nx.draw(self.G, node_color=pos)
			plt.savefig('newnetscience_'+str(itr+1)+'_.png')
		print("\n\n**********************************************************")	
		print('\nThe script take {0} second ',tm)
		print("\nModularity is : ",md)
		#print("\nNMI : ",nmi)			
		print("\nNumber of Communites : ",com)
			#print("\nGlobal Best Position : ",pos)
		#nx.draw(self.G,node_color=[self.G.node[i]['pos'] for i in self.G])
		#fig = plt.figure()
		#plt.draw()
		#nx.draw(self.G, node_color=pos)
		#plt.savefig()
		#plt.show()
		
if __name__=='__main__':
    
	f=Bats()
	f.optimize()
