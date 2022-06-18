# Authors: Steve Reinhardt

# Simple test script
#
# "m5 test.py"

from __future__ import print_function
from __future__ import absolute_import

import argparse
import sys
# import sys
# sys.setdefaultencoding('utf8')
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal, warn

'''
addToPath('../common')
addToPath('../ruby')
addToPath('../topologies')
'''

addToPath('../')

import common.Options as Options
import ruby.Ruby as Ruby
import common.Simulation as Simulation
import common.MemConfig as MemConfig
# from Caches import *
from common.cpu2000 import *
# import common.Mybench as cpu2006
import common.MyCRONO as crono
# import common.MyNPB as npb

class L1Cache(Cache):
    # 相连度
    assoc = 4
    # 标记查找延时
    tag_latency = 2
    # 数据访问延时
    data_latency = 1
    # 未命中时返回路径的延时
    response_latency = 1
    # 最大未完成请求数
    mshrs = 4
    # 每个mshr最大访问次数
    tgts_per_mshr = 20

class L1_ICache(L1Cache):
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True
    # size = '64KB'

class L1_DCache(L1Cache):
    # size = '64KB'
    pass

class L2Cache(Cache):
    # size = '512KB'
    assoc = 8
    tag_latency = 4
    data_latency = 3
    response_latency = 3
    mshrs = 20
    tgts_per_mshr = 12
    write_buffers = 8

class L3Cache(Cache):
    # size = '2048KB'
    assoc = 16
    tag_latency = 6
    data_latency = 6
    response_latency = 6
    mshrs = 20
    tgts_per_mshr = 12
    write_buffers = 8

class IOCache(Cache):
    assoc = 8
    tag_latency = 50
    data_latency = 50
    response_latency = 50
    mshrs = 20
    size = '1kB'
    tgts_per_mshr = 12

class PageTableWalkerCache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 10
    size = '1kB'
    tgts_per_mshr = 12

    # the x86 table walker actually writes to the table-walker cache
    if buildEnv['TARGET_ISA'] == 'x86':
        is_read_only = False
    else:
        is_read_only = True
        # Writeback clean lines as well
        writeback_clean = True

def config_cache(options, system):
    if options.external_memory_system and (options.caches or options.l2cache):
        print("External caches and internal caches are exclusive options.\n")
        sys.exit(1)

    if options.external_memory_system:
        ExternalCache = ExternalCacheFactory(options.external_memory_system)

    if options.cpu_type == "O3_ARM_v7a_3":
        print("O3_ARM_v7a_3 is unavailable. Did you compile the O3 model?")
        sys.exit(1)

        dcache_class, icache_class, l2_cache_class, walk_cache_class = \
            O3_ARM_v7a_DCache, O3_ARM_v7a_ICache, O3_ARM_v7aL2, \
            O3_ARM_v7aWalkCache
    else:
        dcache_class, icache_class, l2_cache_class, \
            l3_cache_class, walk_cache_class = \
            L1_DCache, L1_ICache, L2Cache, L3Cache, None

        if buildEnv['TARGET_ISA'] == 'x86':
            walk_cache_class = PageTableWalkerCache

    # Set the cache line size of the system
    system.cache_line_size = options.cacheline_size

    # If elastic trace generation is enabled, make sure the memory system is
    # minimal so that compute delays do not include memory access latencies.
    # Configure the compulsory L1 caches for the O3CPU, do not configure
    # any more caches.
    if options.l3cache and options.elastic_trace_en:
        fatal("When elastic trace is enabled, do not configure L3 caches.")

    if options.l3cache:
        # Provide a clock for the L2 and the L1-to-L2 bus here as they
        # are not connected using addTwoLevelCacheHierarchy. Use the
        # same clock as the CPUs.
        system.l3 = l3_cache_class(clk_domain=system.cpu_clk_domain,
                                   size=options.l3_size,
                                   assoc=options.l3_assoc)

        if options.l3prefetcher:
            exec("system.l3.prefetcher = %s"%options.l3prefetcher)

        system.tol3bus = L2XBar(clk_domain = system.cpu_clk_domain)
        system.l3.cpu_side = system.tol3bus.mem_side_ports
        system.l3.mem_side = system.membus.cpu_side_ports

    if options.memchecker:
        system.memchecker = MemChecker()

    for i in range(options.num_cpus):
        if options.caches:
            icache = icache_class(size=options.l1i_size,
                                  assoc=options.l1i_assoc)
            dcache = dcache_class(size=options.l1d_size,
                                  assoc=options.l1d_assoc)

            # If we have a walker cache specified, instantiate two
            # instances here
            if walk_cache_class:
                iwalkcache = walk_cache_class()
                dwalkcache = walk_cache_class()
            else:
                iwalkcache = None
                dwalkcache = None

            if options.memchecker:
                dcache_mon = MemCheckerMonitor(warn_only=True)
                dcache_real = dcache

                # Do not pass the memchecker into the constructor of
                # MemCheckerMonitor, as it would create a copy; we require
                # exactly one MemChecker instance.
                dcache_mon.memchecker = system.memchecker

                # Connect monitor
                dcache_mon.mem_side = dcache.cpu_side

                # Let CPU connect to monitors
                dcache = dcache_mon
            
            # When connecting the caches, the clock is also inherited
            # from the CPU in question
            system.cpu[i].addPrivateSplitL1Caches(icache, dcache,
                                                  iwalkcache, dwalkcache)

            if options.memchecker:
                # The mem_side ports of the caches haven't been connected yet.
                # Make sure connectAllPorts connects the right objects.
                system.cpu[i].dcache = dcache_real
                system.cpu[i].dcache_mon = dcache_mon

        elif options.external_memory_system:
            # These port names are presented to whatever 'external' system
            # gem5 is connecting to.  Its configuration will likely depend
            # on these names.  For simplicity, we would advise configuring
            # it to use this naming scheme; if this isn't possible, change
            # the names below.
            if buildEnv['TARGET_ISA'] in ['x86', 'arm']:
                system.cpu[i].addPrivateSplitL1Caches(
                        ExternalCache("cpu%d.icache" % i),
                        ExternalCache("cpu%d.dcache" % i),
                        ExternalCache("cpu%d.itb_walker_cache" % i),
                        ExternalCache("cpu%d.dtb_walker_cache" % i))
            else:
                system.cpu[i].addPrivateSplitL1Caches(
                        ExternalCache("cpu%d.icache" % i),
                        ExternalCache("cpu%d.dcache" % i))

        system.cpu[i].createInterruptController()
        if options.l1dprefetcher:
            exec("system.cpu[i].dcache.prefetcher = %s"%options.l1dprefetcher)            
        if options.l1iprefetcher:
            exec("system.cpu[i].icache.prefetcher = %s"%options.l1iprefetcher)
        if options.l2cache and options.l3cache:
            system.cpu[i].l2 = l2_cache_class(clk_domain=system.cpu_clk_domain,
                                       size=options.l2_size,
                                       assoc=options.l2_assoc)
            if options.l2prefetcher:
                exec("system.cpu[i].l2.prefetcher = %s"%options.l2prefetcher)

            system.cpu[i].tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
            system.cpu[i].l2.cpu_side = system.cpu[i].tol2bus.mem_side_ports
            system.cpu[i].l2.mem_side = system.tol3bus.cpu_side_ports
            system.cpu[i].connectAllPorts(system.cpu[i].tol2bus, system.membus)
            # system.cpu[i].connectAllPorts(
            #     system.cpu[i].tol2bus.cpu_side_ports,
            #     system.membus.cpu_side_ports, system.membus.mem_side_ports)
        elif options.l2cache:
            system.cpu.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain,
                                           size=options.l2_size,
                                           assoc=options.l2_assoc)

            system.cpu.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
            system.cpu.l2.cpu_side = system.cpu.tol2bus.mem_side_ports
            system.cpu.l2.mem_side = system.membus.cpu_side_ports
            system.cpu.connectAllPorts(system.cpu[i].tol2bus, system.membus)
        elif options.external_memory_system:
            system.cpu[i].connectUncachedPorts(
                system.membus.cpu_side_ports, system.membus.mem_side_ports)
        else:
            system.cpu[i].connectBus(system.membus)

    return system

'''
this is now add, different from se_spec2006.py
same in prefetcher_exp.py
check if KVM support has been enabled, we might need to do VM
'''
have_kvm_support = 'BaseKvmCPU' in globals()
def is_kvm_cpu(cpu_class):
    return have_kvm_support and cpu_class != None and \
        issubclass(cpu_class, BaseKvmCPU)

def get_processes(options):
    """Interprets provided options and returns a list of processes"""

    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []

    workloads = options.cmd.split(';')
    if options.input != "":
        inputs = options.input.split(';')
    if options.output != "":
        outputs = options.output.split(';')
    if options.errout != "":
        errouts = options.errout.split(';')
    if options.options != "":
        pargs = options.options.split(';')

    idx = 0
    for wrkld in workloads:
        process = Process(pid = 100 + idx)
        process.executable = wrkld
        process.cwd = os.getcwd()

        if options.env:
            with open(options.env, 'r') as f:
                process.env = [line.rstrip() for line in f]

        if len(pargs) > idx:
            process.cmd = [wrkld] + pargs[idx].split()
        else:
            process.cmd = [wrkld]

        if len(inputs) > idx:
            process.input = inputs[idx]
        if len(outputs) > idx:
            process.output = outputs[idx]
        if len(errouts) > idx:
            process.errout = errouts[idx]

        multiprocesses.append(process)
        idx += 1

    if options.smt:
        assert(options.cpu_type == "DerivO3CPU" or 
                options.cpu_type == "detailed" or 
                options.cpu_type == "inorder")
        return multiprocesses, idx
    else:
        return multiprocesses, 1

#get path 
config_path = os.path.dirname(os.path.abspath(__file__))
config_root = os.path.dirname(config_path) + "/configs"
m5_root = os.path.dirname(config_root)

# parser = optparse.OptionParser()
parser = argparse.ArgumentParser(
    description="My configuration script to run the gapbs benchmarks."
)

Options.addCommonOptions(parser)

Options.addSEOptions(parser)
parser.add_argument("--l3cache",action="store_true")
parser.add_argument("--l1dprefetcher",action="store",
                  dest="l1dprefetcher",default=None)
parser.add_argument("--l1iprefetcher",action="store",
                  dest="l1iprefetcher",default=None)
parser.add_argument("--l2prefetcher",action="store",
                  dest="l2prefetcher",default=None)
parser.add_argument("--l3prefetcher",action="store",
                  dest="l3prefetcher",default=None)
parser.add_argument("-b", "--benchmark", help="The SPEC benchmark to be loaded.")
parser.add_argument("--checkpoint_dir",action="store",
                  dest="checkpoint_dir",default=None)
#parser.add_option("-c", "--chkpt", default="", help="The checkpoint to load.")
#parser.add_option("--benchmark_stdout", type="string", default="", help="Absolute path for stdout redirection for the benchmark.")
#parser.add_option("--benchmark_stderr", type="string", default="", help="Absolute path for stderr redirection for the benchmark.")

#execfile(os.path.join(config_root, "configs", "Options.py"))

if '--ruby' in sys.argv:
    Ruby.define_options(parser)

# print(parser.parse_args())
args = parser.parse_args()
# print(args.cmd)
# (options, args) = parser.parse_args()


# if args:
#     print("Error: script doesn't take any positional arguments")
#     sys.exit(1)

multiprocesses = []
numThreads = 1
apps = []
process = []

if args.bench:
    apps = args.bench.split("-")
    if len(apps) != args.num_cpus:
        print("number of benchmarks not equal to set num_cpus!")
        sys.exit(1)

    #for app in apps:
    for index,app in enumerate(apps): 
        try:
            if buildEnv['TARGET_ISA'] == 'x86':
                # print("is X86 struct")
                
                if app == 'apsp':
                    process.append(crono.apsp)
                elif app == 'cpugcc_r':
                    process.append(crono.cpugcc_r)
                elif app == 'bc':
                    process.append(crono.bc)
                elif app == 'bfs':
                    process.append(crono.bfs)
                elif app == 'community':                    
                    process.append(crono.community)
                elif app == 'c_c':
                    process.append(crono.connected_components)
                elif app == 'dfs':
                    process.append(crono.dfs)
                elif app == 'pagerank':
                    process.append(crono.pagerank)
                elif app == 'sssp':
                    process.append(crono.sssp)
                elif app == 't_c':
                    process.append(crono.triangle_counting)
                elif  app == 'tsp':
                    process.append(crono.tsp)
                elif app == 'gapbs_sssp':
                    process.append(crono.gapbs_sssp)
                elif app == 'gapbs_bc':
                    process.append(crono.gapbs_bc)
                elif app == 'gapbs_bfs':
                    process.append(crono.gapbs_bfs)
                elif app == 'gapbs_cc':
                    process.append(crono.gapbs_cc)
                elif app == 'gapbs_pr':
                    process.append(crono.gapbs_pr)
                elif app == 'gapbs_tc':
                    process.append(crono.gapbs_tc)
                elif app == 'zjp_test':
                    process.append(crono.zjp_test)
                elif app == 'mcf_r':
                    process.append(crono.mcf_r)
                elif app == 'lbm_r':
                    process.append(crono.lbm_r)
                elif app == 'bwaves_r':
                    process.append(crono.bwaves_r)
                elif app == 'deepsjeng_r':
                    process.append(crono.deepsjeng_r)
                elif app == 'nab_r':
                    process.append(crono.nab_r)
                
                elif app == 'bzip22006':
                    process.append(crono.bzip22006)
                elif app == 'gcc2006':
                    process.append(crono.gcc2006)
                elif app == 'mcf2006':
                    process.append(crono.mcf2006)
                elif app == 'gobmk2006':
                    process.append(crono.gobmk2006)
                elif app == 'hmmer2006':
                    process.append(crono.hmmer2006)
                elif app == 'libquantum2006':
                    process.append(crono.libquantum2006)
                elif app == 'xalancbmk2006':
                    process.append(crono.xalancbmk2006)
                elif app == 'hotspot_pagerank':
                    process.append(crono.hotspot_pagerank)
                elif app == 'hotspot_health':
                    process.append(crono.hotspot_health)
                elif app == 'hello_world':
                    process.append(crono.hello_world)
                    
                
                multiprocesses.append(process[index])
            else:
                exec("workload = %s(buildEnv['TARGET_ISA'], 'linux', 'ref')" % app)
                multiprocesses.append(workload.makeProcess())
        except:
            print("Unable to find workload. Exiting!\n", file=sys.stderr)
            sys.exit(1)
elif args.cmd:
    multiprocesses, numThreads = get_processes(args)
else:
    print("No workload specified. Exiting!\n")
    sys.exit(1)

'''
if options.chkpt != "":
    process.chkpt = options.chkpt
'''

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(args)
CPUClass.numThreads = numThreads

#TODO: ?? if delete ?
#MemClass = Simulation.setMemClass(options)
#if MemClass == SimpleMemory:
#    MemClass.latency = options.latency
#    MemClass.bandwidth = options.bandwidth


# Check -- do not allow SMT with multiple CPUs
if args.smt and args.num_cpus > 1:
    fatal("You cannot use SMT with multiple CPUs!")

np = args.num_cpus
mp0_path = multiprocesses[0].executable
system = System(cpu = [CPUClass(cpu_id=i) for i in range(np)],
                        mem_mode = test_mem_mode,
                        mem_ranges = [AddrRange(args.mem_size)],
                        cache_line_size = args.cacheline_size)

if numThreads > 1:
    system.multi_thread = True

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = args.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  args.sys_clock,  voltage_domain = system.voltage_domain)
# system.clk_domain = SrcClockDomain(clock =  '1GH',  voltage_domain = system.voltage_domain)
# system.clk_domain = SrcClockDomain()
# system.clk_domain.clock = '1GHz'
# system.clk_domain.voltage_domain = VoltageDomain()

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = args.cpu_clock,
                                       voltage_domain =
                                       system.cpu_voltage_domain)

# system.cpu_clk_domain = SrcClockDomain()
# system.cpu_clk_domain.clock = '1GHz'
# system.cpu_clk_domain.voltage_domain = VoltageDomain()



#TODO:add on this ??
if args.elastic_trace_en:
    CpuConfig.config_etrace(CPUClass, system.cpu, args)

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

if is_kvm_cpu(CPUClass) or is_kvm_cpu(FutureClass):
    if buildEnv['TARGET_ISA'] == 'x86':
        system.kvm_vm = KvmVM()
        for process in multiprocesses:
            process.useArchPT = True;
            process.kvmInSE = True;
    else:
        fatal("KvmCPU can only be used in SE mode with x86")

# Sanity check
'''
if options.fastmem:
    if CPUClass != AtomicSimpleCPU:
        fatal("Fastmem can only be used with atomic CPU!")
    if (options.caches or options.l2cache):
        fatal("You cannot use fastmem in combination with caches!")
'''

if args.simpoint_profile:
    if not options.fastmem:
        # Atomic CPU checked with fastmem option already
        fatal("SimPoint generation should be done with atomic cpu and fastmem")
    if np > 1:
        fatal("SimPoint generation not supported with more than one CPUs")

for i in range(np):
    if args.smt:
        system.cpu[i].workload = multiprocesses
    elif len(multiprocesses) == 1:
        system.cpu[i].workload = multiprocesses[0]
    else:
        system.cpu[i].workload = multiprocesses[i]

    #if options.fastmem:
    #    system.cpu[i].fastmem = True

    #TODO: some different
    if args.simpoint_profile:
        #system.cpu[i].simpoint_profile = True
        #system.cpu[i].simpoint_interval = options.simpoint_interval
        system.cpu[i].addSimPointProbe(args.simpoint_interval)

    if args.checker:
        system.cpu[i].addCheckerCpu()

    system.cpu[i].createThreads()


if args.ruby:
    print("unsupport ruby!")
    exit(0)
else:
    MemClass = Simulation.setMemClass(args)
    system.membus = SystemXBar()
    system.system_port = system.membus.cpu_side_ports
    config_cache(args, system)
    MemConfig.config_mem(args, system)

system.workload = SEWorkload.init_compatible(mp0_path)

root = Root(full_system = False, system = system)
Simulation.run(args, root, system, FutureClass)
