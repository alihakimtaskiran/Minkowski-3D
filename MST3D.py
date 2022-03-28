import open3d as o3d
import numpy as np
print("Get ready! Tachyon Era coming soon ")

class Wordline(object):
    def __init__(self, RGB, start, end):
        
        if not type(RGB)==str:
            raise TypeError("RGB is a string 3 or 6-digits of hexadecimal number")
        
        
        if type(start) not in {list, tuple}:
            raise TypeError("Starting point must be a tuple or list ")
        
        if type(end) not in {list, tuple}:
            raise TypeError("Ending point must be a tuple or list ")
        
        if not len(start)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
            
        if not len(end)==3:
            raise ValueError("The entity is defined to be had 1 temporal and 2 spatial dimension")
            
        RGB=RGB.strip("#")
        if len(RGB)==6:
            self.color=[int(RGB[2*i:2*i+2],16)/255 for i in range(3)]
        
        elif len(RGB)==3:
            self.color=[int(RGB[i],16)/15 for i in range(3)]
            
        self.delta=(end[0]-start[0], end[1]-start[1], end[2]-start[2])
        self.io=(start,end)
        


class Entity(object):
    def __init__(self):
        
        self.ply=o3d.geometry.PointCloud()
        self.__dots=np.array(((0,0,0),))
        self.__colors=np.array(((0,0,0),))
        self.__max_scalar=0
        
    def __dp(self, p1, p2):#dot_product
        return p1[0]**p2[0]+p1[1]**p2[1]-p1[2]**p2[2]
    
    def add(self,content):
        if type(content)==Wordline:
            for i in range(2):
                for j in range(3):
                    if content.io[i][j]>self.__max_scalar:
                        self.__max_scalar=content.io[i][j]
            self.__colors=np.concatenate((self.__colors,np.array((content.color,)*1000)),0)
            ds=tuple([content.delta[i]/1000 for i in range(3)])
            path=np.zeros((1000,3))
            for i in range(1000):
                for j in range(3):
                    path[i][j]=content.io[0][j]+ds[j]*i
            self.__dots=np.concatenate((self.__dots, path),0)
            
    def render(self):
        _=self.__max_scalar*1.25
        __=self.__max_scalar/800
        ___=__*1000
        ____=_/2
        self.__dots=np.concatenate((self.__dots, np.array([(__*i, 0, 0) for i in range(-1000,1000)]+[(0,__*i, 0) for i in range(-1000,1000)]+[(0, 0, __*i) for i in range(0,1000)])),0)
        self.__dots=np.concatenate((self.__dots, np.array([(_*np.cos(i*.006283185),_*np.sin(i*.006283185),_) for i in range(1000)])),0)
        self.__dots=np.concatenate((self.__dots, np.array([(____*np.cos(i*.006283185),____*np.sin(i*.006283185),____) for i in range(1000)])),0)
        self.__dots=np.concatenate((self.__dots, np.array([(0, i*__, i*__) for i in range(1000)]+[(i*__,0, i*__) for i in range(1000)]+[(i*__,0,___) for i in range(1000)]+[(0, i*__, ___) for i in range(1000)])),0)
        
        self.__colors=np.concatenate((self.__colors,np.array(((0,0,0),)*11000)),0)
        
        self.ply.points=o3d.utility.Vector3dVector(self.__dots)
        self.ply.colors=o3d.utility.Vector3dVector(self.__colors)
        
    def view(self,render=True):
        if render:
            self.render()
        o3d.visualization.draw_geometries([self.ply])
        
    def entity(self, render=True):
        if render:
            self.render()
        return self.ply
