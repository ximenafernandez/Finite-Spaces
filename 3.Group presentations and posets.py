#Poset associated to a group presentation

def presentation_poset(gens,rels):
   
   #expanded relations
    Rels=[]
    for i in range(len(rels)):
        Rels.append([])
        for l in rels[i]:
            if l[1]<0:
                Rels[i]=Rels[i]+[(l[0],-1) for k in range(abs(l[1]))]
            if l[1]>0:
                Rels[i]=Rels[i]+[(l[0],1) for k in range(abs(l[1]))]
    
    #V is the set of elements of the presentation poset
    V=range(len(rels)+1)+[x+str(i) for x in gens for i in range(1,4)]
    
    #E is the list of cover relations of the presentaton poset
    E=[]
    #edges associated to the generators
    for x in gens:
        E=E+[[0,x+'2'],[0,x+'3'],[x+'1',x+'2'],[x+'1',x+'3']]
    
    for i in range(len(Rels)):
        
        letters={}
        for x in gens: letters[x]=0
        for j in range(len(Rels[i])):
            letters[Rels[i][j][0]]=letters[Rels[i][j][0]]+abs(Rels[i][j][1])
        total_letters=sum([letters[x] for x in gens])
        
        V=V+['c'+str(i+1)+'_'+x+str(j)+'_'+str(k) for x in gens if letters[x]!=0 for j in range(1,4) for k in range(1,letras[x]+1)]+ ['c'+str(i+1)+'_0_'+str(k) for k in range(1,total_letters+1)]
        
        #the model of D^2 i associated to the cell corresponding to the relator i:
        
        #edges between the indicator i of the relator and the minimals of the cycle
        
        E=E+[[i+1, 'c'+str(i+1)+'_0_'+str(j+1)] for j in range(total_letters)]+[[i+1,'c'+str(i+1)+ '_'+x+'1'+'_'+str(j+1)] for x in gens for j in range(letters[x])]

        # edges between the models of S^1 associated to generators and relators
        
        for x in gens:
            for k in range(1,4):
                for j in range(letters[x]):
                    E.append([x+str(k), 'c'+str(i+1)+'_'+x+str(k)+'_'+str(j+1)])
        
        for j in range(len(Rels[i])):
            E.append([0,'c'+str(i+1)+'_'+'0'+'_'+str(j+1)])
        
        	#edges of the cycle which do not start in 0
        for l in Rels[i]:
            for j in range(letters[l[0]]):
                E=E+[['c'+ str(i+1)+ '_'+l[0]+'1_'+str(j+1),'c'+ str(i+1)+ '_'+l[0]+'2_'+str(j+1)],['c'+ str(i+1)+ '_'+l[0]+'1_'+str(j+1),'c'+ str(i+1)+ '_'+l[0]+'3_'+str(j+1)]]
        
        	#edges of the cycle starting in 0 
        cont={}
        for x in gens: cont[x]=0
        
        for j in range(len(Rels[i])):
            cont[Rels[i][j][0]]=cont[Rels[i][j][0]]+1
            
            #edges to the 'right'
            if Rels[i][j][1]>0:
                E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+ str(i+1)+'_'+str(Rels[i][j][0])+'2_'+str(cont[Rels[i][j][0]])])
            else:
                E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+ str(i+1)+'_'+str(Rels[i][j][0])+'3_'+str(cont[Rels[i][j][0]])])
        
            #edges to the 'left' 
            if j!=0:
                if Rels[i][j-1][0]==Rels[i][j][0]:
                    if Rels[i][j-1][1]>0:
                        E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'3'+'_'+str(cont[Rels[i][j-1][0]]-1)])   
                    else:
                        E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'2'+'_'+str(cont[Rels[i][j-1][0]]-1) ]) 
                else:
                    if Rels[i][j-1][1]>0:
                        E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'3'+'_'+str(cont[Rels[i][j-1][0]])])   
                    else:
                        E.append(['c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'2'+'_'+str(cont[Rels[i][j-1][0]]) ]) 
        
        #j=0
        n=len(Rels[i])-1  
        if Rels[i][n][1]>0:
            E.append(['c'+str(i+1)+'_0_1', 'c'+str(i+1)+'_'+ str(Rels[i][n][0]) + '3'+ '_'+str( cont[Rels[i][n][0]])])
        else:
            E.append(['c'+str(i+1)+'_0_1', 'c'+str(i+1)+ '_'+str(Rels[i][n][0]) + '2'+ '_'+str( cont[Rels[i][n][0]])])
    return Poset((V,E))


#incidende of the cells in presentation poset

def incidence(gens,rels):
    d={} #dictionary of incidences
    
    #expanded relations of the presentation
    Rels=[]
    for i in range(len(rels)):
        Rels.append([])
        for l in rels[i]:
            if l[1]<0:
                Rels[i]=Rels[i]+[(l[0],-1) for k in range(abs(l[1]))]
            if l[1]>0:
                Rels[i]=Rels[i]+[(l[0],1) for k in range(abs(l[1]))]
    
    #incidence of the edges associated to generators
    for x in gens:
        d[(0,x+'2')]=-1
        d[(0,x+'3')]=1
        d[(x+'1',x+'2')]=1
        d[(x+'1',x+'3')]=-1
    
    
    for i in range(len(Rels)):
       
    #incidence of edges between generatos and relators
        
        #x2,x3
        letters={}
        for x in gens: letters[x]=0
        for j in range(len(Rels[i])):
            letters[Rels[i][j][0]]=letters[Rels[i][j][0]]+1
            for k in [2,3]:
                if Rels[i][j][1]>0:
                    d[(Rels[i][j][0]+str(k),'c'+str(i+1)+'_'+Rels[i][j][0]+str(k)+'_'+str(letters[Rels[i][j][0]]) )]=1
                if Rels[i][j][1]<0:
                    d[(Rels[i][j][0]+str(k),'c'+str(i+1)+'_'+Rels[i][j][0]+str(k)+'_'+str(letters[Rels[i][j][0]]) )]=-1
        
        #x1
        for x in gens:
            for j in range(letters[x]):
                d[(x+'1','c'+str(i+1)+'_'+x+'1'+'_'+str(j+1))]=1
        #0
        for j in range(len(Rels[i])):
            d[(0,'c'+str(i+1)+'_'+'0'+'_'+str(j+1))]=1
        
        total_letters=sum([letters[x] for x in gens])
           
        #incidence of edges between the indicator of the cycle and its minimals 
        for j in range(total_letters):
            d[(i+1, 'c'+str(i+1)+'_0_'+str(j+1))]=-1
        for x in gens:
            for j in range(letters[x]):
                d[(i+1,'c'+str(i+1)+ '_'+x+'1'+'_'+str(j+1))]=-1
                        
        #incidence of the edges that do not start in 0
        
        letters={}
        for x in gens: letters[x]=0
        for j in range (len(Rels[i])):
            letters[Rels[i][j][0]]=letters[Rels[i][j][0]]+1
            if Rels[i][j][1]>0:
                d[('c'+ str(i+1)+ '_'+Rels[i][j][0]+'1_'+str(letters[Rels[i][j][0]]),'c'+ str(i+1)+ '_'+Rels[i][j][0]+'3_'+str(letters[Rels[i][j][0]]))]=1
                d[('c'+ str(i+1)+ '_'+Rels[i][j][0]+'1_'+str(letters[Rels[i][j][0]]),'c'+ str(i+1)+ '_'+Rels[i][j][0]+'2_'+str(letters[Rels[i][j][0]]))]=-1
                
            else:
                d[('c'+ str(i+1)+ '_'+Rels[i][j][0]+'1_'+str(letters[Rels[i][j][0]]),'c'+ str(i+1)+ '_'+Rels[i][j][0]+'2_'+str(letters[Rels[i][j][0]]))]=1
                d[('c'+ str(i+1)+ '_'+Rels[i][j][0]+'1_'+str(letters[Rels[i][j][0]]),'c'+ str(i+1)+ '_'+Rels[i][j][0]+'3_'+str(letters[Rels[i][j][0]]))]=-1
        
        
        #incidence of the edges starting in 0
         
        cont={}
        for x in gens: cont[x]=0
        
        for j in range(len(Rels[i])):
            cont[Rels[i][j][0]]=cont[Rels[i][j][0]]+1
            
            #edges to the 'right'
            
            if Rels[i][j][1]>0:
                d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+ str(i+1)+'_'+str(Rels[i][j][0])+'2_'+str(cont[Rels[i][j][0]]))]=1

            else:
                d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+ str(i+1)+'_'+str(Rels[i][j][0])+'3_'+str(cont[Rels[i][j][0]]))]=1

        
            #edges to the 'left' 
            
            if j!=0:
                
                if Rels[i][j-1][0]==Rels[i][j][0]:
                    if Rels[i][j-1][1]>0:
                        d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'3'+'_'+str(cont[Rels[i][j-1][0]]-1))]=-1
                        
                    else:
                        d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'2'+'_'+str(cont[Rels[i][j-1][0]]-1))]=-1
                else:
                    if Rels[i][j-1][1]>0:
                        d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'3'+'_'+str(cont[Rels[i][j-1][0]]))]=-1
                    else:
                        d[('c'+str(i+1)+'_0_'+str(sum([cont[x] for x in gens])), 'c'+str(i+1)+'_'+str(Rels[i][j-1][0])+'2'+'_'+str(cont[Rels[i][j-1][0]]) )]=-1
        
        #j=0
        n=len(Rels[i])-1  
        if Rels[i][n][1]>0:
            d[('c'+str(i+1)+'_0_1', 'c'+str(i+1)+'_'+ str(Rels[i][n][0]) + '3'+ '_'+str( cont[Rels[i][n][0]]))]=-1
        else:
            d[('c'+str(i+1)+'_0_1', 'c'+str(i+1)+ '_'+str(Rels[i][n][0]) + '2'+ '_'+str( cont[Rels[i][n][0]]))]=-1
         
        
    return d

