from subprocess import call
import libvirt
import time

templates = {"fuel": {
    "cpu": "host",
    "ram": "8192",
    "vcpus": "4,cores=4",
    "os-type": "linux",
    "os-variant": "rhel6",
    "boot": "cdrom,hd",
    "graphics": "vnc,listen=0.0.0.0",
    "noautoconsole": ""},
    }

# Example of dictionary with VM(s)
# vm_desc = { "vm_name": "fuel-test",
#             "vm_template":"fuel",
#             "vm_params":{
#                        "cdrom" : "/var/lib/libvirt/images/fuel-master-505-2014-09-09_00-01-11.iso",
#                        "noautoconsole" : "",
#             "vm_nics":{
#                    "nic1" : "network=10g-1,model=virtio",
#                    "nic2" : "network=1g-1,model=virtio,mac=00:01:02:03:04:05",
#             },
#             "vm_opts":{
#                "host" : "172.16.44.4",
#                "host_proto" : "qemu+tcp",
#                "virttype" : "kvm",
#                "disksize" : "50",
#             }
#            "need_to_poweron": True,
#
#          }

def deploy_vm(vm):
    storage_pool = "default"
    vm_name = vm["name"]
    vm_opts = vm["opts"]
    vm_params = dict(templates[vm["template"]],**vm["params"])
    vm_nics = vm["nics"]
    hypervisor = vm_opts["host_proto"]+"://"+vm_opts["host"]+"/system"

    params = " --name "+vm_name+\
             " --connect "+hypervisor+\
             " --virt-type "+vm_opts["virttype"]+\
             " --disk pool="+storage_pool+",format=qcow2,size="+vm_opts["disksize"]

    for param in vm_params:
        params += " --"+param+("="+vm_params[param] if (len(vm_params[param])>0) else "")

    for nic in vm_nics: params += " --network "+vm_nics[nic]

    try:
        call("virt-install"+params,shell=True)
        if vm["need_to_poweron"]:
            hypervisor = vm_opts["host_proto"]+"://"+vm_opts["host"]+"/system"
            conn = libvirt.open(hypervisor)
            while (not conn.lookupByName(vm_name).info()[0] == 5): time.sleep(5)
            power_on_vm(vm)
    except:
        print "There is a problem with virt-install run. Have you installed virt-inst package?"

def power_on_vm(vm):
        import ipdb;ipdb.set_trace()
        vm_name = vm["name"]
        vm_opts = vm["opts"]
        hypervisor = vm_opts["host_proto"]+"://"+vm_opts["host"]+"/system"
        conn = libvirt.open(hypervisor)
        if conn.lookupByName(vm_name).info()[0] == 5:
            conn.lookupByName(vm_name).create()
            print "VM",vm_name,"is powered on now"
        else:
            print "VM",vm_name,"is already powered on"

def power_off_vm(vm):
    vm_name = vm["name"]
    vm_opts = vm["opts"]
    hypervisor = vm_opts["host_proto"]+"://"+vm_opts["host"]+"/system"
    conn = libvirt.open(hypervisor)
    if conn.lookupByName(vm_name).info()[0] == 1:
        conn.lookupByName(vm_name).destroy()
        print "VM",vm_name,"is powered off now"
    else:
        print "VM",vm_name,"is already powered off"


def delete_vm(vm):
    storage_pool="default"
    vm_name = vm["name"]
    vm_opts = vm["opts"]
    hypervisor = vm_opts["host_proto"]+"://"+vm_opts["host"]+"/system"
    conn = libvirt.open(hypervisor)
    if conn.lookupByName(vm_name):
        power_off_vm(vm)
        conn.lookupByName(vm_name).undefine()
        conn.storagePoolLookupByName(storage_pool).storageVolLookupByName(vm_name+".img").delete()

def modify_vm():