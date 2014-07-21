import logging
import threading
import multiprocessing as multip
import Queue

from spikeylab.tools.util import create_unique_path
from spikeylab.data.dataobjects import AcquisitionData
from spikeylab.main.search_runner import SearchRunner
from spikeylab.main.protocol_runner import ProtocolRunner
from spikeylab.main.chart_runner import ChartRunner
from spikeylab.main.calibration_runner import CalibrationRunner, CalibrationCurveRunner
from spikeylab.stim.stimulusmodel import StimulusModel

class AcquisitionManager():
    """Handles all of the marshalling of different acquisition operations to the correct runner class.
    
    Opens and closes shared data file.
    """
    def __init__(self):

        self.datafile = None
        self.savefolder = None
        self.savename = None

        # self.signals = ProtocolSignals()
        pipelist = ['curve_finished',
                'ncollected',
                'warning',
                'response_collected',
                'average_response',
                'calibration_response_collected',
                'current_trace',
                'current_rep',
                'spikes_found',
                'stim_generated',
                'threshold_updated',
                'trace_finished',
                'group_finished',
                'calibration_file_changed',
                'tuning_curve_started',
                'tuning_curve_response',
                'over_voltage',]
        signals = {}
        recieved_signals = {}
        for p in pipelist:
            # recvr, sendr = multip.Pipe()
            # sendr = multip.Queue()
            sendr = Queue.Queue()
            recvr = sendr
            waker = threading.Event()
            signals[p] = (sendr, waker)
            recieved_signals[p] = (recvr, waker)
        self.signals = signals
        self.recieved_signals = recieved_signals
        self.acquisition_hooks = {}
        # self.signals = {
                # 'curve_finished' : Pipe(),
                # 'ncollected' : Pipe(),
                # 'warning' : Pipe(),
                # 'response_collected' : Pipe(),
                # 'average_response' : Pipe(),
                # 'calibration_response_collected' : Pipe(),
                # 'current_trace' : Pipe(),
                # 'current_rep' : Pipe(),
                # 'spikes_found' : Pipe(),
                # 'stim_generated' : Pipe(),
                # 'threshold_updated' : Pipe(),
                # 'trace_finished' : Pipe(),
                # 'group_finished' : Pipe(),
                # 'calibration_file_changed': Pipe(),
                # 'tuning_curve_started' : Pipe(),
                # 'tuning_curve_response': Pipe(),
                # 'over_voltage': Pipe(),
        # }

        self.explorer = SearchRunner(self.signals)
        self.protocoler =  ProtocolRunner(self.signals)
        self.bs_calibrator = CalibrationRunner(self.signals)
        self.tone_calibrator = CalibrationCurveRunner(self.signals)
        self.charter = ChartRunner(self.signals)
        self.cal_toner = SearchRunner(self.signals)
        stim_names = self.cal_toner.stim_names()
        toneidx = stim_names.index("Pure Tone")
        self.cal_toner.set_stim_by_index(toneidx)
        self.cal_tone_idx = toneidx
        # charter should share protocol model with windowed
        self.charter.protocol_model = self.protocoler.protocol_model

        self.selected_calibration_index = 0
        self.current_cellid = 0

    def _pipe_listen(self):
        # create listener threads for all acquisition hooks
        self.pipe_threads = []
        for name, pipe_waker in self.recieved_signals.items():
            p, wake_event = pipe_waker
            if name in self.acquisition_hooks:
                print '{} hook established'.format(name)
                t = threading.Thread(target=self._listen, args=(p, self.acquisition_hooks[name], wake_event))
                t.daemon = True
                self.pipe_threads.append(t)

    def _listen(self, pipe, func, wake_event):
        getcount = 0
        while not self._halt_threads:
            # if pipe.poll():
            if not pipe.empty():
                # data = pipe.recv()
                data = pipe.get()
                func(*data)
                getcount += 1
            wake_event.clear()
            wake_event.wait()

    def start_listening(self):
        # clear any previous listers?
        print "I'm listening"
        self._pipe_listen()
        self._halt_threads = False
        for t in self.pipe_threads:
            t.start()

    def stop_listening(self):
        self._halt_threads = True
        # wake them up so that they can die
        for name, pipe_waker in self.recieved_signals.items():
            p, wake_event = pipe_waker
            wake_event.set()


    def set_pipe_callback(self, name, func):
        self.acquisition_hooks[name] = func

    def increment_cellid(self):
        """Increments the current cellid number that is saved for each test run"""
        self.current_cellid +=1

    def stimuli_list(self):
        """Get a list of the stimuli for search operation

        :returns: list<AbstractStimulusComponent> -- list of the stimuli classes instances in the search operation
        """
        return self.explorer.stimuli_list()

    def set_cal_tone(self, freq, db):
        """Sets the test calibration tone, for settting the reference intensity/voltage point

        :param freq: Frequency of the tone to be played
        :type freq: int
        :param db: Intensity of the tone to be played
        :type db: float
        """
        stims = self.cal_toner.stimuli_list()
        for stim in stims:
            if stim.name == 'Pure Tone':
                stim.set('frequency', freq)
                stim.set('intensity', db)
        self.cal_toner.set_stim_by_index(self.cal_tone_idx)

    def set_calibration(self, datakey, calf=None, frange=None):
        """Sets a calibration for all of the acquisition operations

        :param datakey: name of the calibration to set. This key must be present in the current data file. A value of ``None`` clears calibration.
        :type datakey: str
        :param calf: Calibration frequency for the attenuation vector to be in relation to. All other frequencies will be in attenutaion from this frequency.
        :type calf: int
        :param frange: Frequency range, low and high, for which to restrict the calibration to
        :type frange: (int, int)
        """
        if datakey is None:
            calibration_vector, calibration_freqs = None, None
        else:
            if calf is None:
                raise Exception('calibration reference frequency must be specified')    
            try:
                cal = self.datafile.get_calibration(datakey, calf)
            except:
                print "Error: unable to load calibration data from: ", datakey
                raise
            calibration_vector, calibration_freqs = cal
        # clear one cache -- affects all StimulusModels
        StimulusModel.clearCache()
        logger = logging.getLogger('main')
        logger.debug('clearing cache')
        logger.debug('setting explore calibration')
        self.explorer.set_calibration(calibration_vector, calibration_freqs, frange, datakey)
        logger.debug('setting protocol calibration')
        self.protocoler.set_calibration(calibration_vector, calibration_freqs, frange, datakey)
        logger.debug('setting chart calibration')
        self.charter.set_calibration(calibration_vector, calibration_freqs, frange, datakey)
        logger.debug('setting calibrator calibration')
        self.bs_calibrator.stash_calibration(calibration_vector, calibration_freqs, frange, datakey)
        logger.debug('setting tone calibrator calibration')
        self.tone_calibrator.stash_calibration(calibration_vector, calibration_freqs, frange, datakey)

    def current_calibration(self):
        """The currently employed calibration

        :returns: (numpy.ndarray, numpy.ndarray) -- Attenuation vector, and associated frequencies
        """
        return self.bs_calibrator.stashed_calibration()

    def set_calibration_duration(self, dur):
        """Sets the stimulus duration for the calibration stimulus. Sets for calibration chirp, test tone, and calibration curve tones

        :param dur: Duration (seconds) of output signal
        :type dur: float
        """
        self.bs_calibrator.set_duration(dur)
        self.tone_calibrator.set_duration(dur)
        self.cal_toner.set_current_stim_parameter('duration', dur)
        # resets the signal in player to output
        self.cal_toner.set_stim_by_index(self.cal_tone_idx)

    def set_calibration_reps(self, reps):
        """Sets the number of repetitions for calibration stimuli

        :param reps: Number of times a unique stimulus is presented in calibration operations
        :type reps: int
        """
        self.bs_calibrator.set_reps(reps)
        self.tone_calibrator.set_reps(reps)

    def create_data_file(self, fname):
        """Creates a new data file to use

        :param fname: File path of the location for the data file to open
        :type fname: str
        """
        self.datafile = AcquisitionData(fname)

        self.explorer.set(datafile=self.datafile)
        self.protocoler.set(datafile=self.datafile)
        self.charter.set(datafile=self.datafile)
        self.bs_calibrator.set(datafile=self.datafile)
        self.tone_calibrator.set(datafile=self.datafile)

        return fname

    def load_data_file(self, fname):
        """Opens an existing data file to append to

        :param fname: File path of the location for the data file to open
        :type fname: str
        """
        self.close_data()
        self.datafile = AcquisitionData(fname, filemode='a')

        self.explorer.set(datafile=self.datafile)
        self.protocoler.set(datafile=self.datafile)
        self.charter.set(datafile=self.datafile)
        self.bs_calibrator.set(datafile=self.datafile)
        self.tone_calibrator.set(datafile=self.datafile)
        self.set_calibration(None)

    def current_data_file(self):
        """Name of the currently employed data file

        :returns: str -- File name of the open data file
        """
        return self.datafile.filename

    def set_threshold(self, threshold):
        """Sets spike detection threshold

        :param threshold: electrical potential to determine spikes (V)
        :type threshold: float
        """
        self.explorer.set_threshold(threshold)
        self.protocoler.set_threshold(threshold)

    def set(self, **kwargs):
        """Sets acquisition parameters for all acquisition types"""
        self.explorer.set(**kwargs)
        self.protocoler.set(**kwargs)
        self.bs_calibrator.set(**kwargs)
        self.tone_calibrator.set(**kwargs)
        self.charter.set(**kwargs)
        self.cal_toner.set(**kwargs)

    def set_stim_by_index(self, index):
        """Sets the current stimulus for search operation by it's index in the order of stim types

        :param index: Index of stimulus to set from the stimuli list
        :type index: int
        """
        self.explorer.set_stim_by_index(index)

    def current_stim(self):
        """The signal of the current search stimulus

        :returns: numpy.ndarray -- the voltage signal of the output
        """
        return self.explorer.current_signal()

    def explore_stim_names(self):
        """Names of the available search operation stimuli, in order

        :returns: list<str> -- list of the names of the stimuli
        """
        return self.explorer.stim_names()

    def run_explore(self, interval):
        """Runs the explore operation

        :param interval: The repetition interval between stimuli presentations (seconds)
        :type interval: float
        :returns: threading.thread -- the acquisition thread
        """
        return self.explorer.run(interval)

    def setup_protocol(self, interval):
        """Sets up the protocol operation for the current settings

        :param interval: The repetition interval between stimuli presentations (seconds)
        :type interval: float
        """
        return self.protocoler.setup(interval)

    def protocol_total_count(self):
        """The number of stimuli presentations (including reps) for the current protocol contents

        :returns: int -- number of presentations
        """
        return self.protocoler.count()

    def run_protocol(self):
        """Runs the protocol operation with the current settings

        :returns: threading.thread -- the acquisition thread
        """
        return self.protocoler.run()

    def run_caltone(self, interval):
        """Runs continuous reptition of the calibration tone"""
        return self.cal_toner.run(interval)

    def set_calibration_by_index(self, idx):
        """Sets the calibration stimulus by it's index in the list of calibration stimuli, with tone curve always being last"""
        self.selected_calibration_index = idx

    def calibration_total_count(self):
        """The number of stimuli presentations (including reps) for the current calibration selected
        
        :returns: int -- number of presentations
        """
        if self.selected_calibration_index == 2:
            return self.tone_calibrator.count()
        else:
            return self.bs_calibrator.count()

    def run_calibration(self, interval, applycal):
        """Runs the calibration operation with the current settings
        
        :param interval: The repetition interval between stimuli presentations (seconds)
        :type interval: float
        :param applycal: Wether to apply a previous saved calibration to this run
        :type applycal: bool
        :returns: threading.thread -- the acquisition thread
        """
        if self.selected_calibration_index == 2:
            self.tone_calibrator.apply_calibration(applycal)
            self.tone_calibrator.setup(interval)
            return self.tone_calibrator.run()
        else:
            self.bs_calibrator.set_stim_by_index(self.selected_calibration_index)
            self.bs_calibrator.apply_calibration(applycal)
            self.bs_calibrator.setup(interval)
            return self.bs_calibrator.run()

    def start_chart(self):
        """Starts the chart acquistion"""
        self.charter.start_chart()

    def stop_chart(self):
        """Halts the chart acquisition"""
        self.charter.stop_chart()

    def run_chart_protocol(self, interval):
        """Runs the stimuli presentation during a chart acquisition

        :param interval: The repetition interval between stimuli presentations (seconds)
        :type interval: float
        :returns: threading.thread -- the acquisition thread
        """
        self.charter.setup(interval)
        return self.charter.run()

    def process_calibration(self, save=True, calf=20000):
        """Processes a completed calibration

        :param save: Wether to save this calibration to file
        :type save: bool
        :param calf: Frequency for which to reference attenuation curve from
        :type calf: int
        :returns: str -- name of a saved calibration
        """
        if self.selected_calibration_index == 2:
            results, calname, freq = self.tone_calibrator.process_calibration(save)
        else:
            results, calname, freq = self.bs_calibrator.process_calibration(save)
        return calname

    def halt(self):
        """Halts any/all running operations"""
        self.explorer.halt()
        self.protocoler.halt()
        self.bs_calibrator.halt()
        self.tone_calibrator.halt()
        self.charter.halt()
        self.cal_toner.halt()

    def close_data(self):
        """Closes the current data file"""
        if self.datafile is not None:
            self.datafile.close()

    def protocol_model(self):
        """Gets the model for the protocol operation

        :returns: ProtocolModel
        """
        return self.protocoler.protocol_model

    def calibration_stimulus(self, mode):
        """Gets the stimulus model for calibration

        :param mode: Type of stimulus to get: tone or noise
        :type mode: str
        :returns: StimulusModel
        """
        if mode == 'tone':
            return self.tone_calibrator.stimulus
        elif mode =='noise':
            return self.bs_calibrator.stimulus

    def explore_genrate(self):
        """Gets the ouput samplerate for the search operation

        :returns: int -- the outgoing samplerate
        """
        return self.explorer.stimulus.samplerate()

    def calibration_genrate(self):
        """Gets the ouput samplerate for the calibration operation

        :returns: int -- the outgoing samplerate
        """
        return self.bs_calibrator.stimulus.samplerate()

    def calibration_range(self):
        """Gets the range of the frequencies and intensities in the calibration tone curve

        :returns: list -- the auto 
        """
        return self.tone_calibrator.stimulus.autoParamRanges()

    def calibration_template(self):
        """Gets the template documentation for the both the tone curve calibration and noise calibration

        :returns: dict -- all information necessary to recreate calibration objects
        """
        temp = {}
        temp['tone_doc'] = self.tone_calibrator.stimulus.templateDoc()
        comp_doc = []
        for calstim in self.bs_calibrator.get_stims():
            comp_doc.append(calstim.stateDict())
        temp['noise_doc'] = comp_doc
        return temp

    def load_calibration_template(self, template):
        """Reloads calibration settings from saved template doc

        :param template: Values for calibration stimuli (see calibration_template function)
        :type template: dict
        """
        self.tone_calibrator.stimulus.clearComponents()
        self.tone_calibrator.stimulus.loadFromTemplate(template['tone_doc'], self.tone_calibrator.stimulus)
        comp_doc = template['noise_doc']
        for state, calstim in zip(comp_doc, self.bs_calibrator.get_stims()):
            calstim.loadState(state)

    def clear_protocol(self):
        """Clears all tests from the protocol acquisition"""
        self.protocoler.clear()

    def set_group_comment(self, comment):
        """Sets a comment for the last executed protocol group"""
        self.protocoler.set_comment(self.current_cellid, comment)

    def attenuator_connection(self):
        """Checks the connection to the attenuator, and attempts to connect if not connected.

        :returns: bool - wether there is a connection
        """
        # all or none will be connected
        acquisition_modules = [self.explorer, self.protocoler, self.bs_calibrator, self.tone_calibrator, self.charter]
        if not acquisition_modules[0].player.attenuator_connected():
            #attempt to re-connect first
            for module in acquisition_modules:
                success = module.player.connect_attenuator()
            if success is None:
                return False
            else:
                return True
        else:
            return True
