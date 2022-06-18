#MyCRONO.py
from multiprocessing.dummy import Process
import m5
from m5.objects import *
m5.util.addToPath('../common')

# binary_dir = '/home/liangyangguang/CRONO/apps/'
binary_dir = '/home/liangyangguang/CRONO/pref_apps/'
data_dir = '/home/liangyangguang/CRONO/dataset/'
thread='1'
#====================

#---------apsp
apsp = Process(pid = 210)
apsp.executable = binary_dir + 'apsp/apsp'
apsp.cmd = [apsp.executable] + [thread, '1024', '40']

#----------bc
bc = Process(pid = 211)
bc.executable = binary_dir + 'bc/bc'
bc.cmd = [bc.executable] + [thread, '1024', '30']

#----------bfs
bfs = Process(pid = 212)
bfs.executable = binary_dir + 'bfs/bfs'
# no input file
bfs.cmd = [bfs.executable] + ['0', '1', '8000', '7000']
# with a input file
#bfs.cmd = [bfs.executable] + ['1', thread, data_dir+'roadNet-CA.txt']

#------------community
community = Process(pid = 213)
community.executable = binary_dir + 'community/community_lock'
# no input file
community.cmd = [community.executable] + ['0', '1', '25', '4096', '160']
# with a input file ----   1-inpufile.  2-.mtx file.
#community.cmd = [community.executable] + ['1', thread, '10000', data_dir+'roadNet-CA.txt']

#--------------connected_compponents
connected_components = Process(pid = 214)
connected_components.executable = binary_dir + 'connected_components/connected_components_lock'
# no input file
connected_components.cmd = [connected_components.executable] + ['0', '1', '8192', '1280']
# with a input file
#connected_components.cmd = [connected_components.executable] + ['1', thread, data_dir+'roadNet-CA.txt']

#--------------dfs
dfs = Process(pid = 215)
dfs.executable = binary_dir + 'dfs/dfs'
dfs.cmd = [dfs.executable] + [thread, data_dir+'roadNet-CA.txt']

#-------------pagerank
pagerank = Process(pid = 216)
pagerank.executable = binary_dir + 'pagerank/pagerank'
#pagerank.cmd = [pagerank.executable] + ['0', '4', '16384', '160']
pagerank.cmd = [pagerank.executable] + ['0', '1', '3000', '2999']
#pagerank.cmd = [pagerank.executable] + ['0', '1', '5500', '5000']
# with a input file
#pagerank.cmd = [pagerank.executable] + ['1', thread, data_dir+'roadNet-CA.txt']

#--------------sssp
sssp = Process(pid = 217)
sssp.executable = binary_dir + 'sssp/sssp'
sssp.cmd = [sssp.executable] + ['0', '1', '4096', '160']
# with a input file
#sssp.cmd = [sssp.executable] + ['1', thread, data_dir+'roadNet-CA.txt']

#-----------------triangle_counting
triangle_counting = Process(pid = 218)
triangle_counting.executable = binary_dir + 'triangle_counting/triangle_counting_lock'
triangle_counting.cmd = [triangle_counting.executable] + ['0', '1', '4096', '1000']
# with a input file
#triangle_counting.cmd = [triangle_counting.executable] + ['1', thread, data_dir+'roadNet-CA.txt']

#-----------------tsp
tsp = Process(pid = 219)
tsp.executable = binary_dir + 'tsp/tsp'
tsp.cmd = [tsp.executable] + [thread, '20']


# zjp_graph500_binary_dir = '/root/sdc1/zhoujiapeng/benchmark/graph500-newreference/src/'
zjp_gapbs_binary_dir = '/root/sde1/zhoujiapeng/benchmark/gapbs-1.4-serial/'

#-----------------zjp_add_tests
#-----------------reference_bfs
# graph500_bfs = Process(pid = 220)
# graph500_bfs.executable = zjp_graph500_binary_dir + 'graph500_reference_bfs'
# graph500_bfs.cmd = [graph500_bfs.executable] + ['16']

gapbs_choice = ['-g', '17']

#-----------------gapbs_sssp
gapbs_sssp = Process(pid = 221)
gapbs_sssp.executable = zjp_gapbs_binary_dir + 'sssp'
# gapbs_sssp.cmd = [gapbs_sssp.executable] + ['-g', '16', '-n', '1']
gapbs_sssp.cmd = [gapbs_sssp.executable] + gapbs_choice

#-----------------gapbs_bc
gapbs_bc = Process(pid = 222)
gapbs_bc.executable = zjp_gapbs_binary_dir + 'bc'
# gapbs_bc.cmd = [gapbs_bc.executable] + ['-g', '16', '-n', '1']
gapbs_bc.cmd = [gapbs_bc.executable] + gapbs_choice

#-----------------gapbs_bfs
gapbs_bfs = Process(pid = 223)
gapbs_bfs.executable = zjp_gapbs_binary_dir + 'bfs'
# gapbs_bfs.cmd = [gapbs_bfs.executable] + ['-g', '16', '-n', '1']
gapbs_bfs.cmd = [gapbs_bfs.executable] + gapbs_choice

#-----------------gapbs_cc
gapbs_cc = Process(pid = 224)
gapbs_cc.executable = '/sdf1/songyifei/gem5-ID_IMP/gapbs/cc'
# gapbs_cc.cmd = [gapbs_cc.executable] + ['-g', '16', '-n', '1']
gapbs_cc.cmd = [gapbs_cc.executable] + gapbs_choice

#-----------------gapbs_pr
gapbs_pr = Process(pid = 225)
gapbs_pr.executable = zjp_gapbs_binary_dir + 'pr'
# gapbs_pr.cmd = [gapbs_pr.executable] + ['-g', '16', '-n', '1']
gapbs_pr.cmd = [gapbs_pr.executable] + gapbs_choice

#-----------------gapbs_tc
gapbs_tc = Process(pid = 226)
gapbs_tc.executable = zjp_gapbs_binary_dir + 'tc'
# gapbs_tc.cmd = [gapbs_tc.executable] + ['-g', '16', '-n', '1']
gapbs_tc.cmd = [gapbs_tc.executable] + gapbs_choice

zjp_graph500_binary_dir = '/sdf1/songyifei/benchmark/graph500-newreference/src/'
#-----------------zjp_add_tests
#-----------------reference_bfs
graph500_bfs = Process(pid = 220)
graph500_bfs.executable = zjp_graph500_binary_dir + 'graph500_reference_bfs'
graph500_bfs.cmd = [graph500_bfs.executable] + ['16', '16']
#-----------------zjp_test
zjp_test = Process(pid = 227)
zjp_test.executable = '/root/sde1/zhoujiapeng/Prefetchers/gem5-21.2.0.0/zjp_test_113/print_test'
zjp_test.cmd = [zjp_test.executable]

syf_spec2017_dir='/home/dengxin/benchamark/speccpu2017/benchspec/CPU/'
#-----------------mcf_r
mcf_r = Process(pid = 228)
mcf_r.executable = syf_spec2017_dir+'505.mcf_r/build/build_base_mytest-m64.0001/mcf_r'
mcf_r.cmd = [mcf_r.executable]+[syf_spec2017_dir+'505.mcf_r/data/refrate/input/inp.in']

# /home/dengxin/benchamark/speccpu2017/benchspec/CPU/505.mcf_r/build/build_base_mytest-m64.0001/mcf_r


#lbm_r
lbm_r = Process(pid = 229)
lbm_r.executable = syf_spec2017_dir+'519.lbm_r/build/build_base_mytest-m64.0001/lbm_r'
lbm_r.cmd = [lbm_r.executable]+['1000','1','0','0']

#bwaves_r
bwaves_r = Process(pid = 230)
bwaves_r.executable = syf_spec2017_dir+'503.bwaves_r/build/build_base_mytest-m64.0001/bwaves_r'
bwaves_r.cmd = [bwaves_r.executable]+['/home/dengxin/benchamark/speccpu2017/benchspec/CPU/503.bwaves_r/data/refrate/input/bwaves_2.in']

#deepsjeng_r
deepsjeng_r = Process(pid = 230)
deepsjeng_r.executable = syf_spec2017_dir+'531.deepsjeng_r/build/build_base_mytest-m64.0001/deepsjeng_r'
deepsjeng_r.cmd = [bwaves_r.executable]+[syf_spec2017_dir+'531.deepsjeng_r/data/refrate/input/ref.txt']

#nab_r
nab_r = Process(pid = 230)
nab_r.executable = syf_spec2017_dir+'544.nab_r/run/run_base_refrate_mytest-m64.0002/nab_r_base.mytest-m64'
nab_r.cmd = [nab_r.executable]+['1am0','12214447','122']

#gcc_r /home/dengxin/benchamark/speccpu2017/benchspec/CPU/502.gcc_r/build/build_base_isb-m64.0000/cpugcc_r
# /home/dengxin/benchamark/speccpu2017/benchspec/CPU/502.gcc_r/data/refrate/input/gcc-smaller.c
cpugcc_r = Process(pid = 231)
cpugcc_r.executable = syf_spec2017_dir+'502.gcc_r/build/build_base_isb-m64.0000/cpugcc_r'
cpugcc_r.cmd = [cpugcc_r.executable]+[syf_spec2017_dir+'502.gcc_r/data/refrate/input/gcc-pp.c']

# omnetpp_r
omnetpp_r = Process(pid = 231)
omnetpp_r.executable = syf_spec2017_dir+'520.omnetpp_r/build/build_base_mytest-m64.0001/omnetpp_r'
omnetpp_r.cmd = [omnetpp_r.executable]+[syf_spec2017_dir+'520.omnetpp_r/data/refrate/input/omnetpp.ini']




spec2006dir='/sdf1/songyifei/zjp/SPECcpu2006/benchspec/CPU2006/'

bzip22006 = Process(pid = 241)
bzip22006.executable = spec2006dir+'401.bzip2/exe/bzip2_base.amd64-m64-gcc41-nn'
bzip22006.cmd = [bzip22006.executable]+[spec2006dir+'401.bzip2/data/ref/input/input.source']

gcc2006 = Process(pid = 242)
gcc2006.executable = spec2006dir+'403.gcc/exe/gcc_base.amd64-m64-gcc41-nn'
gcc2006.cmd = [gcc2006.executable]+[spec2006dir+'403.gcc/data/ref/input/166.i']

mcf2006 = Process(pid = 243)
mcf2006.executable = spec2006dir+'429.mcf/exe/mcf_base.amd64-m64-gcc41-nn'
mcf2006.cmd = [mcf2006.executable]+[spec2006dir+'429.mcf/data/ref/input/inp.in']

gobmk2006 = Process(pid = 244)
gobmk2006.executable = spec2006dir+'445.gobmk/exe/gobmk_base.amd64-m64-gcc41-nn'
gobmk2006.cmd = [gobmk2006.executable]
# +[spec2006dir+'445.gobmk/data/ref/input/input.source']


hmmer2006 = Process(pid = 245)
hmmer2006.executable = spec2006dir+'456.hmmer/exe/hmmer_base.amd64-m64-gcc41-nn'
hmmer2006.cmd = [hmmer2006.executable]+[spec2006dir+'456.hmmer/data/ref/input/nph3.hmm']

libquantum2006 = Process(pid = 246)
libquantum2006.executable = spec2006dir+'462.libquantum/exe/libquantum_base.amd64-m64-gcc41-nn'
libquantum2006.cmd = [libquantum2006.executable]+[spec2006dir+'462.libquantum/data/ref/input/control']

# omnetpp2006 = Process(pid = 234)
# omnetpp2006.executable = spec2006dir+'471.omnetpp/exe/omnetpp_base.amd64-m64-gcc41-nn'
# omnetpp2006.cmd = [omnetpp2006.executable]+[spec2006dir+'471.omnetpp/data/ref/input/control']

# astar2006 = Process(pid = 234)
# astar2006.executable = spec2006dir+'473.astar/exe/astar_base.amd64-m64-gcc41-nn'
# astar2006.cmd = [astar2006.executable]+[spec2006dir+'473.astar/data/ref/input/BigLakes2048.bin']

xalancbmk2006 = Process(pid = 247)
xalancbmk2006.executable = spec2006dir+'483.xalancbmk/exe/Xalan_base.amd64-m64-gcc41-nn'
xalancbmk2006.cmd = [xalancbmk2006.executable]+[spec2006dir+'483.xalancbmk/data/ref/input/t5.xml']+[spec2006dir+'483.xalancbmk/data/ref/input/xalanc.xsl']

xalancbmk2006 = Process(pid = 247)
xalancbmk2006.executable = spec2006dir+'483.xalancbmk/exe/Xalan_base.amd64-m64-gcc41-nn'
xalancbmk2006.cmd = [xalancbmk2006.executable]+[spec2006dir+'483.xalancbmk/data/ref/input/t5.xml']+[spec2006dir+'483.xalancbmk/data/ref/input/xalanc.xsl']



hotspot_pagerank = Process(pid = 248)
hotspot_pagerank.executable = '/home/liangyangguang/CRONO/pref_apps/pagerank/pagerank'
hotspot_pagerank.cmd = [hotspot_pagerank.executable]+['0']+['1']+['3000']+['2999']

hotspot_health = Process(pid = 249)
hotspot_health.executable = '/home/dengxin/benchmark/olden/health/run'
hotspot_health.cmd = [hotspot_health.executable]+['8']+['300']+['4']


hello_world = Process(pid = 250)
hello_world.executable = '/sdc1/qinjingyuan/gem5-21.1.0.2/hello_world'
hello_world.cmd = [hotspot_health.executable]






# /home/liangyangguang/CRONO/pref_apps/pagerank/pagerank 0 1 3000 2999
# /root/sdc1/zhoujiapeng/benchmark/graph500_v2-spec/graph500_no_verify/seq-csr/seq-csr -s 16 -e 16
# /root/sdc1/zhoujiapeng/benchmark/NPB3.3.1/NPB3.3-SER/bin/cg.A.x
# /root/sdc1/zhoujiapeng/benchmark/libquantum_base.amd64-m64-gcc42-nn 1000
# /home/dengxin/benchmark/spec2017/benchspec/CPU/505.mcf_r/exe/mcf_r_base.mytest-m64 /home/dengxin/benchmark/spec2017/benchspec/CPU/505.mcf_r/data/test/input/inp.in
# /home/dengxin/benchmark/olden/health/run 8 300 4






