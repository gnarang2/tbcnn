import os
import multiprocessing
import tensorflow as tf

proc = None
summary_writer = None

def start_tensorboard_intern():
    os.system('python3 -m tensorboard.main --logdir=./logs/')

def start_tensorboard():
    global proc

    proc = multiprocessing.Process(target=start_tensorboard_intern) 
    proc.start()

def init_run(_logDir, graph=None):
    global summary_writer
    logDir = os.path.join('logs', _logDir)

    try:
        os.mkdir(logDir)
    except:
        pass

    summary_writer = tf.summary.FileWriter(logDir, graph)

def wait_tensorboard():
    proc.join()

def create_metrics_summary(metrics):
    summaries = []

    for dataset in ['training', 'test']:
        for name, metric in metrics.items():
            placeholder = tf.placeholder(tf.float32, shape=None, name=dataset + '_' + name)
            metric_summary = tf.summary.scalar(dataset + ' ' + name, placeholder)
            summaries.append(metric_summary)

    return tf.summary.merge(summaries)

def add_summary(summ_data, epoch):
    summary_writer.add_summary(summ_data, epoch)
    summary_writer.flush()