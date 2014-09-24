from subprocess import call
import libvirt
import time
import paramiko
import StringIO

def upload_image(iso,node,storage_path):

    iso_name = iso["name"]
    iso_url = iso["url"]
    node_ip = node["ip"]
    node_username = node["username"]
    node_key = node["key"]

    f = StringIO.StringIO(node_key)
    private_key = paramiko.RSAKey.from_private_key(f)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(node_ip, username=node_username,pkey=private_key)

    # checking that image exists
    stdin,stdout,stderr = ssh.exec_command("ls -l "+storage_path+"|grep -c "+iso_name)

    if int(stdout.read().rstrip()) < 1:
        ssh.exec_command("mkdir -p "+storage_path)
        stdin,stdout,stderr = ssh.exec_command("wget -O "+storage_path+"/"+iso_name+" "+iso_url)
        print "Image downloaded.Info: \n",stdout.read()
    else:
        print "Image is already exists"

    f.close()
    ssh.close()

def images_clean_up():
    print "bbbb"