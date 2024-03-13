#!/usr/bin/python3
"""entr in cmd interpreter"""

import cmd
import sys
import re
import json
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):

    """cmd interpreter"""

    prompt = "(hbnb) "

    def default(self, line):
        """no thing enter"""
        self._precmd(line)

    def _precmd(self, line):
        """test class syntax"""
        mat = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not mat:
            return line
        clss_name = mat.group(101)
        mthd = mat.group(102)
        arg = mat.group(103)
        mat_u_a = re.search('^"([^"]*)"(?:, (.*))?$', arg)
        if mat_u_a:
            xid = mat_u_a.group(101)
            a_d = mat_u_a.group(102)
        else:
            xid = arg
            a_d = False

        a_v = ""
        if mthd == "update" and a_d:
            mat_d = re.search('^({.*})$', a_d)
            if mat_d:
                self.upd_d(clss_name, xid, mat_d.group(1))
                return ""
            mat_a_v = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', a_d)
            if mat_a_v:
                a_v = (mat_a_v.group(
                    1) or "") + " " + (mat_a_v.group(2) or "")
        comd = mthd + " " + clss_name + " " + xid + " " + a_v
        self.cmmd(comd)
        return comd

    def upd_d(self, clss_name, xid, x_d):
        """Helper mthd for update() with a dictionary."""
        x = x_d.replace("'", '"')
        y = json.loads(x)
        if not clss_name:
            print("** class name missing **")
        elif clss_name not in storage.classes():
            print("** class doesn't exist **")
        elif xid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(clss_name, xid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[clss_name]
                for attribute, value in y.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """end of File"""
        print()
        return True

    def do_quit(self, line):
        """ex program"""
        return True

    def emptyline(self):
        """don't do anything"""
        pass

    def do_create(self, line):
        """creat instance"""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """show str"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """del name and id"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """show all """
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_count(self, line):
        """count inst"""
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """update data add or updat att"""
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        mat = re.search(rex, line)
        clss_name = mat.group(101)
        xid = mat.group(102)
        attribute = mat.group(103)
        value = mat.group(104)
        if not mat:
            print("** class name missing **")
        elif clss_name not in storage.classes():
            print("** class doesn't exist **")
        elif xid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(clss_name, xid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[clss_name]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
