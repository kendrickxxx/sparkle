import numpy as np
from spikeylab.acq.daq_tasks import AITaskFinite, AOTaskFinite, AITask, AOTask, \
                                    DigitalOutTask, get_ao_chans, get_ai_chans
try:
    from PyDAQmx import *
except:
    from spikeylab.acq.daqmx_stub import *

import time

DEBUG = False
DEVNAME = "PCI-6259"

from guppy import hpy

def setUp():
    h = hpy()
    stats = h.heap()
    with open('memuse.txt', 'w') as memfile:
        memfile.write(stats.__str__())

class TestDAQTasks():
    def setup(self):
        self.data = []
        self.sr = 1000000 # 1000000 is max for PCI-6259

        answer = bool32()
        err = DAQmxGetDevIsSimulated(DEVNAME, answer)
        self.devmode = answer.value

    def test_sync_finite(self):
        u"""
        Test basic operation of DAQ and drivers
        """

        #amps = [0.00002, 0.0001, 0.001, 0.01, 0.1, 1]
        amps = [0.01, 0.1, 1]
        frequency = 5#0000
        npts = 10000
        x = np.linspace(0,np.pi, npts)
        for amp in amps:
            aot = AOTaskFinite(DEVNAME+"/ao0", self.sr, npts, trigsrc=u"ai/StartTrigger")
            ait = AITaskFinite(DEVNAME+"/ai0", self.sr, npts)

            stim = amp * np.sin(frequency*x*2*np.pi)

            aot.write(stim)

            aot.StartTask()
            ait.StartTask()

            response = ait.read()

            aot.stop()
            ait.stop()

            response = np.roll(response, -1)
            response[-1] = stim[-1] # free pass on first point
            if DEBUG:
                import matplotlib.pyplot as plt
                plt.plot(x, stim, x, response)
                plt.show()

            assert stim.shape == response.shape

            if not self.devmode:
                tolerance = max(amp*0.1, 0.005) #noise floor
                assert np.allclose(stim[10:],response[10:],rtol=0,atol=tolerance)
            
    def test_sync_continuous(self):

        npts = 10000
        frequency = 50000
        amp = 2
        x = np.linspace(0, np.pi, npts)
        stim = amp * np.sin(frequency*x*2*np.pi)

        aot = AOTask(DEVNAME+"/ao0", self.sr, npts, trigsrc=b"ai/StartTrigger")
        ait = AITask(DEVNAME+"/ai0", self.sr, npts)

        ait.register_callback(self.stashacq,npts)

        aot.write(stim)
        aot.start()
        ait.start()

        acqtime = 2 #seconds 
        time.sleep(acqtime)

        aot.stop()
        ait.stop()
        # print('no. data points acquired: ', len(self.data), 'expected', acqtime*self.sr)
        # print type(self.data[0])

        expected = acqtime*self.sr
        assert expected*0.85 <= len(self.data) <= expected*1.1

    def test_asynch_continuous_finite(self):
        ainpts = 1000

        ait = AITask(DEVNAME+"/ai0", self.sr, ainpts)
        ait.register_callback(self.stashacq, ainpts)
        ait.start()
        
        amps = [0.01, 0.1, 1]
        frequency = 50000
        aonpts = 10000
        x = np.linspace(0, np.pi, aonpts)
        for amp in amps:
            aot = AOTaskFinite(DEVNAME+"/ao0", self.sr, aonpts, trigsrc=u"")

            stim = amp * np.sin(frequency*x*2*np.pi)

            aot.write(stim)
            aot.StartTask()
            aot.wait()
            aot.stop()

        ait.stop()

        assert len(self.data) > aonpts*len(amps)

    def test_digital_output(self):
        dur = 2
        rate = 2
        dout = DigitalOutTask(DEVNAME+'/port0/line1', rate)
        dout.start()
        time.sleep(dur)
        print 'samples generated', dout.generated()
        # this reading is haywire?
        # assert  dout.generated() == dur*rate
        dout.stop()

    def test_triggered_AI(self):
        npts = 10000
        rate = 2.
        trigger = DigitalOutTask(DEVNAME+'/port0/line1', rate)
        ait = AITaskFinite(DEVNAME+"/ai0", self.sr, npts, trigsrc='/'+DEVNAME+'/PFI0')
        starttime = time.time()
        trigger.start()
        ait.StartTask()
        response0 = ait.read()
        ait.StopTask()
        ait.start()
        # ait = AITaskFinite(DEVNAME+"/ai0", self.sr, npts, trigsrc='/'+DEVNAME+'/PFI0')
        response1 = ait.read()
        duration = time.time() - starttime
        trigger.stop()
        ait.stop()

        print "response shape", response1.shape
        print "duration", duration
        assert len(response1) == npts
        assert False

    def stashacq(self, data):
        self.data.extend(data.tolist())

def test_get_ao_chans():
    chans = get_ao_chans(DEVNAME)
    assert len(chans) == 4

def test_get_ai_chans():
    chans = get_ai_chans(DEVNAME)
    assert len(chans) == 32