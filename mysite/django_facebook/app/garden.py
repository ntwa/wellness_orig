#!/usr/bin/python
import PIL
from PIL import Image,ImageFont,ImageDraw
from random import randint
from sqlalchemy import create_engine,distinct,func
from sqlalchemy.orm import sessionmaker
from retrieve_intermediary import RetrieveIntermediary
from retrieve_activity_goal import RetrieveActivityGoal
from wellness.applogic.activity_module import PhysicalActivity,db,dbconn
from retrieve_points import RetrievePoints
from save_factors import ManageFactors
import os


import sys,json
import datetime


#Sort in descending order
def bubblesort( A ):
  
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k].totalpoints > A[k - 1].totalpoints ):
        swap( A, k, k - 1 )
  return A
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp


class BotanicalGarden:
    def __init__(self,i_id,b_id,folder_name):
        self.b_id=b_id
        self.i_id=i_id
        self.clickpoints=0
        self.stepspoints=0
        self.totalpoints=0
        self.trees=100
        self.flowers=68
        self.rank=1
        self.folder_name=folder_name
        self.file_name=""
        self.TreeFactor=float(0.0)
        self.FlowerFactor=float(0.0)
    
    def getSteps(self):
        
        
        try:
            varmyjson={'Day':'2000-01-01'}


            stepsPointsObj=RetrievePoints(varmyjson,self.i_id,0)
            ressteps=stepsPointsObj.getSteps(self.b_id)
            ressteps=json.loads(ressteps)

            stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
        
               
        except Exception as e:
            print e,", on function getSteps"
            stepspoints=0
        
                
        self.stepspoints=stepspoints
        print self.stepspoints,self.b_id 
                     
        
    def getIntermediaryPoints(self):
       
        try:
                
          
          varmyjson={'Day':'2012-01-01'}

          clickPointsObj=RetrievePoints(varmyjson,self.i_id,0)
          resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
          resclickpoints=json.loads(resclickpoints)

          clickpoints=int(resclickpoints["points"]/resclickpoints["dates_counter"])


          self.clickpoints=clickpoints


        except Exception as e:
          print e
          self.clickpoints=0
        
    

    def plantFlowers(self):
     
      highest_points=60.0
      try:
          
        path="/var/www/apps/static/django_facebook/images/garden/"
        filepathIm1="%sdesert_square.jpeg"%path
        filepathfreshIm1="%sdesert_square.jpeg"%path
        
        im1=Image.open(filepathIm1)
  
  
        #path="../static/django_facebook/images/garden/"
        filepathIm2="%sflower1_1.jpeg"%path  
        
        #path="../static/django_facebook/images/garden/"
     
        
        im2=Image.open(filepathIm2)        
        width, height =im1.size 
        width1,height1=im2.size
        
        
       
        highest_points=float(highest_points) 
        self.clickpoints=float(self.clickpoints)
        
        if self.clickpoints>highest_points:
          factor_ratio=1.0
        else:
          factor_ratio=float(self.clickpoints/highest_points)
        self.FlowerFactor=factor_ratio

        
        if factor_ratio==0.0:
            return im1
      
        
        
          
        

        width1=float(width1)
        height1=float(height1)
       
        
        #self.trees=self.trees*factor_ratio
        self.flowers=self.flowers*factor_ratio
        self.flowers=int(round(self.flowers,0))
        
        flower=self.flowers
        flower_width=width1*factor_ratio
        flower_height=height1*factor_ratio
        
        flower_width=int(round(flower_width,0))
        flower_height=int(round(flower_height,0))
        
        
        flower_variety=10*factor_ratio
        
                   
       
        
        flower_variety=int(round(flower_variety,0))
        
        if flower_variety==0:
            flower_variety=1
       

        if flower_width==0:
            flower_width=1
      
        if flower_height==0:
            flower_height=1        
        
    
        counter=0
        im2array=[]
  
        
  
        start_column_posn=120
  
        border=200
        column_width=int((border-start_column_posn)/4)
        end_column_posn=start_column_posn+column_width
        remaining_space=((border-start_column_posn)%4)
  
      
        
        #only four columns
        number_of_columns=4        
     
        
  
  
        
        #start_row_posn=50
        start_row_posn=40
        row_height=int(25*factor_ratio)

        if(row_height==0):
            row_height=1 
        number_of_rows=200-40
        number_of_rows=int(number_of_rows/row_height)
        
        end_row_posn=40+row_height
         
    
        
        divider=number_of_columns*number_of_rows
        if(divider==0):
            divider=1
  
        
      
  
  
        maximum_number_of_iterations=int(flower/divider)#this implies the number of trees that can be planted in each of four columns in each of the four rows rows
        remaining_flowers=int(flower%divider)        
        #if(maximum_number_of_iterations==0):
        #    maximum_number_of_iterations=1
  
  
        iteration=0
        #x1=randint(0,300)
        #y1=randint(50,150)
        if end_column_posn ==0 or end_row_posn==0:
            return im1
        
        x1=randint(start_column_posn,end_column_posn)
        y1=randint(start_row_posn,end_row_posn)
        
        #obj=PlotActivityGraph({"Day":"Last week"},8)
        
        width_end_marker=width1*factor_ratio # mark where the tree should end in x axis
        height_end_marker=height1*factor_ratio # mark where the tree should end in y axis
        
        #return im1
        #res=obj.getDataPoints()
        original_start_column_posn=start_column_posn
        original_end_column_posn=end_column_posn
        
        
        original_start_row_posn=start_row_posn
        original_end_row_posn=end_row_posn
  
        
  
             
        sentinal=50
        num=0
  
        
        samplefg=im2.crop((0,0,1,1))#get a default white back ground that needs to be replaced with a portion from image background
        pix=samplefg.load()
        r,g,b=pix[0,0]
        space=0
        prevnum=-1
        #trees=["tree0_1.jpeg","tree1_1.jpeg","tree2_1.jpeg","tree3_1.jpeg","tree4_1.jpeg","tree5_1.jpeg","tree6_1.jpeg","tree7_1.jpeg","tree8_1.jpeg","tree9_1.jpeg","tree10_1.jpeg","tree11_1.jpeg","tree12_1.jpeg","tree13_1.jpeg","tree14_1.jpeg","tree15_1.jpeg","tree16_1.jpeg","tree17_1.jpeg","tree18_1.jpeg","tree19_1.jpeg","tree20.jpeg","tree21_1.jpeg"]
        flowers=["flower1_1.jpeg","flower2_1.jpeg","flower3_1.jpeg","flower4_1.jpeg","flower5_1.jpeg","flower6_1.jpeg","flower7_1.jpeg","flower8_1.jpeg","flower9_1.jpeg","flower10_1.jpeg"]
      
        if flower_variety>1:
            num=randint(0, (flower_variety-1))
        else:
            num=0 
        flower=int(flower)# make sure the number of flower is an integer
        for_remaining_token_flag=0
        if(remaining_flowers>0):
            for_remaining_token_flag=1
        while counter<flower:
              
            if(maximum_number_of_iterations==iteration) and iteration>0:
                if for_remaining_token_flag == 1:
                    iteration=iteration-1#go one iteration back to plant one flower from a list of remaining flowers
                    for_remaining_token_flag=0
                    remaining_flowers=remaining_flowers-1
                    
                else:
                    
                    iteration=0
                    if remaining_flowers>0:
                        for_remaining_token_flag=1
                    #start_column_posn=start_column_posn+
                    #end_column_posn=end_column_posn+75
                    
                    #start_column_posn=start_column_posn+50
                    #end_column_posn=end_column_posn+50
                    
                    start_column_posn=start_column_posn+column_width
                    end_column_posn=end_column_posn+column_width                   
                    #print "(%s,%s)"%(start_column_posn,end_column_posn)
                    
                    if (start_column_posn==(column_width*3)):
                        end_column_posn=border
                        
                    #print "(%s,%s)"%(start_column_posn,end_column_posn)
                    if(start_column_posn>=border):
                        start_column_posn=original_start_column_posn
                        end_column_posn=original_end_column_posn
                        #start_row_posn=start_row_posn+25
                        start_row_posn=start_row_posn+row_height
                        
                        
                        #end_row_posn=end_row_posn+25
                        end_row_posn=end_row_posn+row_height
                    #else:
                    #    print " we are drawing in  between(%s,%s) and end at(%s,%s)"%(start_column_posn,start_row_posn,end_column_posn,end_row_posn)
                       
            elif (maximum_number_of_iterations==iteration) and iteration==0 and counter>0:
                start_column_posn=original_start_column_posn
                end_column_posn=border
                start_row_posn=original_start_row_posn
                end_row_posn=border
  
  
  
            #prevent flowers from the house
            if(counter>=1):                                        
                
                x1=randint(start_column_posn,end_column_posn)
                y1=randint(start_row_posn,end_row_posn)
  
  
                    
                
            
            #print "A  flower drawn at ",x1,y1," and our boundary is (%s,%s) and end at(%s,%s)"%(start_column_posn,start_row_posn,end_column_posn,end_row_posn)
  
            if maximum_number_of_iterations>0:
                
                iteration=iteration+1
            c1=x1
            c2=y1
            d1=c1+1
            d2=c2+1 
            x=c1
            y=c2    
            
            
            
            if flower_variety>1:
                num=randint(0, (flower_variety-1))            
                while(num==prevnum):
                    num=randint(0, (flower_variety-1))
                
            #prevnum=num    
            
        
  
            im2x=0
            im2y=0
            
            path="/var/www/apps/static/django_facebook/images/garden/"
            filepathIm2mod="%s%s"%(path,flowers[num]) 
            
            
  
              
                          
            prevnum=num              
            
            
            im2mod=Image.open(filepathIm2mod)
        
            #if (factor_ratio!=1):
            im2mod = im2mod.resize((flower_width,flower_height), PIL.Image.ANTIALIAS)
        
  
            while im2x<flower_width:#move one column
                while im2y<flower_height:#move through each row on the column    
                    box2=(im2x,im2y,(im2x+1),(im2y+1)) # for cropping the fore ground
                    box=(c1,c2,d1,d2)  # coordinate for each pixel box
                    croppedbg=im1.crop(box)
                    
                    croppedfg=im2mod.crop(box2)
                    pix2=croppedfg.load()
        
                    
                    
                        
                    r1,g1,b1=pix2[0,0]
                    
                    diff1=r-r1
                    diff2=g-g1
                    diff3=b-b1
                    
                    if(diff1<0):
                        diff1=diff1*(-1)
                    if(diff2<0):
                        diff2=diff2*(-1)
                    if(diff1<0):
                        diff1=diff1*(-1)    
                    if(diff1<0):
                        diff1=diff1*(-1)            
                    
                    
                
                    if((diff1<=20) and (diff2<=20) and (diff2<=20)):
                        #only replace white background on this image
                        im2mod.paste(croppedbg,(im2x,im2y))
                        pass
                        #replaced=croppedbg.load()
                    
            
                        
                    d2=d2+1
                    c2=c2+1
                    im2y=im2y+1
                    #box=(c1,c2,d1,d2)  # coordinate for each pixel box on the background image
                im2y=0
                #c2=49
                #c2=y1+(row*50)
                
                      
                #d2=0# start to row 0 in the next iteration
                #c1=d1
                
                
                #d1=c1+1
                
                
                #d2=c2+1
                
                
                c1=d1
                #c1=x1+(column*30)+1
                c2=y1               
                
                
                d1=c1+1
                
                
                d2=c2+1
                
                
         
                im2x=im2x+1 #for each foreground in the xaxis
            
            im2x=0# for each foreground
          
            im3mod=im2mod.crop((0,1,flower_width,flower_height))
            
            im1.paste(im3mod,(x,y))
   
            
            counter=counter+1
            im2mod=None   

        
        
      except Exception as e:
        print "Exception thrown inside plantFlowers: %s"%e
        
        
    
      return im1    
    
    
    
    
    
    
    def plantTrees(self,im1):
        
        max_points=100.0
        try:
          
          #im1.save("myfile7.jpeg")
          #obj=PlotActivityGraph({"Day":"Last week"},8)
          #print "----------------------------------------------------------"
          #res=obj.getDataPoints()
          #print res#im1=Image.open("desert_square.jpeg")
          path="/var/www/apps/static/django_facebook/images/garden/"
          filepathIm2="%stree1.jpeg"%path  
          
          #path="../static/django_facebook/images/garden/"
          filepathhouse="%shouse.jpeg"%path 
          
          
          im2=Image.open(filepathIm2)        
          width, height =im1.size 
          width1,height1=im2.size
          
  
         
          
         
            
          if self.stepspoints>max_points:
              factor_ratio=1.0
          else:

              factor_ratio=float(self.stepspoints/max_points)
          
          self.TreeFactor=factor_ratio
             
          if factor_ratio==0.0:
              return im1
          
          
           
          #print "steps=",self.steps
          #print "goal=",self.goal
          
          width1=float(width1)
          height1=float(height1)
         
          
          self.trees=float(self.trees*factor_ratio)
          self.trees=int(round(self.trees,0))
          
          
          tree=self.trees
          tree_width=width1*factor_ratio
          tree_height=height1*factor_ratio
          
          tree_width=int(round(tree_width,0))
          tree_height=int(round(tree_height,0))
          
          tree_variety=21*factor_ratio
          #flower_variety=10*factor_ratio
          
          tree_variety=int(round(tree_variety,0))
          #flower_variety=int(round(flower_variety,0))
          if(tree_variety==0):
            tree_variety==1
          #print "Tree variety=",tree_variety
          
          
          
          #print "Tree=",self.trees
          counter=0
          im2array=[]
          house=Image.open(filepathhouse)
          housex=width/2
          housey=(height/2)+25
  
          hsize = int((float(house.size[1])*float(0.8)))
          wsize =int((float(house.size[1])*float(0.8)))
          house = house.resize((wsize,hsize), PIL.Image.ANTIALIAS)        
          #print "House size=",wsize,hsize
          #print "start build=",housex,housey
          
          
          
          housec1=housex
          housec2=housey
          housed1=housec1+1
          housed2=housec2+1
          
          
          orighousec1=housec1
          orighousec2=housec2
          orighoused1=housed1
          orighoused2=housed2
          
  
          start_column_posn=0
          #column_width=int(tree_width)
          
  
          #end_column_posn=column_width
          #end_column_posn=140-int(column_width)# this ensure that no tree is drawn beyond 100
          centre=120
          border=centre-tree_width
          end_column_posn=int(border/4)# 
          remaining_space=border%4
          #print "Remainig Space,",remaining_space
          
          
          #column_width=int(tree_width)
          column_width=end_column_posn
          #print end_column_posn,column_width
  
          
          #number_of_columns=int(140/column_width)
          
          #only four columns
          number_of_columns=4        
          #number_of_columns=int((140/column_width)/4)
          #print "column width=",column_width
          #print "Number of columns,=", number_of_columns
  
          
          
          #start_row_posn=50
          start_row_posn=40
          row_height=int(25*factor_ratio)
          if row_height==0:
            row_height=1
         
          number_of_rows=200-40
          number_of_rows=int(number_of_rows/row_height)
          
          end_row_posn=40+row_height
          
      
          
          divider=number_of_columns*number_of_rows
          if(divider==0):
              divider=1
          #print "Divider,",divider
          #print "number of columns=",number_of_columns
          #print "number of rows=",number_of_rows
          #end_row_posn=60
  
          maximum_number_of_iterations=int(tree/divider)#this implies the number of trees that can be planted in each of four columns in each of the four rows rows
          remaining_trees=int(tree%divider)
          
          #print "maximum number of iteration=",maximum_number_of_iterations
          #print "remaining=",remaining_trees
          iteration=0
          #x1=randint(0,300)
          #y1=randint(50,150)
          if end_column_posn ==0 or end_row_posn==0:
              return im1

          x1=randint(start_column_posn,end_column_posn)
          y1=randint(start_row_posn,end_row_posn)
         
          #obj=PlotActivityGraph({"Day":"Last week"},8)
          
          width_end_marker=width1*factor_ratio # mark where the tree should end in x axis
          height_end_marker=height1*factor_ratio # mark where the tree should end in y axis
          
          #return im1
          #res=obj.getDataPoints()
          original_start_column_posn=start_column_posn
          original_end_column_posn=end_column_posn
          
          
          
  
          
          sentinal=50
          num=0
  
          
          samplefg=im2.crop((0,0,1,1))#get a default white back ground that needs to be replaced with a portion from image background
          pix=samplefg.load()
          r,g,b=pix[0,0]
          space=0
          prevnum=-1
          trees=["tree0_1.jpeg","tree1_1.jpeg","tree2_1.jpeg","tree3_1.jpeg","tree4_1.jpeg","tree5_1.jpeg","tree6_1.jpeg","tree7_1.jpeg","tree8_1.jpeg","tree9_1.jpeg","tree10_1.jpeg","tree11_1.jpeg","tree12_1.jpeg","tree13_1.jpeg","tree14_1.jpeg","tree15_1.jpeg","tree16_1.jpeg","tree17_1.jpeg","tree18_1.jpeg","tree19_1.jpeg","tree20.jpeg","tree21_1.jpeg"]
          #flowers=["flower1_1.jpeg","flower2_1.jpeg","flower3_1.jpeg","flower4_1.jpeg","flower5_1.jpeg","flower6_1.jpeg","flower7_1.jpeg","flower8_1.jpeg","flower9_1.jpeg","flower10_1.jpeg"]
        
          if tree_variety>1:
              num=randint(0, (tree_variety-1))
          else:
              num=0        
          
          tree=int(tree)# make sure the number of tree is an integer
          for_remaining_token_flag=0
          
          if(remaining_trees>0):
              for_remaining_token_flag=1
          while counter<tree:
                
              if(maximum_number_of_iterations==iteration) and iteration>0:
                  if for_remaining_token_flag == 1:
                      iteration=iteration-1#go one iteration back to plant one tree from a list of remaining trees
                      for_remaining_token_flag=0
                      remaining_trees=remaining_trees-1
                      
                  else:
                      
                      iteration=0
                      #if remaining_trees>0:
                      #    for_remaining_token_flag=1
                      #start_column_posn=start_column_posn+
                      #end_column_posn=end_column_posn+75
                      
                      #start_column_posn=start_column_posn+50
                      #end_column_posn=end_column_posn+50
                      
                      start_column_posn=start_column_posn+column_width
                      end_column_posn=end_column_posn+column_width                   
                      #print "(%s,%s)"%(start_column_posn,end_column_posn)
                      
                      if (start_column_posn==(column_width*3)):
                          end_column_posn=border
                          
                      #print "(%s,%s)"%(start_column_posn,end_column_posn)
                      if(start_column_posn>=border):
                          start_column_posn=original_start_column_posn
                          end_column_posn=original_end_column_posn
                          #start_row_posn=start_row_posn+25
                          start_row_posn=start_row_posn+row_height
                          
                          
                          #end_row_posn=end_row_posn+25
                          end_row_posn=end_row_posn+row_height
                  #else:
                  #    print " we are drawing in  between(%s,%s) and end at(%s,%s)"%(start_column_posn,start_row_posn,end_column_posn,end_row_posn)
                         
              elif (maximum_number_of_iterations==iteration) and iteration==0 and counter>0:
                #start_column_posn=0
                #end_column_posn=120
              #    if(counter%2==0):
              #    start_row_posn=start_row_posn+int(25*factor_ratio)
              #    end_row_posn=200
                start_column_posn=start_column_posn+column_width
                end_column_posn=end_column_posn+column_width                   
                      
                if(start_column_posn>=border):
                  
                  start_column_posn=original_start_column_posn
                  end_column_posn=original_end_column_posn
                      # start_row_posn=start_row_posn+25
                  start_row_posn=start_row_posn+row_height
                          
                  
                  end_row_posn=end_row_posn+25
                  #end_row_posn=end_row_posn+row_height
              #else:
                  #print "start new raw at (%s,%s)"%(start_row_posn,end_column_posn)
  
             
              #prevent trees from the house
              if(counter>=1):                                        
                  
                
                  #prevent tree from the location of the house
             
                  x1=randint(start_column_posn,end_column_posn)
                  y1=randint(start_row_posn,end_row_posn)
  
                  
                  #x1=randint(0,300)
                  #y1=randint(50,150)
                  tracker=0
                  #while((x1>=(orighousec1) and x1<=(orighousec1+40)) or ((x1+width_end_marker)>=(orighousec1) and (x1+width_end_marker)<=(orighousec1+40))) and ((y1>=(orighousec2) and y1<=(orighousec2+40)) or ((y1+height_end_marker)>=(orighousec1) and (y1+height_end_marker)<=(orighousec1+40))):
                      #x1=randint(0,300) 
                      #y1=randint(50,150)
                  #    x1=randint(start_column_posn,end_column_posn)
                  #    y1=randint(start_row_posn,end_row_posn)
                  #    tracker=tracker+1
                  #    if(tracker==50):
                  #        break
                      
                  
              
              #print "A  tree drawn at ",x1,y1," and our boundary is (%s,%s) and end at(%s,%s)"%(start_column_posn,start_row_posn,end_column_posn,end_row_posn)
              
              if maximum_number_of_iterations>0:
                  
                  iteration=iteration+1
              c1=x1
              c2=y1
              d1=c1+1
              d2=c2+1 
              x=c1
              y=c2    
              
              
             
                  
              if tree_variety>1:
                  num=randint(0, (tree_variety-1))
                  while(num==prevnum):
                      num=randint(0, (tree_variety-1))
            
              #prevnum=num    
              
          
   
              im2x=0
              im2y=0
              
              path="/var/www/apps/static/django_facebook/images/garden/"
              filepathIm2mod="%s%s"%(path,trees[num]) 
              
              
              #if(num==(tree_variety-1)):
              #    num=0
                  #num=randiAl-hajj F. Mohammednt(0, 21)
                  #while(num==prevnum):
                  #    num=randint(0, 21)                
                  
              #else:
              #    num=num+1
                
                            
              prevnum=num              
              
              
              im2mod=Image.open(filepathIm2mod)
          
              #if (factor_ratio!=1):
              im2mod = im2mod.resize((tree_width,tree_height), PIL.Image.ANTIALIAS)
          
              #num=num+1
              #if(num==21):
              #    num=0
              #width1=20
              #height1=20
              #while im2x<width1:#move one column
              #    while im2y<height1:#move through each row on the column
              while im2x<tree_width:#move one column
                  while im2y<tree_height:#move through each row on the column    
                      box2=(im2x,im2y,(im2x+1),(im2y+1)) # for cropping the fore ground
                      box=(c1,c2,d1,d2)  # coordinate for each pixel box
                      croppedbg=im1.crop(box)
                      
                      croppedfg=im2mod.crop(box2)
                      pix2=croppedfg.load()
          
                      
                      
                          
                      r1,g1,b1=pix2[0,0]
                      
                      diff1=r-r1
                      diff2=g-g1
                      diff3=b-b1
                      
                      if(diff1<0):
                          diff1=diff1*(-1)
                      if(diff2<0):
                          diff2=diff2*(-1)
                      if(diff1<0):
                          diff1=diff1*(-1)    
                      if(diff1<0):
                          diff1=diff1*(-1)            
                      
                      
                  
                      if((diff1<=20) and (diff2<=20) and (diff2<=20)):
                          #only replace white background on this image
                          im2mod.paste(croppedbg,(im2x,im2y))
                          pass
                          #replaced=croppedbg.load()
                      
              
                          
                      d2=d2+1
                      c2=c2+1
                      im2y=im2y+1
                      #box=(c1,c2,d1,d2)  # coordinate for each pixel box on the background image
                  im2y=0
                  #c2=49
                  #c2=y1+(row*50)
                  
                        
                  #d2=0# start to row 0 in the next iteration
                  #c1=d1
                  
                  
                  #d1=c1+1
                  
                  
                  #d2=c2+1
                  
                  
                  c1=d1
                  #c1=x1+(column*30)+1
                  c2=y1               
                  
                  
                  d1=c1+1
                  
                  
                  d2=c2+1
                  
                  
           
                  im2x=im2x+1 #for each foreground in the xaxis
              
              im2x=0# for each foreground
              #im3mod=im2mod.crop((0,1,50,50))
              #im3mod=im2mod.crop((0,1,20,20))
              im3mod=im2mod.crop((0,1,tree_width,tree_height))
              #im1.paste(im2mod,(x,y))
              im1.paste(im3mod,(x,y))
              #x=x+50
              #if counter==0:
              #im1.paste(house,(orighousec1,orighousec2))
              
              counter=counter+1
              im2mod=None
            
            
            
          #im1.paste(house,(orighousec1,orighousec2))
          #subimage3=im1.crop((0,0,width,300))
          #im0.paste(subimage3,(0,0))  
          
          
          
           #now build a house
          #self.drawHouse(orighousec1,orighousec2,im1,house)
          im2x=0
          im2y=0
          c1=orighousec1
          c2=orighousec2
          d1=c1+1
          d2=c2+1
          #box=(c1,c2,d1,d2)
          while im2x<width1:#move one column
              while im2y<height1:#move through each row on the column
                     
                  box2=(im2x,im2y,(im2x+1),(im2y+1)) # for cropping the fore ground
                  box=(c1,c2,d1,d2)  # coordinate for each pixel box on the background image
                  croppedbg=im1.crop(box)
                  
                  croppedhousebg=house.crop(box2)
                  pix2=croppedhousebg.load()
              
                  
                     
                      
                  r1,g1,b1=pix2[0,0]
                  
                  diff1=r-r1
                  diff2=g-g1
                  diff3=b-b1
                  
                  if(diff1<0):
                      diff1=diff1*(-1)
                  if(diff2<0):
                      diff2=diff2*(-1)
                  if(diff1<0):
                      diff1=diff1*(-1)    
                  if(diff1<0):
                      diff1=diff1*(-1)            
                  
                  
              
                  if((diff1<=20) and (diff2<=20) and (diff2<=20)):
                      #only replace white background on this image
                      house.paste(croppedbg,(im2x,im2y))
                      pass
                      #replaced=croppedbg.load()
                  
                      
                  d2=d2+1
                  c2=c2+1
                  im2y=im2y+1
      
              im2y=0
              c2=orighousec2
            
              
                    
              #d2=0# start to row 0 in the next iteration
              c1=d1
              
              d1=c1+1
              
              d2=c2+1
              
              im2x=im2x+1 #for each foreground in the xaxis

        except Exception as e:
          print "Exception was thrown in function plantTrees: %s"%e
      
      
         
           

        im1.paste(house,(orighousec1,orighousec2))
                
        return im1

    
    


myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
obj=RetrieveIntermediary(myjson)
result=obj.retrieveIntermediaryInDB()

intermediaries_tuple=json.loads(result)
intermediaries_emails=[]
orig_emails=[]
beneficiary_ids=[]
posn=0
gardens=[]
competitors_counter=0

try:
  for record in intermediaries_tuple.items():
      
      key,user =record
      
      if(user["D2"]=="None"):
          continue
      else:
          orig_emails.append(user["D1"]) #keep original email addresses
          orig_email=user["D1"]
          
          user["D1"]=user["D1"].replace("@","_at_")
          user["D1"]=user["D1"].replace(".","_dot_")
          folder_name=user["D1"]
          #intermediaries_emails.append(user["D1"])
          
          myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
          obj=RetrieveIntermediary(myjson)
          result2=obj.isAssignedBeneficiary()
          
          beneficiary_tuple=json.loads(result2)
          beneficiary_ids.append(beneficiary_tuple["Id"])
          posn=posn+1
          
          obj=BotanicalGarden(orig_email,beneficiary_tuple["Id"],folder_name)
          
          obj.getSteps()
          
          obj.getIntermediaryPoints()

          if obj.clickpoints>60:
              obj.clickpoints=60
          if obj.stepspoints>100:
              obj.stepspoints=100

          obj.totalpoints=obj.clickpoints+obj.stepspoints
          
           
          gardens.append(obj)
          
except Exception as e:
  print "An exception was thrown inside for record in intermediaries_tuple: %s"%e
        
bubblesort(gardens)




posn=0
total_goal_steps=0

date_today_int=datetime.date.today()
date_today_str ="%s"%date_today_int

garden_label=date_today_str.replace("-","_")
interm_points=[]
highest_points=1.0
#for email in intermediaries_emails:
for one_garden in gardens:
    
  #path="../static/django_facebookdjango_facebook/images/garden/"
  #filepathsave="%s%s.png"%(path,email)
  
  #intermediary_orig_email=intermediaries_emails[posn].replace("_at_","@")
  #intermediary_orig_email=intermediary_orig_email.replace("_dot_",".")    
  email=one_garden.folder_name
  
  path="/var/www/apps/static/django_facebook/images/garden/%s/"%email
  directory="/var/www/apps/static/django_facebook/images/garden/%s"%email
  
  if not os.path.exists(directory):
      os.makedirs(directory)      

  #filepathsave="%s%s.png"%(path,email)
  filename="%s_%s"%(one_garden.b_id,garden_label)
  one_garden.file_name=filename
  filepathsave="%s%s.jpeg"%(path,filename)
  
  #obj=BotanicalGarden(beneficiary_ids[posn])
  
  #obj.getSteps()
  #obj.getGoal()
  #points=obj.getIntermediaryPoints(orig_emails[posn])
  #interm_points.append(points)
  
 
  
  #garden=obj.plantFlowers()
 # print "Start printing Flowers"
  garden=one_garden.plantFlowers()
 #print "Done printing Flowers"
  #completegarden=obj.plantTrees(garden)
  completegarden=one_garden.plantTrees(garden)
  #myjson={"FactorId":one_garden.file_name,"TreeFactor":one_garden.TreeFactor,"FlowerFactor":one_garden.FlowerFactor}
  #forestFactorObj=ManageFactors(myjson)
  #forestFactorObj.saveFactorsInDB()

  #print filepathsave 
  completegarden.save(filepathsave,"JPEG", quality=80)    
  posn=posn+1
 

sys.exit(1)   
myjson={'Day':'Today'}
obj=RetrievePoints(myjson,'katulentwa@gmail.com')
result=obj.retrieveScoreGardensUrls()
print result

