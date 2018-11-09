import numpy as np
import multiprocessing
from chorales import filter_voices, load_chorales

def slice_sequence_examples(sequence, num_steps):
    """Slice a sequence into redundant sequences of length num_steps."""
    xs = []
    for i in range(len(sequence) - num_steps - 1):
        example = sequence[i: i + num_steps]
        xs.append(example)
    return xs

# Load dataset and create pairs of inputs and targets

def split_inputs(training_inputs, sample_length):
    inputs = []
    for seq in training_inputs:
        slices = slice_sequence_examples(seq, sample_length)
        for sl in slices:
            inputs.append(sl)
    inputs = np.array(inputs)
    np.savez(path+'split_inputs.npz', train=inputs)
    print("input length", len(inputs))

def split_targets(training_targets, sample_length):
    targets = []
    for seq in training_targets:
        slices = slice_sequence_examples(seq, sample_length)
        for sl in slices:
            targets.append(sl)
    targets = np.array(targets)
    np.savez(path+'split_targets.npz', train=targets)
    print("target length", len(targets))


def split_test_inputs(test_data_inputs, sample_length):
    test_inputs_split = []
    for seq in test_data_inputs:
        slices = slice_sequence_examples(seq, sample_length)
        for sl in slices:
            test_inputs_split.append(sl)
    test_inputs_split = np.array(test_inputs_split)
    np.savez(path+'split_test_inputs.npz', test=test_inputs_split)
    print("test input length", len(test_inputs_split))


def split_test_targets(test_data_targets, sample_length):
    test_targets_split = []
    for seq in test_data_targets:
        slices = slice_sequence_examples(seq, sample_length)
        for sl in slices:
            test_targets_split.append(sl)
    test_targets_split = np.array(test_targets_split)
    np.savez(path+'split_test_targets.npz', test=test_targets_split)
    print("test target length", len(test_targets_split))



if __name__ == '__main__':

    path = "../training_sets_split/"
    with np.load('all_voices_note_array.npz') as data:
            train_set = data['voices']
    #with np.load('very_small_set.npz') as data:
    #    train_set = data['train']
    num_examples = len(train_set)
    print("Length:", num_examples)

    # Use even number melody lines as inputs and odd numbers as targets
    training_inputs = train_set[0:num_examples:2]
    training_targets = train_set[1:num_examples:2]

    training_split = int(np.round(0.95 * num_examples))
    print("Training split",training_split)
    indices = np.arange(num_examples//2)
    np.random.shuffle(indices)
    test_indices = indices[0:num_examples - training_split]
    print("Test indices",len(test_indices))

    test_data_inputs = training_inputs[test_indices]
    test_data_targets = training_targets[test_indices]
    training_inputs = np.delete(training_inputs, test_indices)
    training_targets = np.delete(training_targets, test_indices)

    print("training inputs", len(training_inputs))
    print("training targets", len(training_targets))
    print("Test inputs", len(test_data_inputs))
    print("Test targets", len(test_data_targets))

    path = "../training_sets_split/"
    np.savez(path+'test_soprano_tenor.npz', test=np.array(test_data_inputs))
    np.savez(path+'test_alto_bass.npz', test=np.array(test_data_targets))

    sample_length = 64
    test_sample_length = 128

    split_in = multiprocessing.Process(target=split_inputs,args=(training_inputs, sample_length))
    split_tar = multiprocessing.Process(target=split_targets,args=(training_targets, sample_length))
    split_test_in = multiprocessing.Process(target=split_test_inputs,args=(test_data_inputs, sample_length))
    split_test_tar = multiprocessing.Process(target=split_test_targets,args=(test_data_targets, sample_length))

    split_in.start()
    split_tar.start()
    split_test_in.start()
    split_test_tar.start()
    split_in.join()
    split_tar.join()
    split_in.join()
    split_tar.join()
