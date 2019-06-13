from osf_visualizer.visdom_visualizer.async.visualization_producer import VisualizationProducer

environment_num = 2

for j in range(environment_num):
    cb = VisualizationProducer(experiment_name="Example{}".format(j), port=8097, wait_time=2,
                               items=['loss', 'val_loss', 'iou_score', 'val_iou_score']
                               )
    for i in range(1, 100):
        cb.on_epoch_end(i, {"loss": 1.0 / i, "iou_score": 0.01 * i, 'val_loss': 0.1, 'val_iou_score':1.0})