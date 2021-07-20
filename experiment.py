from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from psychopy import parallel
 
port = parallel.ParallelPort(address=0x0378)

monitors_ = {
    "office": [1920, 1080, 52.70, 29.64, 56]
}

def trigger(send_bit):
    port.setData(send_bit)
    core.wait(0.004)
    port.setData(0)

which_monitor = "office"
mon = monitors.Monitor("default")
w_px, h_px, w_cm, h_cm, d_cm = monitors_[which_monitor]
mon.setWidth(w_cm)
mon.setDistance(d_cm)
mon.setSizePix((w_px, h_px))

win = visual.Window(
    [w_px, h_px],
    monitor=mon,
    units="deg",
    color="#000000",
    fullscr=True,
    allowGUI=False,
    winType="pyglet"
)

win.mouseVisible = False


cue = visual.Circle(
    win,
    radius=4,
    edges=40,
    units="deg",
    fillColor="red",
    lineColor="red",
    pos=(-15, 7)
)

port.setData(0)
cue.fillColor = "red"
cue.lineColor = "red"
cue.draw()
trigger(50)
win.flip()
core.wait(5)

while not event.getKeys(keyList=['q'], timeStamped=False):
    for i in range(10):
        
        cue.fillColor = "orange"
        cue.lineColor = "orange"
        cue.draw()
        win.flip()
        core.wait(2)
        if event.getKeys(keyList=["escape"], timeStamped=False):
            win.close()
            core.quit()
        
        cue.fillColor = "green"
        cue.lineColor = "green"
        cue.draw()
        trigger(100)
        win.flip()
        core.wait(4)
        if event.getKeys(keyList=["escape"], timeStamped=False):
            win.close()
            core.quit()
        
        cue.fillColor = "red"
        cue.lineColor = "red"
        cue.draw()
        trigger(200)
        win.flip()
        core.wait(5)
        if event.getKeys(keyList=["escape"], timeStamped=False):
            win.close()
            core.quit()


trigger(250)
win.close()
core.quit()

