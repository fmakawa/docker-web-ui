import platform,socket,re,uuid,json,psutil,GPUtil,logging
import sqlite3
import docker
from datetime import datetime, date
from flask import render_template, Flask,request
from sqlite3 import Error
from web.models.models import Drolex
from web.database import workdir
from web import app
from web.routes_util.containers import docker_client, container_detail, removed_containers


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getSystemInfo():
    try:
        # System Info
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        # Boot Time
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        info['boot-time'] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        
        # CPU Info
        cpu = {}
        # number of cores
        cpu['physical_cores'] = psutil.cpu_count(logical=False)
        cpu['total_cores'] = psutil.cpu_count(logical=True)
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        cpu['max _frequency'] = cpufreq.max
        cpu['min_frequency'] = cpufreq.min
        cpu['current_frequency'] = cpufreq.current
        # CPU usage
        # CPU Usage Per Core
        cores = {}
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cores[f'core {i}'] = percentage
        cpu['cores'] = cores
        cpu['totalcpu_usage'] = str(psutil.cpu_percent())
        info['cpu'] = cpu
        
        # Memory Usage
        memory = {}
        # memory ram
        svmem = psutil.virtual_memory()
        memory['total'] =  get_size(svmem.total)
        # print('total_memory: ' + get_size(svmem.total))
        memory['available'] = get_size(svmem.available)
        memory['used'] = get_size(svmem.used)
        memory['percentage'] = svmem.percent
        # swap
        swap = psutil.swap_memory()
        memory['swap_total'] = get_size(swap.total)
        memory['swap_free'] = get_size(swap.free)
        memory['swap_used'] = get_size(swap.used)
        memory['swap_percentage'] = swap.percent
        info['memory'] = memory
        
        # Disk Usage
        disk_usage = {}
        # partitions
        partitions = psutil.disk_partitions()
        partitions_list = []
        for partition in partitions:
            partition_info = {}
            partition_info['device'] = partition.device
            partition_info['mountpoint'] = partition.mountpoint
            partition_info['file_system_type'] = partition.fstype
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be caught due to the disk that isn't ready
                continue
            partition_info['total_size'] = get_size(partition_usage.total)
            partition_info['partition_used'] = get_size(partition_usage.used)
            partition_info['free'] = get_size(partition_usage.free)
            partition_info['percentage'] = partition_usage.percent
            partitions_list.append(partition_info)
        disk_usage['partitions'] = partitions_list
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        disk_usage['total_read'] = get_size(disk_io.read_bytes)
        # print('total_read: ' + str(get_size(disk_io.read_bytes)))
        disk_usage['total_write'] = get_size(disk_io.write_bytes)
        info['disk_usage'] = disk_usage

        # Network information
        network = {}
        if_addrs = psutil.net_if_addrs()
        interfaces = []
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                interface = {}
                if str(address.family) == 'AddressFamily.AF_INET':
                    interface['name'] = interface_name
                    interface['ip_address'] = address.address
                    interface['netmask'] = address.netmask
                    interface['broadcast_ip'] = address.broadcast
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    interface['name'] = interface_name
                    interface['mac_address'] = address.address
                    interface['netmask'] = address.netmask
                    interface['broadcast_mac'] = address.broadcast
                else:
                    # print(interface_name) # needs to be logged
                    # print(address) # need to be logged
                    pass
                if 'veth' not in interface_name and interface:
                    interfaces.append(interface)
        # get IO statistics since boot
        network['interfaces'] = interfaces
        net_io = psutil.net_io_counters()
        network['total_bytes_Sent'] = get_size(net_io.bytes_sent)
        network['total_bytes_received'] = get_size(net_io.bytes_recv)
        info['network'] = network
        # GPU information
        gpus = GPUtil.getGPUs()
        gpus_data = []
        if gpus != None or gpus != 'Null' :
            for gpu in gpus:
                # get the GPU id
                gpu_id = gpu.id
                # name of GPU
                gpu_name = gpu.name
                # get % percentage of GPU usage of that GPU
                gpu_load = f"{gpu.load*100}%"
                # get free memory in MB format
                gpu_free_memory = f"{gpu.memoryFree}MB"
                # get used memory
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                # get total memory
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                # get GPU temperature in Celsius
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                
                data={
                    'id':gpu_id,
                    'name':gpu_name,
                    'load':gpu_load,
                    'free_memory':gpu_free_memory,
                    'used_memory':gpu_used_memory,
                    'total_memory':gpu_total_memory,
                    'temperature':gpu_temperature,
                    'uuid':gpu_uuid
                    }
                gpus_data.append(data)
        info['gpus']=gpus_data
        # print("="*40 + " System Info " + "="*40)
        # print(json.dumps(info, indent=2))
        # print("="*40 + " System Info END " + "="*40)
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

def docker_info_detail():
    info = docker_client().info()
    # print("="*40 + " INFO " + "="*40) 
    # print(json.dumps(info, indent=2))
    # print("="*40 + " INFO END " + "="*40)
    return info

def docker_df_detail():
    df = docker_client().df()
    # print("="*40 + " DF " + "="*40)
    # print(json.dumps(df, indent=2))
    # print("="*40 + " DF END " + "="*40)
    return df

def docker_stats_detail():
    containerz = docker_client().containers(all=True)
    container_id = []
    data = json.loads(getSystemInfo())
    stats = {}
    memory = 0
    num_cores = data['cpu']['physical_cores']
    cpu_usage = 0 
    core_cpu_usage = {}
    k = 0
    while k < num_cores:
        core_cpu_usage[k] = 0
        k += 1
    usage_kernel_mode = 0
    usage_user_mode = 0
    num_procs = 0
    memory_con = {}
    cpu_usage_con = {}
    for container in containerz:
        container_id.append(container['Id'])
        name = container['Names'][0].replace("/", "")
        stats[name] = docker_client().stats(container['Id'], stream=False)
        #print(docker_client().stats(container['Id'], stream=False))
        stats_json = docker_client().stats(container['Id'], stream=False)
        if stats_json['memory_stats']:
            memory += int(stats_json['memory_stats']['usage'])
            memory_con[name] = stats_json['memory_stats']['usage']
        cpu_usage += stats_json['cpu_stats']['cpu_usage']['total_usage']
        cpu_usage_con[name] = stats_json['cpu_stats']['cpu_usage']['total_usage']
        num_procs += stats_json['num_procs']
        usage_kernel_mode += stats_json['cpu_stats']['cpu_usage']['usage_in_kernelmode']
        usage_user_mode += stats_json['cpu_stats']['cpu_usage']['usage_in_usermode']
        if 'percpu_usage' in stats_json['cpu_stats']['cpu_usage']:
            i = 0
            while i < num_cores:
                core_cpu_usage[i] += stats_json['cpu_stats']['cpu_usage']['percpu_usage'][i] 
                i += 1

    #print("="*40 + " STATS " + "="*40)
    #print(json.dumps(stats, indent=2))
    #print("="*40 + " STATS END " + "="*40)

    # Only running and restarting app use CPU and RAM and network. ALL use disk space
     
    return stats, memory, cpu_usage,usage_kernel_mode, usage_user_mode, num_procs, core_cpu_usage

@app.route('/system/overview')
def system():
    # Get Data
    system = json.loads(getSystemInfo())
    
    info=docker_info_detail()

    stats=docker_stats_detail()

    return render_template(
        "test.html",
        section='system',
        system=system,
        info=info,
        stats=stats[0],
        memory=stats[1],
        cpu_usage=stats[2],
        sage_kernel_mode=stats[3], 
        usage_user_mode=stats[4],
        num_procs=stats[5],
        core_cpu_usage=stats[6],
    )

@app.route('/system/info')
def dk_info():
    
    info=json.dumps(docker_info_detail())

    return render_template(
        "system_overview/system_info.html",
        section='system',
        info=info,
    )

@app.route('/system/df')
def df():

    # Get Data
    params = container_detail()
    
    system = json.loads(getSystemInfo())
    
    info=docker_info_detail()

    df=docker_df_detail()

    stats=docker_stats_detail()

    return render_template(
        "test.html",
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
        dockerweb = params[6],
        removed_containers=removed_containers,
        section='system',
        system=system,
        info=info,
        stats=stats,
        df = df
    )

@app.route('/system/stats')
def stats():
    # Get Data
    params = container_detail()
    
    system = json.loads(getSystemInfo())
    
    info=docker_info_detail()

    df=docker_df_detail()

    stats=docker_stats_detail()

    return render_template(
        "test.html",
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
        dockerweb = params[6],
        removed_containers=removed_containers,
        section='system',
        system=system,
        info=info,
        stats=stats,
        df = df
    )
