import wget
import os

if __name__ == '__main__':
    MODEL_ID = 'pretrained_model'
    MODEL_PATH = './ckpt/%s' % MODEL_ID
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
    LINK_RELEASE = 'http://sound-of-pixels.csail.mit.edu/release'

    LIST_VAL = '%s/val.csv' % LINK_RELEASE
    WEIGHTS_FRAME = '%s/%s/frame_best.pth' % (LINK_RELEASE, MODEL_ID)
    WEIGHTS_SOUND = '%s/%s/sound_best.pth' % (LINK_RELEASE, MODEL_ID)
    WEIGHTS_SYNTHESIZER = '%s/%s/synthesizer_best.pth' % (LINK_RELEASE, MODEL_ID)

    # start download
    filename = wget.download(url=LIST_VAL, out='./data')
    print('download to %s' % filename)

    filename = wget.download(url=WEIGHTS_FRAME, out=MODEL_PATH)
    print('download to %s' % filename)

    filename = wget.download(url=WEIGHTS_SOUND, out=MODEL_PATH)
    print('download to %s' % filename)

    filename = wget.download(url=WEIGHTS_SYNTHESIZER, out=MODEL_PATH)
    print('download to %s' % filename)
