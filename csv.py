class CSVImporter:

    def __init__(self, mapping, separator="\t"):
        self.separator = separator
        self.mapping = mapping

    def open(self, filename):
        self.file_handler = file(filename, "r")
        headers_line = self.file_handler.readline().rstrip()
        self._headers = headers_line.split(self.separator)

    def save_all(self):
        while self.save_row(self.readline()):
            pass

    def readline(self):
        line = self.file_handler.readline().rstrip()
        if not line:
            return None

        data_fields = line.split(self.separator)

        results = self.mapping.new_resultset()

        for i in range(len(data_fields)):
            field_value = data_fields[i]
            header = self._headers[i]

            instance_name, field_name = tuple(header.split("."))
            setattr(results[instance_name], field_name, field_value)

        for instance, attributes in self.mapping.relations.items():
            for attribute, target in attributes.items():
                setattr(results[instance], attribute, results[target])

        return results

    def save_row(self, results):
        for name, obj in results.items():
            self.save_obj(results, name)

    def save_obj(self, results, name):
        obj = results[name]

        if not obj.pk:
            for attribute, target in self.mapping.relations.get(name, {}).items():
                target_obj = self.save_obj(results, target)
                setattr(obj, attribute, target_obj)

            obj.save()

        return obj
class InstanceMapping:

    def __init__(self, obj_class):
        self.obj_class = obj_class

    def new(self):
        return self.obj_class()

class CSVImporterMapping:

    def __init__(self):
        self.map_dict = {}
        self.relations = {}
        self.inverse_relations = {}

    def map_class(self, instance_name, class_obj):
        self.map_dict[instance_name] = InstanceMapping(class_obj)

    def map_relation(self, base, attribute, target):
        self.relations.setdefault(base, {})[attribute] = target
        self.inverse_relations.setdefault(target, {})[attribute] = base

    def new_resultset(self):
        out = {}
        for instance_name, instance_mapping in self.map_dict.items():
            out[instance_name] = instance_mapping.new()
        return out
