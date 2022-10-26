import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 1,
    "distance": 4.0,
    "lookat": np.array((0.0, 0.0, 2.0)),
    "elevation": -20.0,
}

class MultiCarEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    """
    ### description
    Try to start a minimum gym RL environment based on MuJoCo engine
    """

    def __init__(self):
        utils.EzPickle.__init__(self)
        # the number is the frame to skip, a.k.a. define the dt
        # dt = model.opt.steptime * frame_skip
        mujoco_env.MujocoEnv.__init__(self, "D:\\mujoco220\\script\\car.xml", 5)


    def step(self, action):
        """
        ### Input
        the `action` here is a nparray which match the shape of mujoco `data.ctrl`
        ### Returns
        #### observation (object) 
        this will be an element of the environment's :attr:`observation_space`.
        This may, for instance, be a numpy array containing the positions and velocities of certain objects.
        #### reward (float)
        The amount of reward returned as a result of taking the action.
        #### done (bool)
        A boolean value for if the episode has ended, in which case further :meth:`step` calls will return undefined results.
        A done signal may be emitted for different reasons: Maybe the task underlying the environment was solved successfully,
        a certain timelimit was exceeded, or the physics simulation has entered an invalid state.
        #### info (dictionary)
        A dictionary that may contain additional information regarding the reason for a ``done`` signal.
        `info` contains auxiliary diagnostic information (helpful for debugging, learning, and logging).
        This might, for instance, contain: metrics that describe the agent's performance state, variables that are
        hidden from observations, information that distinguishes truncation and termination or individual reward terms
        that are combined to produce the total reward
        """ 

        self.do_simulation(action,self.frame_skip)
        reward = 1.0
        ob = self._get_obs()
        done = False
        info = {}
        return ob, reward, done, info

    
    def _get_obs(self):
        """
        return the state `qpos` and `qvel` as a one dimensional nparray
        """
        return  np.concatenate([self.data.qpos, self.data.qvel]).ravel()


    def reset_model(self):
        """
        Reset the robot degrees of freedom (qpos and qvel).
        Can also add noise to the initial states
        """
        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos,qvel)
        return self._get_obs()


    def viewer_setup(self):
        """
        This method is called when the viewer is initialized.
        Optionally implement this method, if you need to tinker with camera position and so forth.
        """
        # return super().viewer_setup()
        for key, value in DEFAULT_CAMERA_CONFIG.items():
            if isinstance(value, np.ndarray):
                getattr(self.viewer.cam, key)[:] = value
            else:
                setattr(self.viewer.cam, key, value)