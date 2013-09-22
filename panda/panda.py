#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import pisi
import shutil
from subprocess import call

sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

grub_file = "/boot/grub2/grub.cfg"
grub_new = "/boot/grub2/grub.cfg.new"
grub_back = "/boot/grub2/grub.cfg.back"
grub_default_file = "/etc/default/grub"
grub_default_file_new = "/etc/default/grub.new"
grub_default_file_back = "/etc/default/grub.back"
kernel_file = "/etc/kernel/kernel"
kernel_file_pae = "/etc/kernel/kernel-pae"
nvidia_blacklist_file = "/etc/modprobe.d/nvidia-blacklist.conf"

class Panda():
    '''Pardus Alternative Driver Administration'''
    def __init__ (self, default_args=None):
        self.driver_name = None
        self.kernel_flavors = None
        self.os_driver = None
        self.driver_packages = {"fglrx": ["module-fglrx",
                                     "module-pae-fglrx",
                                     "module-fglrx-userspace",
                                     "xorg-video-fglrx"],
                           "nvidia-current": ["module-nvidia-current",
                                              "module-pae-nvidia-current",
                                              "module-nvidia-current-userspace",
                                              "xorg-video-nvidia-current",
                                              "nvidia-xconfig",
                                              "nvidia-settings"] ,
                           "nvidia96": ["module-nvidia96",
                                        "module-pae-nvidia96",
                                        "module-nvidia96-userspace",
                                        "xorg-video-nvidia96",
                                        "nvidia-xconfig",
                                        "nvidia-settings"],
                           "nvidia173": ["module-nvidia173",
                                         "module-pae-nvidia173",
                                         "module-nvidia173-userspace",
                                         "xorg-video-nvidia173",
                                         "nvidia-xconfig",
                                         "nvidia-settings"],
                           "nvidia304": ["module-nvidia304",
                                         "module-nvidia304-userspace",
                                         "xorg-video-nvidia304",
                                         "nvidia-xconfig",
                                         "nvidia-settings"]}

    def __get_primary_driver(self):
        '''Get driver name for the working primary device'''

        self.driver_name = "Not defined"

        for boot_vga in glob.glob("%s/*/boot_vga" % sysdir):
            if open(boot_vga).read().startswith("1"):
                dev_path = os.path.dirname(boot_vga)
                vendor = open(os.path.join(dev_path, "vendor")).read().strip()
                device = open(os.path.join(dev_path, "device")).read().strip()
                device_id = vendor[2:] + device[2:]

                try:
                    db_file = open(driversDB)
                except IOError:
                    break

                # We've found a Nvidia card, thus set it to nvidia-current
                # That's a workaround for new Nvidia cards that are not written in driversDB
                if vendor[2:] == "10de":
                    self.driver_name = "nvidia-current"

                for line in db_file:
                    if line.startswith(device_id):
                        self.driver_name = line.split()[1]
                        break

                # We've set a card, no need to search for another one
                break 

        return self.driver_name

    def __get_kernel_module_packages(self, kernel_list=None):
        '''Get the appropirate module for the specified kernel'''
        if not kernel_list:
            if self.kernel_flavors is None:
                self.__get_kernel_flavors()
            kernel_list = self.kernel_flavors.keys()

        if self.driver_name is None:
            self.__get_primary_driver()

        module_packages = []
        for kernel_name in kernel_list:
            tmp, sep, suffix = kernel_name.partition("-")
            if suffix:
                module_packages.append("module-%s-%s" % (suffix, self.driver_name))
            else:
                module_packages.append("module-%s" % self.driver_name)

        return module_packages

    def __get_kernel_flavors(self):
        ''' Get kernel version '''
        kernel_dict = {}

        for kernel_file in glob.glob("/etc/kernel/*"):
            if not os.path.isfile(kernel_file): continue
            kernel_name = os.path.basename(kernel_file)
            kernel_dict[kernel_name] = open(kernel_file).read()

        self.kernel_flavors = kernel_dict

    def get_blacklisted_module(self):
        if self.driver_name is None:
            self.__get_primary_driver()

        if self.driver_name == "fglrx":
            self.os_driver = "radeon"
            return self.os_driver
        elif self.driver_name in ["nvidia-current", "nvidia96", "nvidia173", "nvidia304"]:
            self.os_driver = "nouveau"
            return self.os_driver
        else:
            return


    def get_needed_driver_packages(self, kernel_flavors=None, installable=False):
        '''Filter modules that should be addded'''
        needed_module_packages = self.__get_kernel_module_packages(kernel_flavors)

        if not self.driver_name == "Not defined":
            # List only kernel_flavors, we assume that a kernel flavor begins with
            # "module-" and does not end with "-userspace"
            module_packages = filter(lambda x: x.startswith("module-") and not x.endswith("-userspace"), \
                                    self.driver_packages[self.driver_name])

            # Kernel_list contains currently used kernel modules
            # Kernel_flavors contains predefined kernel modules
            # driver_package[driver_name] contains all modules 
            # All modules should be stay nontouched, but remove kernels in kernel_flavors
            # that are not in kernel_list (hence we are not using them)

            need_to_install = list(set(self.driver_packages[self.driver_name]) - \
                                   (set(module_packages) - set(needed_module_packages)))

            if installable:
                import pisi
                idb = pisi.db.installdb.InstallDB()
                need_to_install = [x for x in need_to_install if not idb.has_package(x)]

            return need_to_install
        else:
            return []

    def get_all_driver_packages(self):
        '''Extract lists from the driver dict and return one unique single list'''
        drivers = sum([x for x in self.driver_packages.values()], [])

        return list(set(drivers))

    def update_system_files(self, arg):
        '''Update system files to enable the use of propretiary graphic card drivers'''
        if self.os_driver is None:
            self.get_blacklisted_module()

        status, modified = self.update_grub_default_entries(arg)
        if status in ["os", "generic", "vendor"] and modified:
            self.update_grub_cfg()
            self.set_libGL(self.driver_name if self.driver_name in ["nvidia-current", "nvidia96", "nvidia173", "nvidia304", "fglrx"] and status == "vendor" else "mesa")
            if self.driver_name in ["nvidia-current", "nvidia96", "nvidia173", "nvidia304"] and status == "vendor":
                open(nvidia_blacklist_file, "w").write("blacklist nouveau\n")
            elif self.driver_name in ["nvidia-current", "nvidia96", "nvidia173", "nvidia304"] and os.path.isfile(nvidia_blacklist_file):
                os.remove(nvidia_blacklist_file)
                

        return status

    def set_libGL(self, arg):
        '''alternatives --set libGL /usr/lib/arg/libGL.so.1.2.0'''
        try:
            retcode = call("alternatives --set libGL /usr/lib/%s/libGL.so.1.2.0" % arg, shell=True)
        except OSError as e:
            print >>sys.stderr, "alternatives --set libGL /usr/lib/%s/libGL.so.1.2.0 failed:" % arg, e
        if not arg in ["mesa", "nvidia-current", "fglrx"]: return
        try:
            retcode = call("alternatives --set libGL-32bit /usr/lib32/%s/libGL.so.1.2.0" % arg, shell=True)
        except OSError as e:
            print >>sys.stderr, "alternatives --set libGL-32bit /usr/lib32/%s/libGL.so.1.2.0 failed:" % arg, e

    ########################################
    # Functions essential for grub parsing #

    def parameter_value_in_line(self, line, keyword):
        params = line.split()
        blacklist = []

        for param in params:
            if param.startswith("%s=" % keyword):
                modules = param.split("=", 1)[1].split(",")
                blacklist.extend(modules)

        return blacklist

    def update_parameter_in_line(self, line, parameter_name, parameter_value):
        params = [x for x in line.strip().split() if not x.startswith("%s" % parameter_name)]

        if parameter_value is True:
            params.append(parameter_name)
        elif parameter_value:
            params.append("%s=%s" % (parameter_name, ",".join(parameter_value)))

        return " ".join(params) + "\n"

    ###################
    # State functions #

    def get_driver_types(self):
        if self.driver_name is None:
            self.__get_primary_driver()

        if self.driver_name in "fglrx" or self.driver_name in ["nvidia-current", "nvidia96", "nvidia173", "nvidia304"]:
            return ["vendor", "os", "generic"]
        elif "Not defined" == self.driver_name:
            return ["os", "generic"]

    def get_grub_state(self):
        '''Get the current driver state from grub file'''
        if self.os_driver is None:
            self.get_blacklisted_module()

        if self.kernel_flavors is None:
            self.__get_kernel_flavors()

        kernel_version = self.kernel_flavors["kernel"] # This one should change

        with open(grub_file) as grub:
            for line in grub:
                if "kernel" in line and kernel_version in line:
                    blacklist = self.parameter_value_in_line(line, "blacklist")
                    xorg_param = self.parameter_value_in_line(line, "xorg")

                    if self.os_driver in blacklist:
                        return "vendor"
                    elif "safe" in xorg_param:
                        return "generic"
                    else:
                        return "os"

        return "Cannot parse %s" % grub_file

    #######################################
    # Grub2 parsing and writing functions #

    def update_grub_default_entries(self, arg):
        '''Edit grub default file to enable the use of propretiary graphic card drivers'''
        if arg == "vendor" and self.os_driver is None:
            print "I'm not able to install vendor drivers"
            return
        elif arg:
            pass
        else:
            return "Wrong parameter!\" You can use: vendor or os"

        configured = False
        grub_tmp = open(grub_default_file_new, "w")

        with open(grub_default_file) as grub_default:
            for line in grub_default:
                if "GRUB_CMDLINE_LINUX_DEFAULT=" in line:
                    params = {} if line.startswith("#") else dict((k, v.split(','))
                                                                  for k,v in (item.split('=') if "=" in item else (item, '')
                                                                              for item in line.replace('"', '').replace("'", "").split("DEFAULT=")[1].split()))
                    old_line = " ".join(["%s%s%s" % (k, "=" if l[0] else "", ",".join([v for v in l])) for k, l in sorted(params.items())])
                    if arg == "os":
                        try :
                            params["blacklist"] = [x for x in params["blacklist"] if x != self.os_driver]
                            if len(params["blacklist"]) == 0: del params["blacklist"]
                        except KeyError:
                            pass
                        try :
                            params["xorg"] = [x for x in params["xorg"] if x !=  "safe"]
                            if not params["xorg"] or not params["xorg"][0]: del params["xorg"] 
                        except KeyError:
                            pass
                        status = "os"

                    elif arg == "vendor":
                        try:
                            if not self.os_driver in params["blacklist"]:
                                params["blacklist"].append(self.os_driver)
                        except KeyError:
                            params["blacklist"] = [self.os_driver]
                        try :
                            params["xorg"] = [x for x in params["xorg"] if x !=  "safe"]
                            if not params["xorg"] or not params["xorg"][0]: del params["xorg"]
                        except KeyError:
                            pass
                        status = "vendor"

                    elif arg == "generic":
                        try:
                            params["xorg"].append("safe")
                        except KeyError:
                            params["xorg"] = ["safe"]
                        status = "generic"

                    new_line = " ".join(["%s%s" % ("%s=" % k if l[0] else k, ",".join([v for v in l])) for k, l in sorted(params.items())])
                    configured = old_line != new_line
                    new_line = 'GRUB_CMDLINE_LINUX_DEFAULT="%s"\n' % new_line
                    grub_tmp.write(new_line)
                else:
                    grub_tmp.write(line)

        grub_tmp.close()

        if configured:
            shutil.copy2(grub_default_file, grub_default_file_back)
            shutil.copy2(grub_default_file_new, grub_default_file)

        return status, configured

    def update_grub_cfg(self):
        '''Create new grub2 config file'''
        os.environ["LANG"] = read_file("/etc/mudur/locale").split("\n")[0]
        os.environ["PATH"] = "/usr/sbin:/usr/bin:/sbin:/bin"

        shutil.copy2(grub_file, grub_back)
        try:
            retcode = call("grub2-mkconfig -o %s" % grub_new, shell=True)
        except OSError as e:
            print >>sys.stderr, "Creating %s failed:" % grub_new, e
        else:
            shutil.copy2(grub_new, grub_file)

    ######################################
    # Grub parsing and writing functions #

    def update_grub_entries(self, arg):
        '''Edit grub file to enable the use of propretiary graphic card drivers'''
        if self.os_driver is None:
            self.get_blacklisted_module()

        if self.kernel_flavors is None:
            self.__get_kernel_flavors()

        kernel_version = self.kernel_flavors["kernel"] # This one should change

        if arg == "vendor" and self.os_driver is None:
            print "I'm not able to install vendor drivers"
            return
        elif arg:
            pass
        else:
            return "Wrong parameter!\" You can use: vendor or os"

        ## Grub Parsing
        configured = False

        grub_tmp = open(grub_new, "w")

        with open(grub_file) as grub:
            for line in grub:
                if "kernel" in line and kernel_version in line:
                    blacklist = self.parameter_value_in_line(line, "blacklist")
                    xorg_param = self.parameter_value_in_line(line, "xorg")

                    if arg == "os":
                        blacklist = [x for x in blacklist if x != self.os_driver]
                        if "safe" in xorg_param:
                            xorg_param.remove("safe")
                        nomodeset_param = False
                        status = "os"

                    elif arg == "vendor":
                        if self.os_driver not in blacklist:
                            blacklist.append(self.os_driver)
                        if "safe" in xorg_param:
                            xorg_param.remove("safe")
                        nomodeset_param = False
                        status = "vendor"

                    elif arg == "generic":
                        if "safe" not in xorg_param:
                            xorg_param.append("safe")
                        nomodeset_param = True
                        status = "generic"

                    new_line = self.update_parameter_in_line(line, "xorg", xorg_param)
                    new_line = self.update_parameter_in_line(new_line, "nomodeset", nomodeset_param)
                    new_line = self.update_parameter_in_line(new_line, "blacklist", blacklist)
                    # keep indentation
                    new_line = line.split("linux")[0] + new_line 
                    grub_tmp.write(new_line)
                    configured = line != new_line

                else:
                    grub_tmp.write(line)

        grub_tmp.close()

        # Replace the new grub file with the old one, create also a backup file
        if configured:
            # Backup of grub file is created: /boot/grub/grub.conf.back
            shutil.copy2(grub_file, grub_back)

            # New grub file is created: /boot/grub/grub.conf
            shutil.copy2(grub_new, grub_file)

        return status

def read_file(path):
    with open(path) as f:
        return f.read().strip()

if __name__ == '__main__':
    p = Panda()
    
    # Test cases
    print p.get_grub_state()
    print p.get_all_driver_packages()
    print p.get_blacklisted_module()
#    print p.update_grub_entries("vendor")
    print p.update_system_files("vendor")
    print p.get_needed_driver_packages(installable=False)
