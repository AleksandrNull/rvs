from vm_handle import deploy_vm, delete_vm, power_on_vm
from image_handling import upload_image

iso = {
    "name" : "fuel-test.iso",
    "url" : "http://download.onkyo.com/AVR0008/ONKAVR0008_00EAEAEA00EA_122.zip"
}

node = {
    "ip" : "172.16.44.4",
    "username" : "alwex",
    "key" : "-----BEGIN RSA PRIVATE KEY-----\n\
MIIEewIBAAKB+QZpjjBIMLqQe/qLdvmRHEEfs4Op+wC8pCQ+TlDrl7sSRXB9FZb4\n\
fbJ9qQbVOgNT/2LdtGpSJneuCkiJHtBior678obTw53TCT97ap3H44x948mKP4hc\n\
3yv+jbHugtjFQCx4Gp1Ey0Dcyv6qPeASLbEmSbHtj8Dp6lJ06nbELMU1n9XMTNvf\n\
0dbOKuofoFNQLSunQDndfFHUQsPFwV5V6KUEWFwihW1j62b2YQVs5P5AG9Y84NpE\n\
wNzOt0F0lnaEZVwfWQtcNSq3CILTDF8TuH9JemTRaMBMX/F1cmVEotu2D1wbQzbT\n\
xKKW5NmZPazKhdoM7zB1JfXGTwIDAQABAoH5Aj8FhNo035VvKHOkKIXxXMqrCmsH\n\
ttldsih1LJlqXChpVJ8saeb/uP+VrwQQP0w0QMCiyz+do/y+M2x888gpdCDIMvyJ\n\
IIblTWyBC2YSyorquRWJbc4CixmvLu36vc5SzYEA6ahIfp8ZKJ4f8JbNlKlx1Tb/\n\
TTdjUqEL5K6tythvOFzVhKYr3LS7J9AlqBON98tQbN46SOODGlK4Dz6bh+b21CaH\n\
TS4OTEraEhubVScHrU4kn265AJBzQ6lc5Xj6z6Q/As6MIWdum3gr/Q1YXFVruYwl\n\
Y2JJ73TnHodT3p3BZ95p413L+9zrnePdMpQ0a3V3tFjrcRDxAn0Dn8Neu+4agQ00\n\
3NOEAgbtyp50amNRXSGBPXEWE78iQvzn/xaMm3ntcVuYk1T5tQJ7m/h/9mPYqFli\n\
XUqTW8//N+EfEKSGFKPdFKJWFKioNBrUfWaIsVwJYjrbIEHh85HwZs7NULQMKpT8\n\
6cKqsnRCkq2zkCO75O3lDl7NCQJ9AcT1XqgJPKoUlv2W7RICl+LXFyymIaE2GswK\n\
auI4mC6X86E+9BxwDDQzGWXOBKyrfJItdMyIr1Yo0ZzRlqHidWWOEiDHWtXFlbs/\n\
BPF0rpeTVAMhyb023CHHvYf4pv4Z96nQKUEylQxS2Nu52m1xqp//EBoO1jIbCScf\n\
ppcCfQIQUGj6C7T8GFEqDyj1Hoz6/RC+JKCIsDOwkV1JEWapTuutz2FyiBQ2oTpZ\n\
a+JmuWs6fmAgJuuRspTZG0ae2es0HvZZu9a+mjGjNm5ehUyDn2OxpVnh5c9SKMHv\n\
tJS+5zRG1y0D8AOdnAoJ89jQlnPyowfF5RNyYiY18LZBAn0BIw6IRHGrCZ8xZsIU\n\
k/4WmyybN5WJBo49qd8Hz1WOdGIvqu1I7v0Q2nn7V++KEWogIc4Tv1oVUMfp6VrD\n\
8EIULa2c+HMhazwLesaD5qOTjNKeqWSMvYkC6rHul/CvXZhSDEw2Ni7Kl6CkuIw0\n\
Tx87BJRhRF1ERe4Zc4pjAQJ9AZ2JRbsvvb/duZjIcz1heP5iSACRsdO7CJTZw488\n\
4WMV4bzSJOegj1RFjdq2dokba8iWSNOYrcRbTC1LJIORa0a/aCCYhzcoTn69CbF5\n\
IuQi+GuoK9O1VLcm8D2QiCtbE+3AWFMBT346DDQ34218NWU/BE6mUX8XQ7Q6WUA=\n\
-----END RSA PRIVATE KEY-----"

}

storage_path = "/tmp"

# Example of dictionary with VM(s)
vm_desc = {
                "name": "fuel-test",
                "template": "fuel",
                "need_to_poweron": True,
                "params": {
                        "cdrom": "/var/lib/libvirt/images/fuel-master-505-2014-09-09_00-01-11.iso",
                },
                "nics": {
                    "nic1": "network=10g-1,model=virtio",
                    "nic2": "network=1g-1,model=virtio,mac=00:01:02:03:04:05",
                },
                "opts": {
                    "host": "172.16.44.4",
                    "host_proto": "qemu+tcp",
                    "virttype": "kvm",
                    "disksize": "40",
                },
          }

#deploy_vm(vm_desc)
#power_on_vm(vm_desc)
#delete_vm(vm_desc)

upload_image(iso,node,storage_path)