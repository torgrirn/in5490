from music21 import converter, instrument, note, chord, stream, midi, corpus
from midi_functions import streamToNoteArray
import numpy as np

def chorales_from_corpus():
    """ Return a list of Bach chorales """
    chorales = corpus.getComposer('bach', 'xml')
    chorale_list = []
    for chorale in chorales:
        chorale_list.append(converter.parse(chorale))
    return chorale_list

def save_streams(chorales):
    """ Store file of midi streams """
    stream_array = []
    reference_set = set(["Soprano", "Alto", "Tenor", "Bass"])

    for i, chorale in enumerate(chorales):
        part_set = set([parts.id for parts in chorale])

        # Choose only chorales with all four voices.
        if reference_set.issubset(part_set):
            for part in chorale:
                if part.id in reference_set:
                    stream_array.append(part)
        else:
            print("Skipped", i)
        if i % 10 == 0:
            print(i)
    stream_array = np.array(stream_array)
    np.savez('../files/all_voices_stream', streams=stream_array)


def save_chorales(chorales):
    np.savez('../files/chorales', streams=chorales)

def load_chorales():
    with np.load('chorales.npz') as data:
        choral = data['streams']
    return choral


def filter_voices(chorales, split=False, save=False):
    """ Filter out chorales with all four voices:
        Soprano
        Alto
        Tenor
        Bass
        ARGS:
            note_array <list>: list of chorales.
            split <boolean>: Choose to store all voices in single list or split into four separate lists.
        Returns:

    """

    list_of_parts = []
    reference_set = set(["Soprano", "Alto", "Tenor", "Bass"])

    for i, chorale in enumerate(chorales):
        part_set = set([parts.id for parts in chorale])

        # Choose only chorales with all four voices.
        if reference_set.issubset(part_set):
            for part in chorale:
                if part.id in reference_set:
                    list_of_parts.append(streamToNoteArray(part))
        else:
            print("Skipped", i)
        if i % 10 == 0:
            print(i)

    soprano = np.array(list_of_parts[0:len(list_of_parts):4])
    alto = np.array(list_of_parts[1:len(list_of_parts):4])
    tenor = np.array(list_of_parts[2:len(list_of_parts):4])
    bass = np.array(list_of_parts[3:len(list_of_parts):4])
    print("Number of soprano voices:",len(soprano))
    print("Number of alto voices:",len(soprano))
    print("Number of tenor voices:",len(soprano))
    print("Number of bass voices:",len(soprano))

    if split:
        if save:
            np.savez('soprano.npz', voices = soprano_voices)
            np.savez('alto.npz', voices = alto_voices)
            np.savez('tenor.npz', voices = tenor_voices)
            np.savez('bass.npz', voices = bass_voices)
        return soprano, alto, tenor, bass
    else:
        list_of_parts = np.array(list_of_parts)
        if save:
            np.savez('all_voices_note_array.npz', voices = list_of_parts)
        return list_of_parts
