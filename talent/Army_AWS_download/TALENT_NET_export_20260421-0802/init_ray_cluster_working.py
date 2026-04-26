# === Reusable Ray Initialization ===
import os, ray


def init_ray_cluster(cpus=12, obj_store_gb=40, temp_dir="/tmp/ray_tmp",dis_mem_mon="0"):
    """
    Cleanly initializes Ray with safe defaults for systems with 16 CPUs and ~124 GiB RAM.
    Args:
        cpus (int): Number of CPUs Ray can use.
        obj_store_gb (int): Shared memory size for object store in GiB.
        tem_dir (str): Temporary directory for Ray spillover.
    Usage:
        init_ray_cluster() # Initializes Ray for your system.
    """
    from functionsG import print_syntax
    
    os.environ["MODIN_ENGINE"] = "ray"
    # Note: RAY_OBJECT_STORE_MEMORY is better set via ray.init(object_store_memory=...) parameter
    # os.environ["RAY_OBJECT_STORE_MEMORY"] = str(obj_store_gb * 1024 **3)
    # Memory monitor: "0" = enabled (recommended for OOM prevention), "1" = disabled
    # Enabling memory monitor helps prevent OOM by killing workers before system runs out of memory
    os.environ["RAY_DISABLE_MEMORY_MONITOR"] = dis_mem_mon  # Use parameter instead of hardcoded "1"
    os.environ["RAY_TEMPDIR"] = temp_dir
    
    try:
        ray.init(
    		num_cpus=cpus,
            object_store_memory=obj_store_gb * (1024 **3),
    		ignore_reinit_error=True,
    		)
        code_str = f"def init_ray_cluster(cpus={cpus}, obj_store_gb={obj_store_gb}, temp_dir='{temp_dir}',dis_mem_mon='{dis_mem_mon}'):"
        print(f"Ray initialized with {cpus} CPUs and {obj_store_gb} GiB object store with temp_dir='{temp_dir}', and with memory monitor {'disbaled' if dis_mem_mon =='1' else 'enabled'}")
        print("USING:")
        print_syntax(code_str, lang='python')
    except ConnectionError:
        print("Could not connect to a local Ray instance")
    except Exception as e:
        print(f"An unexpected error occurred during Ray initializaion: {e}")
