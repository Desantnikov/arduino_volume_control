import ctypes
import comtypes
from ctypes import wintypes


from v2.constants import ROUND_VOLUME_VALUE_TO_N_DIGITS

"""
Proudly copypasted from 
https://stackoverflow.com/questions/32149809/read-and-or-change-windows-8-master-volume-in-python

Don't give a shit what happens here, but it works
"""

MMDeviceApiLib = comtypes.GUID(
    '{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = comtypes.GUID(
    '{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceCollection = comtypes.GUID(
    '{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IMMDeviceEnumerator = comtypes.GUID(
    '{A95664D2-9614-4F35-A746-DE8DB63617E6}')
IID_IAudioEndpointVolume = comtypes.GUID(
    '{5CDF2C82-841E-4546-9722-0CF74078229A}')
CLSID_MMDeviceEnumerator = comtypes.GUID(
    '{BCDE0395-E52F-467C-8E3D-C4579291692E}')

# EDataFlow
eRender = 0  # audio rendering stream
eCapture = 1  # audio capture stream
eAll = 2  # audio rendering or capture stream

# ERole
eConsole = 0  # games, system sounds, and voice commands
eMultimedia = 1  # music, movies, narration
eCommunications = 2  # voice communications

LPCGUID = REFIID = ctypes.POINTER(comtypes.GUID)
LPFLOAT = ctypes.POINTER(ctypes.c_float)
LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPUINT = ctypes.POINTER(wintypes.UINT)
LPBOOL = ctypes.POINTER(wintypes.BOOL)
PIUnknown = ctypes.POINTER(comtypes.IUnknown)


class IMMDevice(comtypes.IUnknown):
    _iid_ = IID_IMMDevice
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'Activate',
                           (['in'], REFIID, 'iid'),
                           (['in'], wintypes.DWORD, 'dwClsCtx'),
                           (['in'], LPDWORD, 'pActivationParams', None),
                           (['out', 'retval'], ctypes.POINTER(PIUnknown), 'ppInterface')),
        comtypes.STDMETHOD(ctypes.HRESULT, 'OpenPropertyStore', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetId', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetState', []))


PIMMDevice = ctypes.POINTER(IMMDevice)


class IMMDeviceCollection(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceCollection


PIMMDeviceCollection = ctypes.POINTER(IMMDeviceCollection)


class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'EnumAudioEndpoints',
                           (['in'], wintypes.DWORD, 'dataFlow'),
                           (['in'], wintypes.DWORD, 'dwStateMask'),
                           (['out', 'retval'], ctypes.POINTER(PIMMDeviceCollection),
                            'ppDevices')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetDefaultAudioEndpoint',
                           (['in'], wintypes.DWORD, 'dataFlow'),
                           (['in'], wintypes.DWORD, 'role'),
                           (['out', 'retval'], ctypes.POINTER(PIMMDevice), 'ppDevices')))

    @classmethod
    def get_default(cls, dataFlow, role):
        enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator, cls, comtypes.CLSCTX_INPROC_SERVER)
        return enumerator.GetDefaultAudioEndpoint(dataFlow, role)


class VolumeController(comtypes.IUnknown):
    _iid_ = IID_IAudioEndpointVolume
    _methods_ = (
        comtypes.STDMETHOD(ctypes.HRESULT, 'RegisterControlChangeNotify', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'UnregisterControlChangeNotify', []),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelCount',
                           (['out', 'retval'], LPUINT, 'pnChannelCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevel',
                           (['in'], ctypes.c_float, 'fLevelDB'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevelScalar',
                           (['in'], ctypes.c_float, 'fLevel'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevel',
                           (['out', 'retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevelScalar',
                           (['out', 'retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevel',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['in'], ctypes.c_float, 'fLevelDB'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevelScalar',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['in'], ctypes.c_float, 'fLevel'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevel',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['out', 'retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevelScalar',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['out', 'retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMute',
                           (['in'], wintypes.BOOL, 'bMute'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMute',
                           (['out', 'retval'], LPBOOL, 'pbMute')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeStepInfo',
                           (['out', 'retval'], LPUINT, 'pnStep'),
                           (['out', 'retval'], LPUINT, 'pnStepCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepUp',
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepDown',
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'QueryHardwareSupport',
                           (['out', 'retval'], LPDWORD, 'pdwHardwareSupportMask')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeRange',
                           (['out', 'retval'], LPFLOAT, 'pfLevelMinDB'),
                           (['out', 'retval'], LPFLOAT, 'pfLevelMaxDB'),
                           (['out', 'retval'], LPFLOAT, 'pfVolumeIncrementDB')))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_volume = 0

    @classmethod
    def get_default(cls):
        endpoint = IMMDeviceEnumerator.get_default(eRender, eMultimedia)
        interface = endpoint.Activate(cls._iid_, comtypes.CLSCTX_INPROC_SERVER)
        return ctypes.cast(interface, ctypes.POINTER(cls))

    def set_system_volume(self, volume, round_volume=ROUND_VOLUME_VALUE_TO_N_DIGITS):
        rounded_volume = round(volume, round_volume)

        print(f'Rounded: {rounded_volume}; Current: {self.current_volume}')
        if rounded_volume == self.current_volume:
            print(f'Same volume: {rounded_volume}, ignore')
            return

        print(f'Set system volume rounded to 2: {rounded_volume}\r\n')
        self.current_volume = rounded_volume

        comtypes.CoInitialize()
        ev = self.get_default()
        ev.SetMasterVolumeLevelScalar(rounded_volume)
        comtypes.CoUninitialize()


