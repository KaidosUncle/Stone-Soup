import numpy as np
import os

from ..runmanagercore import RunManagerCore

# Run from stonesoup working directory
# def setup_module():
#     while os.getcwd().split('\\')[-1] != 'stonesoup':
#         os.chdir(os.path.dirname(os.getcwd()))

# test_config = "stonesoup\\runmanager\\tests\\test_configs\\test_config_all.yaml"
# test_config_nomm = "stonesoup\\runmanager\\tests\\test_configs\\test_config_nomm.yaml"
# test_config_nogt = "stonesoup\\runmanager\\tests\\test_configs\\test_config_nogt.yaml"
# test_config_trackeronly =
# "stonesoup\\runmanager\\tests\\test_configs\\test_config_trackeronly.yaml"
# test_json = "stonesoup\\runmanager\\tests\\test_configs\\dummy.json"

# These paths for circleci tests
test_config = "stonesoup/runmanager/tests/test_configs/test_config_all.yaml"
test_config_nomm = "stonesoup/runmanager/tests/test_configs/test_config_nomm.yaml"
test_config_nogt = "stonesoup/runmanager/tests/test_configs/test_config_nogt.yaml"
test_config_trackeronly = "stonesoup/runmanager/tests/test_configs/test_config_trackeronly.yaml"
test_json = "stonesoup/runmanager/tests/test_configs/dummy.json"
test_config_dir = "stonesoup/runmanager/tests/test_configs/"

rmc = RunManagerCore(test_config, test_json, False, test_config_dir)


def test_cwd_path():
    assert os.path.isdir('stonesoup/runmanager/tests/test_configs') is True


def test_read_json():

    test_json_data = rmc.read_json(test_json)
    assert type(test_json_data) is dict


def test_set_trackers():

    test_combo = [{'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 500},
                  {'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 540},
                  {'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 580},
                  {'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 620},
                  {'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 660},
                  {'SingleTargetTracker.initiator.initiator.prior_state.num_particles': 700}]

    with open(test_config, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, True)
    file.close()

    trackers, ground_truths, metric_managers = rmc.set_trackers(test_combo,
                                                                tracker, gt, mm)

    assert type(trackers) is list
    assert type(ground_truths) is list
    assert type(metric_managers) is list

    assert len(trackers) > 0
    assert "tracker" in str(type(trackers[0]))
    assert ground_truths[0] == trackers[0].detector.groundtruth
    assert "metricgenerator" in str(type(metric_managers[0]))


def test_set_trackers_edge_cases():

    empty_combo = []
    combo_no_path = [{'abc': 0}]

    with open(test_config, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, True)
    file.close()

    # Empty combo dict
    trackers, ground_truths, metric_managers = rmc.set_trackers(empty_combo,
                                                                tracker, gt, mm)

    assert type(trackers) is list
    assert type(ground_truths) is list
    assert type(metric_managers) is list
    assert len(trackers) == 0
    assert len(ground_truths) == 0
    assert len(metric_managers) == 0

    # No path combo dict
    trackers, ground_truths, metric_managers = rmc.set_trackers(combo_no_path,
                                                                tracker, gt, mm)

    assert type(trackers) is list
    assert type(ground_truths) is list
    assert type(metric_managers) is list
    assert len(trackers) == 1
    assert len(ground_truths) == 1
    assert len(metric_managers) == 1


def test_set_param():

    with open(test_config, 'r') as file:
        tracker, _, _ = rmc.read_config_file(file, True)
    file.close()

    test_split_path = ['initiator', 'initiator', 'prior_state', 'num_particles']
    test_value = 250

    assert test_split_path[-1] not in dir(tracker.initiator.initiator.prior_state)

    rmc.set_param(test_split_path, tracker, test_value)

    assert test_split_path[-1] in dir(tracker.initiator.initiator.prior_state)
    assert tracker.initiator.initiator.prior_state.num_particles is test_value


def test_set_param_edge_cases():
    empty_path = []
    one_path = ['a']
    test_value = 0

    with open(test_config, 'r') as file:
        tracker, _, _ = rmc.read_config_file(file, True)
    file.close()

    # Empty path
    orig_tracker = tracker
    rmc.set_param(empty_path, tracker, test_value)  # Shouldn't do anything
    assert tracker is orig_tracker

    # Path with one element
    assert 'a' not in dir(tracker)
    rmc.set_param(one_path, tracker, test_value)
    assert 'a' in dir(tracker)
    assert tracker.a is test_value


def test_read_config_file():

    # Config with all tracker, grountruth, metric manager
    with open(test_config, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, True)
    assert "tracker" in str(type(tracker))
    assert gt == tracker.detector.groundtruth
    assert "metricgenerator" in str(type(mm))
    file.close()


def test_read_config_file_nomm():

    # Config with tracker and groundtruth but no metric manager
    with open(test_config_nomm, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, True)
    assert "tracker" in str(type(tracker))
    assert gt == tracker.detector.groundtruth
    assert mm is None
    file.close()


def test_read_config_file_nogt():

    # Config with tracker and metric manager but no groundtruth
    with open(test_config_nogt, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, False)
    assert "tracker" in str(type(tracker))
    assert gt is None
    assert "metricgenerator" in str(type(mm))
    file.close()


def test_read_config_file_tracker_only():
    # Config with tracker only
    with open(test_config_trackeronly, 'r') as file:
        tracker, gt, mm = rmc.read_config_file(file, False)
    assert "tracker" in str(type(tracker))
    assert gt is None
    assert mm is None
    file.close()
    
def test_read_config_dir():
    result = rmc.read_config_dir(test_config_dir)
    assert type(result) is list

def test_read_config_dir_empty():
    result = rmc.read_config_dir('')
    assert result is None
    
def test_get_filepaths():
    file_path = rmc.get_filepaths(test_config_dir)
    assert type(file_path) is list

def test_get_filepaths_empty():
    file_path = rmc.get_filepaths('')
    assert len(file_path) == 0

def test_get_config_and_param_lists():
    files = rmc.get_filepaths(test_config_dir)
    pair = rmc.get_config_and_param_lists(files)
    assert type(pair) is list

def test_set_components_empty():
    tracker, ground_truth, metric_manager = rmc.set_components('', True)
    assert tracker is None
    assert ground_truth is None
    assert metric_manager is None

def test_set_components():
    tracker, ground_truth, metric_manager = rmc.set_components(test_config, True)
    assert "tracker" in str(type(tracker))
    assert ground_truth == tracker.detector.groundtruth
    assert "metricgenerator" in str(type(metric_manager))
    
def test_set_components_no_gt():
    tracker, ground_truth, metric_manager = rmc.set_components(test_config_nogt, False)
    assert "tracker" in str(type(tracker))
    assert ground_truth == None
    assert "metricgenerator" in str(type(metric_manager))
    
def test_set_components_no_gt_mm():
    tracker, ground_truth, metric_manager = rmc.set_components(test_config_trackeronly, False)
    assert "tracker" in str(type(tracker))
    assert ground_truth == None
    assert metric_manager == None

def test_set_components_no_mm():
    tracker, ground_truth, metric_manager = rmc.set_components(test_config_nomm, True)
    assert "tracker" in str(type(tracker))
    assert ground_truth == tracker.detector.groundtruth
    assert metric_manager == None

