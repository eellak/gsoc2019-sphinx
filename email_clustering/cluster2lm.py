import subprocess
import os

if __name__ == '__main__':
    output = './clusters-gsoc'
    for cluster in os.listdir(output):
        cluster_path = os.path.join(output, cluster)
        if subprocess.call(['ngram-count -kndiscount -interpolate -text ' + os.path.join(cluster_path, 'corpus') + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ' + os.path.join(cluster_path, 'model.lm')], shell=True):
            sys.exit('Error in subprocess')
