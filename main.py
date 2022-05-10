from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0,exposure=4)
scene.set_floor(-0.94, (0.01,0.01,0.01))
scene.set_background_color((0.01,0.01,0.01))
scene.set_directional_light((1, 1, 1), 0.8, (0.5, 0.5, 0.5))

color1=vec3(160/255,84/255,5/255)
color2=vec3(160/255/5,84/255/5,5/255/5)

@ti.func
def createOctahedron(X,Yup,Ylow,Z,rotx=0,roty=0,rotz=0,pos=vec3(0,0,0),H=0,color=color1,vtype=1):
    R=0
    if H==0: R=max(X,Yup,Ylow,Z)
    else: R=max(X,abs(H),Z)
    matrot=rot3(vec3(1,0,0),radians(-rotx))@rot3(vec3(0,1,0),radians(-roty))@rot3(vec3(0,0,1),radians(-rotz))
    for x,y,z in ti.ndrange((-R+pos.x,R+1+pos.x),(-R+pos.y,R+1+pos.y),(-R+pos.z,R+1+pos.z)):
        coord=matrot@(vec3(x,y,z)-pos)
        xx,yy,zz=coord.xyz
        if yy>=0 and (H==0 or (H>0 and yy<=H)):
            if abs(xx)/X+abs(yy)/Yup+abs(zz)/Z<=1:
                scene.set_voxel(vec3(x, y, z), vtype, color)
        if yy<0 and (H==0 or (H<0 and yy>=H)):
            if abs(xx)/X+abs(yy)/Ylow+abs(zz)/Z<=1:
                scene.set_voxel(vec3(x, y, z), vtype, color)
@ti.func
def createPillar(X,H,rotx=0,roty=0,rotz=0,pos=vec3(0,0,0)):
    R=max(X,H)
    matrot=rot3(vec3(1,0,0),radians(-rotx))@rot3(vec3(0,1,0),radians(-roty))@rot3(vec3(0,0,1),radians(-rotz))
    for x,y,z in ti.ndrange((-R+pos.x,R+1+pos.x),(-R+pos.y,R+1+pos.y),(-R+pos.z,R+1+pos.z)):
        coord=matrot@(vec3(x,y,z)-pos)
        xx,yy,zz=coord.xyz
        if yy>=0 and yy<=H and abs(xx)+abs(zz)<=X:
            scene.set_voxel(vec3(x, y, z), 1, color1)
@ti.func
def remove(C,S):#center & scale
    for x,y,z in ti.ndrange((C.x-S.x,C.x+S.x),(C.y-S.y,C.y+S.y),(C.z-S.z,C.z+S.z)):
        scene.set_voxel(vec3(x, y, z), 0, vec3(0,0,0))
@ti.func
def drawLine(start,length,dir=1,vtype=1,color=color1):
    for i in range(length):
        if dir==1:scene.set_voxel(vec3(start.x+i, start.y+i+10, start.z-1), vtype, color) #左下-》右上 
        if dir==2:scene.set_voxel(vec3(start.x+i, start.y-i+10, start.z-1), vtype, color) #左上-》右下
        if dir==3:scene.set_voxel(vec3(start.x+i, start.y+10, start.z-1), vtype, color) #左-》右
        if dir==4:scene.set_voxel(vec3(start.x, start.y-i+10, start.z-1), vtype, color) #上-》下
        if dir==1:scene.set_voxel(vec3(start.x+i, start.y+i+10, start.z), 0, color) #左下-》右上 
        if dir==2:scene.set_voxel(vec3(start.x+i, start.y-i+10, start.z), 0, color) #左上-》右下
        if dir==3:scene.set_voxel(vec3(start.x+i, start.y+10, start.z), 0, color) #左-》右
        if dir==4:scene.set_voxel(vec3(start.x, start.y-i+10, start.z), 0, color) #上-》下

@ti.kernel
def initialize_voxels():

    createPillar(X=4,H=40,rotz=-135,pos=vec3(-28,10,0)) #左下
    createPillar(X=4,H=40,rotz=-45,pos=vec3(-28,10,0)) #左上
    createOctahedron(X=4,Yup=4,Ylow=1,Z=4,rotz=90,pos=vec3(-28,10,0)) #左中
    remove(C=vec3(0,34,0),S=vec3(6,8,8))
    remove(C=vec3(0,-14,0),S=vec3(6,8,8))
    createOctahedron(X=16,Yup=16,Ylow=16,Z=5,pos=vec3(0,10,0)) #中心
    remove(C=vec3(0,10,5),S=vec3(10,10,2))
    createOctahedron(X=5,Yup=8,Ylow=50,Z=5,rotx=15,rotz=-45,pos=vec3(32,12,10),H=10) #右下-大
    createOctahedron(X=5,Yup=8,Ylow=100,Z=5,rotx=15,rotz=-45,pos=vec3(32,12,10),H=-50) #右下-大
    createOctahedron(X=4,Yup=4,Ylow=16,Z=4,rotx=5,rotz=-60,pos=vec3(31,0,-3),H=10) #右下-小
    createOctahedron(X=4,Yup=4,Ylow=60,Z=4,rotx=5,rotz=-60,pos=vec3(31,0,-3),H=-35) #右下-小
    createOctahedron(X=8,Yup=13,Ylow=35,Z=6,rotx=22,rotz=32,pos=vec3(7,41,9),H=13) #右上-大
    createOctahedron(X=8,Yup=13,Ylow=70,Z=6,rotx=22,rotz=32,pos=vec3(7,41,9),H=-45) #右上-大
    createOctahedron(X=5,Yup=7,Ylow=25,Z=4,rotx=10,rotz=16,pos=vec3(15,35,-7),H=10) #右上-小
    createOctahedron(X=5,Yup=7,Ylow=50,Z=4,rotx=10,rotz=16,pos=vec3(15,35,-7),H=-30) #右上-小
    createOctahedron(X=3,Yup=6,Ylow=6,Z=2,pos=vec3(20,23,14),vtype=1,color=color1) #右前
    createOctahedron(X=5,Yup=9,Ylow=9,Z=4,pos=vec3(-17,22,-14),vtype=1,color=color1) #左后
    createOctahedron(X=3,Yup=6,Ylow=6,Z=2,rotz=35,pos=vec3(-5,-27,0)) #下1
    createOctahedron(X=4,Yup=9,Ylow=9,Z=5,rotx=-10,rotz=-15,pos=vec3(0,-37,0)) #下2
    createOctahedron(X=7,Yup=11,Ylow=11,Z=7,roty=30,pos=vec3(0,-60,0),H=9) #下3

    drawLine(start=vec3(0,7,2),length=7,dir=2,vtype=2)
    drawLine(start=vec3(-6,-1,2),length=7,dir=2,vtype=2)
    drawLine(start=vec3(1,5,2),length=6,dir=2,vtype=2)
    drawLine(start=vec3(-6,0,2),length=6,dir=2,vtype=2)
    drawLine(start=vec3(-4,3,2),length=4,dir=1,vtype=2)
    drawLine(start=vec3(1,-6,2),length=4,dir=1,vtype=2)
    drawLine(start=vec3(-1,2,2),length=3,dir=3,vtype=2)
    drawLine(start=vec3(-1,-2,2),length=3,dir=3,vtype=2)
    drawLine(start=vec3(-3,3,2),length=2,dir=1,vtype=2)
    drawLine(start=vec3(2,-4,2),length=2,dir=1,vtype=2)
    drawLine(start=vec3(-3,2,2),length=3,dir=2,vtype=2)
    drawLine(start=vec3(1,0,2),length=3,dir=2,vtype=2)
    drawLine(start=vec3(-2,-1,2),length=2,dir=3,vtype=2)
    drawLine(start=vec3(1,1,2),length=2,dir=3,vtype=2)
    drawLine(start=vec3(-5,1,2),length=2,dir=4,vtype=2)
    drawLine(start=vec3(5,0,2),length=2,dir=4,vtype=2)
    drawLine(start=vec3(3, -1, 2),length=1,dir=4,vtype=2)
    drawLine(start=vec3(4, 1, 2),length=1,dir=4,vtype=2)
    drawLine(start=vec3(-3, 1, 2),length=1,dir=4,vtype=2)
    drawLine(start=vec3(-4, -1, 2),length=1,dir=4,vtype=2)

initialize_voxels()
scene.finish()
