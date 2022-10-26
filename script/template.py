import mujoco as mj
import glfw
from threading import Lock

class multi_car:
    def __init__(self,model_path):
        self.model = mj.MjModel.from_xml_path(model_path)
        self.data = mj.MjData(self.model)

        mj.mjcb_control = self.controller

        glfw.init()
        self.width, self.height = glfw.get_video_mode(glfw.get_primary_monitor()).size
        self.window = glfw.create_window(self.width // 2, self.height // 2, "sim", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        
        # visualize and render variables
        self.scene = mj.MjvScene(self.model, maxgeom=1000)
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150)
        self.option = mj.MjvOption()
        self.camera = mj.MjvCamera()
        self.perturb = mj.MjvPerturb()

        # interactive variables
        # self.action = mj.mjtMouse(0)     # for mouse action definition
        self.gui_lock = Lock()
        self.button_left_pressed = False
        self.button_right_pressed = False
        self.button_middle_pressed = False
        self.lastx = 0
        self.lasty = 0

        # GLFW interactive settings
        glfw.set_scroll_callback(self.window, self.scroll)
        glfw.set_cursor_pos_callback(self.window, self.mouse_move)
        glfw.set_mouse_button_callback(self.window, self.mouse_button)

    
    def scroll(self,window,xoffset,yoffset):
        mj.mjv_moveCamera(self.model,mj.mjtMouse.mjMOUSE_ZOOM,0,-0.05*yoffset,self.scene,self.camera)
        return

    
    def mouse_button(self,window, button, act, mods):
        self.button_left_pressed = (
            glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        )
        self.button_right_pressed = (
            glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS
        )
        self.button_mid_pressed = (
            glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS
        )

        self.lastx, self.lasty = glfw.get_cursor_pos(window)
        return

    
    def mouse_move(self, window, xpos, ypos):
        if not (self.button_left_pressed or self.button_right_pressed):
            return
        mod_shift = (
            glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
            or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
        )
        if self.button_right_pressed:
            action = (
            mj.mjtMouse.mjMOUSE_MOVE_H
            if mod_shift
            else mj.mjtMouse.mjMOUSE_MOVE_V
            )
        elif self.button_left_pressed:
            action = (
            mj.mjtMouse.mjMOUSE_ROTATE_H
            if mod_shift
            else mj.mjtMouse.mjMOUSE_ROTATE_V
            )
        else:
            action = mj.mjtMouse.mjMOUSE_ZOOM

        dx = int(xpos - self.lastx)
        dy = int(ypos - self.lasty)
        self.lastx = xpos
        self.lasty = ypos
        width,height = glfw.get_window_size(window)
        with self.gui_lock:
            mj.mjv_moveCamera(self.model,action,dx/height,dy/height,self.scene,self.camera)
        return

    
    def controller(self):
        t = self.data.time
        self.data.ctrl[4] = 2 * t
        self.data.ctrl[6] = - 2 * t
        self.data.ctrl[8] = - 2 * t
        self.data.ctrl[10] = 2 * t

    def simulate(self):
        while not glfw.window_should_close(self.window):
            starttime = self.data.time
            while self.data.time-starttime<1/60:
                mj.mj_step1(self.model,self.data)
                self.controller()
                mj.mj_step2(self.model,self.data)

            viewport = mj.MjrRect(0, 0, 0, 0)
            viewport.width, viewport.height = glfw.get_framebuffer_size(self.window)
            mj.mjv_updateScene(self.model,self.data,
                self.option,self.perturb,self.camera,
                mj.mjtCatBit.mjCAT_ALL,self.scene)
            mj.mjr_render(viewport,self.scene,self.context)
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        self.context.free()
        # mj.mjv_freeScene(scene)
        # mj.mjr_freeContext(context)
        glfw.terminate()

simu = multi_car('script\car.xml')
simu.simulate()