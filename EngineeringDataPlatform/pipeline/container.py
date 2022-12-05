
from python_on_whales import docker
import EngineeringDataPlatform as edp




class WorkspaceContainerManager:

    def __init__(self, workspace):
        self.workspace = workspace

        self.running_containers = {}
        self._get_running_containers()



    def get_or_start(self, config):
        """
        Get or start the specified container.
        Note that the container can take multiple minutes to actually become available, and the reference object is returned after executing the "docker run -d ...".
        :param config:
        :return:
        """
        image_name = config.get('image')
        base_container_name = config.get('name')

        if base_container_name in self.running_containers:
            return self.running_containers[base_container_name]

        else:
            ports = config.get('ports') # eg list of inside and outside ports = [(27017, 27017)]

            port_offset = self.workspace.get_workspace_port_offset_for_local_containers()
            workspace_ports = [(internal+port_offset, internal) for internal in ports]

            container_name = base_container_name + '_edp_' + self.workspace.name()

            mongo = docker.run(image_name, publish=workspace_ports, detach=True, name=container_name)
            self.running_containers[base_container_name] = mongo
            return mongo


    def _get_running_containers(self):
        self.running_containers.clear() # reset this

        all_containers = docker.ps()
        for container in all_containers:
            info = self._parse_container_name(container.name)
            if info is None:
                continue # not ours

            self.running_containers[info[0]] = container


    def _parse_container_name(self, container_name):
        # we're separating by underscores in the name for now...
        # eg $name$_edp_$workspaceName$

        if '_edp_' not in container_name:
            return None
        else:
            return container_name.split('_edp_')






