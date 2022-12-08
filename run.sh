ROOTPATH=$(pwd)
SIMU_ROOTPATH=${ROOTPATH}/simulation
ANALYSIS_ROOTPATH=${ROOTPATH}/analysis

DATA_ROOTPATH=${ANALYSIS_ROOTPATH}/data

NODE_IDS="1 2 3 4 5"
RERUN=1
if [ ${RERUN} == 1 ]; then
    time_str=$(date +%Y%m%d-%H%M%S)
else
    time_str="<data_folder>"
fi

DATA_PATH=${DATA_ROOTPATH}/${time_str}

SIMU_CONFIG=${SIMU_ROOTPATH}/mix/config.txt
SIMU_STDOUT_FILEPATH=${SIMU_ROOTPATH}/stdout.txt

ANALYSIS_CONFIG_TEMPLATE=${ANALYSIS_ROOTPATH}/config_template.py
ANALYSIS_CONFIG=${ANALYSIS_ROOTPATH}/config.py


function main() {
    if [ ${RERUN} == 1 ]; then
        mkdir -p ${DATA_PATH}
        cd ${SIMU_ROOTPATH}
        echo "Running simulation..."
        ./waf --run 'scratch/third mix/config.txt' > ${SIMU_STDOUT_FILEPATH}
        (( $? != 0)) && echo "Run simulation failed" && exit -1

        cd ${ROOTPATH}

        echo "Copying config files and tracing files"
        cp ${SIMU_CONFIG} ${DATA_PATH}
        cp ${SIMU_STDOUT_FILEPATH} ${DATA_PATH}
        files=$(cat ${SIMU_CONFIG} | grep FILE | awk '{print $2}')
        for file in ${files[@]}; do
            cp ${SIMU_ROOTPATH}/${file} ${DATA_PATH}
        done

        cd ${ANALYSIS_ROOTPATH}
        echo "Deserialize trace file"
        ./trace_reader ${DATA_PATH}/mix.tr > ${DATA_PATH}/mix.tr.txt
    else
        echo "RERUN = ${RERUN}, Use old simulation data"
    fi

    cd ${ANALYSIS_ROOTPATH}

    sed "s/<data_time_str>/${time_str}/g" ${ANALYSIS_CONFIG_TEMPLATE} > ${ANALYSIS_CONFIG}

    echo "Ploting all in one diagram"
    python3 plot.py ${NODE_IDS}

    echo "Ploting diagram for each node"
    for node_id in ${NODE_IDS[@]}; do
        python3 plot.py ${node_id}
        echo "Node ${node_id} Diagram generated to ${DATA_PATH}/node_${node_id}_bw.png"
    done
}

main "$*"
