import mujoco as mj
import glfw
from threading import Lock


button_left_pressed = False
button_right_pressed = False
button_middle_pressed = False
lastx = 0
lasty = 0

filename="/my_project/multi_car/car.xml"

model = mj.MjModel.from_xml_path('script\car.xml')
data = mj.MjData(model)


glfw.init()
width, height = glfw.get_video_mode(glfw.get_primary_monitor()).size
window = glfw.create_window(width // 2, height // 2, "mujoco", None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)


scene = mj.MjvScene(model, maxgeom=1000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150)
option = mj.MjvOption()
camera = mj.MjvCamera()
perturb = mj.MjvPerturb()

action = mj.mjtMouse(0)     # for mouse action definition
gui_lock = Lock()


def scroll(window,xoffset,yoffset):
  mj.mjv_moveCamera(model,mj.mjtMouse.mjMOUSE_ZOOM,0,-0.05*yoffset,scene,camera)
  return

def mouse_button(window, button, act, mods):
  global button_left_pressed
  global button_middle_pressed
  global button_right_pressed
  global lastx
  global lasty
  button_left_pressed = (
      glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
  )
  button_right_pressed = (
      glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS
  )
  button_mid_pressed = (
      glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS
  )

  lastx, lasty = glfw.get_cursor_pos(window)
  return

def mouse_move(window, xpos, ypos):
  global button_left_pressed
  global button_middle_pressed
  global button_right_pressed
  global lastx
  global lasty
  if not (button_left_pressed or button_right_pressed or button_middle_pressed):
    return
  mod_shift = (
      glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
      or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
  )
  if button_right_pressed:
    action = (
      mj.mjtMouse.mjMOUSE_MOVE_H
      if mod_shift
      else mj.mjtMouse.mjMOUSE_MOVE_V
    )
  elif button_left_pressed:
    action = (
      mj.mjtMouse.mjMOUSE_ROTATE_H
      if mod_shift
      else mj.mjtMouse.mjMOUSE_ROTATE_V
    )
  else:
    action = mj.mjtMouse.mjMOUSE_ZOOM
  print('lastx: '+str(lastx))
  print('xpos: '+str(xpos))
  print('lasty: '+str(lasty))
  print('ypos: '+str(ypos))
  dx = xpos - lastx
  dy = ypos - lasty
  lastx = xpos
  lasty = ypos
  width,height = glfw.get_window_size(window)
  with gui_lock:
    mj.mjv_moveCamera(model,action,dx/height,dy/height,scene,context)
  return

glfw.set_scroll_callback(window, scroll)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)

while not glfw.window_should_close(window):
  starttime = data.time
  while data.time-starttime<1/60:
    mj.mj_step(model,data)

  viewport = mj.MjrRect(0, 0, 0, 0)
  viewport.width, viewport.height = glfw.get_framebuffer_size(window)
  mj.mjv_updateScene(model,data,option,perturb,camera,mj.mjtCatBit.mjCAT_ALL,scene)
  mj.mjr_render(viewport,scene,context)
  glfw.swap_buffers(window)
  glfw.poll_events()


context.free()
# mj.mjv_freeScene(scene)
# mj.mjr_freeContext(context)
glfw.terminate()