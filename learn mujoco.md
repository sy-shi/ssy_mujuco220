https://mujoco.readthedocs.io/en/latest/overview.html

https://www.youtube.com/playlist?list=PLc7bpbeTIk758Ad3fkSywdxHWpBh9PM0G

## Goal

generate a basic environment with robot 

let it move 

## Learning process

#### Install

- Run commands in shell:

```shell
cd mujoco220
cd sample
make
```

issues with make (glfw)：https://github.com/deepmind/mujoco/issues/162

- Try to run a simulation

```shell
cd mujoco220
cd bin
simulate ../model/tendon_arm/arm26.xml
```



#### File structure

![image-20220621135610767](learn mujoco.assets/image-20220621135610767.png)

source codes

- head files

![image-20220621145758591](learn mujoco.assets/image-20220621145758591.png)



#### My project

template: https://pab47.github.io/mujoco.html

```makefile
COMMON=/O2 /MT /EHsc /arch:AVX /I../../include /Fe../../bin/
LIBS = ../../lib/glfw3dll.lib  ../../lib/mujoco.lib
CC = cl

ROOT = ballmove

all:
	$(CC) $(COMMON) main.cpp $(LIBS) -o ../../bin/$(ROOT)
	del *.obj

main.o:
	$(CC) $(COMMON) -c main.cpp

clean:
	rm *.o ../../bin/$(ROOT)
```

```bat
make
SET var=%cd%
cd ../../bin
ballmove
cd %var%
```

#### Source code

- Basic interactive operations

```c++
void keyboard();
void mouse_button();
void mouse_move();
void scroll();
```

- load model

```c++
char filename[] = "../my_project/ballmove/ball.xml";
mjModel* m = mj_loadXML(filename);  
mjData* d = mj_makeData(m);        // make data corresponding to model
```

- basic settings

```c++
mjvCamera cam;                      // abstract camera (e.g. your view)
mjvOption opt;                      // visualization options
mjvScene scn;                       // abstract scene
mjrContext con;                     // custom GPU context
```

- simulate

```c++
while(d->time<10)
{
	mjtNum simstart = d->time;
	while(d->time - simstart < 0.1)
		mj_step(m,d);
	mjv_updateScene(m, d, &opt, NULL, &cam, mjCAT_ALL, &scn);
    mjr_render(viewport, &scn, &con);	
}	
```

- free data

```c++
mj_deleteData(d);
mj_deleteModel(m);
mj_deactivate();
```

- control

```c++
void controller(const mjModel * m, mjData * d)
{
    generate_traj(m,d);
    d->ctrl[4] = traj[0];
    d->ctrl[6] = traj[1];
    d->ctrl[8] = traj[2];
    d->ctrl[10] = traj[3];
};
```



#### xml model

```xml
<mujoco model="car">
    <asset></asset>
    <option></option>
    <worldbody>
        <body>
            <geom></geom>
            <joint></joint>
        </body>
    </worldbody>
</mujoco>
```



## MuJoCo with Gym

#### install

```shell
(base)>conda create -n mujoco
(base)>conda activate mujoco
(mujoco)>pip install mujoco
(mujoco)>pip install gym[mujoco,robotics]
```

#### make environment in Gym 	

```python
class MultiCarEnv(mujoco_env.MujocoEnv):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self,model_path, ...)
        
    def step(self,action):
        self.do_simulation(action, ...)
        ob = self._get_obs()
        return ob, reward
    
    def reset_model(self):
        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos,qvel)
        return self._get_obs()
    
    def _get_obs(self):
        return np.concatenate([self.data.qpos, self.data.qvel])
    
    def viewer_setup(self):
        """
        optionally implement
        """
```

- register

```python
from gym.envs.registration import register
from MyEnvs.envs.MultiCarEnv import MultiCarEnv
register(
    id='MultiCar-v0',
    entry_point='MyEnvs.envs:MultiCarEnv',
    max_episode_steps=1000,
)
```

- setup package

```python
from setuptools import setup

setup(name='MyEnvs',
    version='0.0.1',
    install_requires=['gym>=0.23.1']
)
```

```shell
pip install -e MyEnvs
```



