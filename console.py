#!/usr/bin/env python3

""" AirBnB Console """

import cmd
import sys
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import argparse


class HBNBCommand(cmd.Cmd):
    """ Class HBNB to read command """
    prompt = '(hbnb) '
    __all_117 = 0

    def emptyline(self):
        """Pass if no command is given"""
        pass

    def precmd(self, line):
        """ Edit given command to allow second type of input"""
        if not sys.stdin.isatty():
            print()
        if '.' in line:
            HBNBCommand.__all_117 = 1
            line = line.replace('.', ' ').replace('(', ' ').replace(')', ' ')
            cmd_argv = line.split()
            cmd_argv[0], cmd_argv[1] = cmd_argv[1], cmd_argv[0]
            line = " ".join(cmd_argv)
        return super().precmd(line)

    def do_quit(self, arg):
        'Quit command to exit the program'
        return True

    def do_EOF(self, arg):
        'EOF command to exit the program'
        print()
        return True

    def do_create(self, arg):
        "Create an instance if the Model exists"
        if not arg:
            print("** class name missing **")
            return None
        try:
            my_model = eval(arg + "()")
            my_model.save()
            print(my_model.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        "Print dict of an instance in base of its ID"
        cmd_argv = arg.split()
        if not cmd_argv:
            print("** class name missing **")
            return None
        try:
            eval(cmd_argv[0])
        except NameError:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all()
        if len(cmd_argv) < 2:
            print("** instance id missing **")
            return None

        cmd_argv[1] = cmd_argv[1].replace("\"", "")
        key = cmd_argv[0] + '.' + cmd_argv[1]

        if all_objs.get(key, False):
            print(all_objs[key])
        else:
            print("** no instance found **")

    def do_all(self, arg):
        "Print all the instances saved in file.json"
        cmd_argv = arg.split()

        if cmd_argv:
            try:
                eval(cmd_argv[0])
            except NameError:
                print("** class doesn't exist **")
                return None

        all_objs = storage.all()
        print_list = []
        len_objs = len(all_objs)
        for key, value in all_objs.items():
            if not cmd_argv:
                if HBNBCommand.__all_117 == 0:
                    print_list.append("\"" + str(value) + "\"")
                else:
                    print_list.append(str(value))
            else:
                check = key.split('.')
                if cmd_argv[0] == check[0]:
                    if HBNBCommand.__all_117 == 0:
                        print_list.append("\"" + str(value) + "\"")
                    else:
                        print_list.append(str(value))
        print("[", end="")
        print(", ".join(print_list), end="")
        print("]")

    def do_destroy(self, arg):
        "Deletes an instance based on it's ID and save the changes\n \
        Usage: destroy <class name> <id>"

        cmd_argv = arg.split()
        if not cmd_argv:
            print("** class name missing **")
            return None
        try:
            eval(cmd_argv[0])
        except Exception:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all()

        if len(cmd_argv) < 2:
            print("** instance id missing **")
            return None

        cmd_argv[1] = cmd_argv[1].replace("\"", "")
        key = cmd_argv[0] + '.' + cmd_argv[1]

        if all_objs.get(key, False):
            all_objs.pop(key)
            storage.save()
        else:
            print("** no instance found **")

    def do_update(self, arg):
        "Usage: update <class name> <id> <attribute name> <attribute value>"
        parser = argparse.ArgumentParser()
        parser.add_argument('class_name', help='class name')
        parser.add_argument('id', help='instance id')
        parser.add_argument('attribute_name', help='attribute name')
        parser.add_argument('attribute_value', help='attribute value')
        args = parser.parse_args(arg.split())

        class_name = args.class_name
        id = args.id
        attribute_name = args.attribute_name
        attribute_value = args.attribute_value

        if not class_name:
            print("** class name missing **")
            return None

        try:
            cls = eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return None

        all_objs = storage.all(cls)

        key = "{}.{}".format(class_name, id)
        if key not in all_objs:
            print("** no instance found **")
            return None

        obj = all_objs[key]
        setattr(obj, attribute_name, attribute_value)
        obj.save()

    def do_count(self, arg):
        "Usage: count <class name> or <class name>.count()"
        parser = argparse.ArgumentParser()
        parser.add_argument('class_name', help='class name', nargs='?')
        args = parser.parse_args(arg.split())

        class_name = args.class_name

        if not class_name:
            count = len(storage.all())
        else:
            try:
                cls = eval(class_name)
            except NameError:
                print("** class doesn't exist **")
                return None

            count = len(storage.all(cls))

        print(count)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
