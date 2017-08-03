'''
Openstack Capacity Utilization
sbabbar - 05152017
'''

import subprocess
import os
import sys
import decimal
from keystoneauth1.identity import v3
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v3 import client
from novaclient import client as nclient

def exp_auth():
   with open('/openrc') as fh:
      for line in fh:
         if line.__contains__("export"):
            VAR = line.split('export')[1].strip()
            key = VAR.split('=')[0]
            value = VAR.split('=')[1].replace("'", '').strip() 
            os.environ[key] = value.strip('')

exp_auth()

auth = v3.Password(auth_url=os.environ["OS_AUTH_URL"], username=os.environ["OS_USERNAME"],
                      password=os.environ["OS_PASSWORD"], project_name=os.environ["OS_PROJECT_NAME"],
                      user_domain_id=os.environ["OS_USER_DOMAIN_ID"], project_domain_id=os.environ["OS_PROJECT_DOMAIN_ID"])

sess = session.Session(auth=auth)
keystone = client.Client(session=sess)
nova = nclient.Client(2.0, session=sess)
print "\n","Tenant,TotalCoresAllocated,TotalCoresUsed,TotalMemoryAllocated(GB),TotalMemoryUsed(GB),TotalInstancesAllocated,TotalInstancesUsed"
print '=' * 130
def get_tenant():
   GTotalInstancesAllocated = 0
   tenants=keystone.projects.list()
   for line in tenants:
      tenant=line.name
      tenantID=line.id
      mydi = dict()
      limits = subprocess.check_output(['nova', 'absolute-limits', '--tenant', tenantID])
      lines = limits.splitlines()
      for item in lines:
         for word in item.split():
            mydi.setdefault(word, list()).append(item)

      Cores_Used=mydi['Cores'][0].split('|')[2].strip(' ')
      Cores_Max=mydi['Cores'][0].split('|')[3].strip(' ')
      Instances_Used=mydi['Instances'][0].split('|')[2].strip(' ')
      Instances_Max=mydi['Instances'][0].split('|')[3].strip(' ')
      RAM_Used_GB=int(mydi['RAM'][0].split('|')[2].strip(' ')) / 1024
      RAM_Max_GB=int(mydi['RAM'][0].split('|')[3].strip(' ')) / 1024
      GTotalInstancesAllocated += int(Instances_Max)
      print(','.join([tenant,Cores_Max, Cores_Used, str(RAM_Max_GB), str(RAM_Used_GB), Instances_Max, Instances_Used]))
   return (GTotalInstancesAllocated)
  

GTotalInstancesAllocated = get_tenant()

myd = dict()
stats = subprocess.check_output("openstack hypervisor stats show", shell=True)
lines = stats.splitlines()
for item in lines:
    for word in item.split():
        myd.setdefault(word, list()).append(item)

hypervisor_count=myd['count'][0].split('|')[2].strip(' ')
vcpus=myd['vcpus'][0].split('|')[2].strip(' ')
vcpus_used=myd['vcpus_used'][0].split('|')[2].strip(' ')
memory_gb=int(myd['memory_mb'][0].split('|')[2].strip(' ')) / 1024
memory_gb_used=int(myd['memory_mb_used'][0].split('|')[2].strip(' ')) / 1024
running_vms=myd['running_vms'][0].split('|')[2].strip(' ')
PercentCPUutilized = round(decimal.Decimal(int(vcpus_used))/int(vcpus)*100,1)
PercentRAMutilized = round(decimal.Decimal(int(memory_gb_used))/int(memory_gb)*100,1)
print "\n","Total_Hypervisors,Total_vCPUs,Total_vCPUs_Used,PercentCPUutilized,Total_Memory(GB),Total_Memory_Used(GB),PercentRAMutilized,TotalInstancesAllocated,Total_Running_VMs"
print '=' * 165
print(','.join([hypervisor_count, vcpus, vcpus_used, str(PercentCPUutilized), str(memory_gb), str(memory_gb_used), str(PercentRAMutilized), str(GTotalInstancesAllocated), running_vms])),"\n"
