CONFIG_DIR="../configs/example/myL3.py"
#OUTDIR="myPfOnSpec06Result"
OUTDIR="test"
#    1xxxx000 预热的指令数
WARM=1
#    1xxxx0000 快速跳过的指令数
FAST=90000000000
#    1xxxx0000
INST=10000000000
MEMSIZE="8192MB"
L1SIZE="64kB"
L2SIZE="512kB"
L3SIZE="2MB"
CPUNUM=1

datetime=`date +%Y-%m-%d_%H:%M:%S.%N `


prefetchs=(
    # "IrregularStreamBufferPrefetcher()"  
    # "STeMSPrefetcher()" 
    "none()"
    # "SignaturePathPrefetcher()"
)
for prefetch in "${prefetchs[@]}"
    do (
    benchmarks=(
        # "hotspot_pagerank"
        "hotspot_health"
        # "bzip22006"
        # "gcc2006"
        # "mcf2006"
        # "gobmk2006"
        # "hmmer2006"
        # "libquantum2006"
        # "xalancbmk2006"
    )
    for prog in  "${benchmarks[@]}"
        do
        (
            echo "====================begin=================="
            echo "warmup-insts :        $WARM"
            echo "fast-forward :        $FAST"
            echo "run-insts :           $INST"
            echo "prefetch :            $prefetch"
            echo "benchmark :           $prog"
            echo "outdir :              "$OUTDIR"/${prefetch:0:-2}"
            echo "config_file :         $CONFIG_DIR"

            if [ ${prefetch} == "none()" ];then
                l1dprefetcher=""
            else 
                # l1dprefetcher="--l1dprefetcher=\"${prefetch}\""
                l3prefetcher="--l3prefetcher=\"${prefetch}\""
            fi


            # echo \
            # ../build/X86/gem5.opt \
            # --redirect-stdout \
            # --outdir="$OUTDIR"/${datetime}/${prog}_${prefetch:0:-2}    \
            # --debug-flag="mydebug" \
            # "$CONFIG_DIR"  \
            # --num-cpus=$CPUNUM \
            # --cpu-type=DerivO3CPU \
            # --bench=$prog \
            # --caches --l2cache --l3cache \
            # --l1d_size=$L1SIZE --l2_size=$L2SIZE --l3_size=$L3SIZE \
            # -W $WARM \
            # -F $FAST \
            # -I $INST \
            # --mem-size=$MEMSIZE \
            # ${l3prefetcher}

            echo \
            ../build/X86/gem5.opt \
            --redirect-stdout \
            --outdir="$OUTDIR"/${datetime}/${prog}_${prefetch:0:-2}    \
            --debug-flag="ROI"  \
            "$CONFIG_DIR"  \
            --num-cpus=$CPUNUM \
            --cpu-type=DerivO3CPU \
            --bench=$prog \
            --caches --l2cache --l3cache \
            --l1d_size=$L1SIZE --l2_size=$L2SIZE --l3_size=$L3SIZE \
            -W $WARM \
            -F $FAST \
            -I $INST \
            --mem-size=$MEMSIZE \
            ${l3prefetcher} 


            
            # echo "build/X86/gem5.opt --redirect-stdout --outdir="$OUTDIR"/${prefetch:0:-2}/${prog} "$CONFIG_DIR" --num-cpus=$CPUNUM --cpu-type=DerivO3CPU --bench="${prog}" --caches --l2cache --l1d_size=$L1SIZE --l2_size=$L2SIZE --l3_size=$L3SIZE --l3cache --fast-forward=$FAST --warmup-insts=$WARM -I $INST --mem-size=$MEMSIZE --l3prefetcher="${prefetch}" "
            
            echo "${prefetch:0:-2} finish!"
            echo "====================end===================="
            echo ""
        ) &
        done
    ) & done
wait
echo "ALL JOB DONE!"
echo "generating the result..."




