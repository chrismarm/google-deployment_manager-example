"""Creates a GCE Compute Instance"""


COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
  base_name = context.env['deployment'] + '-' + context.env['name']
  project = context.env['project']
  zone = context.properties['zone']
  machine = context.properties['machineType']
  image = context.properties['image']

  instance = {
      'zone': zone,
      'machineType': GetUrlZones(project, zone, 'machineTypes', machine),
      'disks': [{
          'deviceName': 'boot',
          'type': 'PERSISTENT',
          'autoDelete': True,
          'boot': True,
          'mode': 'READ_WRITE',
          'initializeParams': {
              'diskName': base_name + '-disk',
              'sourceImage': GetUrlGlobal('debian-cloud', 'images', image)
              },
          }],
      'networkInterfaces': [{
          'accessConfigs': [{
              'name': 'NAT',
              'type': 'ONE_TO_ONE_NAT'
              }],
          'network': GetUrlGlobal(
              project, 'networks', 'default')
          }]
      }

  config = {
      'resources': [{
            'name': base_name,
            'type': 'compute.v1.instance',
            'properties': instance
          },
          {
            'name': 'http-access',
            'type': 'compute.v1.firewall',
            'properties': {
              'sourceRanges': ["0.0.0.0/0"],
              'allowed': [{
                'IPProtocol': 'TCP',
                'ports': ["80"]    
              }]
            }
          }],
      'outputs': [{
        'name': 'instance_ip',
        'value': '$(ref.' + base_name + '.networkInterfaces[0].accessConfigs[0].natIP)'
      }]
    }

  return config

def GetUrlGlobal(project, elementType, name):
  return ''.join([COMPUTE_URL_BASE, 'projects/', project,
                  '/global/', elementType, '/', name])


def GetUrlZones(project, zone, elementType, name):
  return ''.join([COMPUTE_URL_BASE, 'projects/', project,
                  '/zones/', zone, '/', elementType, '/', name])
