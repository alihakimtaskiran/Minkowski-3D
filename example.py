from MST3D import *
space_ship=Wordline("#F22", (0,0,0),(0,.4,2))
light=Wordline("#bf00ff",(0,0,0),(1,1,2**.5))
space=Entity()
space.add({space_ship, light})
space.view(True)
