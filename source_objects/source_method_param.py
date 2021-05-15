from source_objects.source_object import SourceObject


class SourceMethodParam(SourceObject):
    def __init__(self, param):
        super().__init__(param.name)
        self.type = self.resolve_param_type(param)

    @staticmethod
    def resolve_param_type(param):
        if param.type:
            resolved_type = param.type.name + "[]" * len(param.type.dimensions)
        elif param.pattern_type:
            resolved_type = param.pattern_type
        else:
            resolved_type = "UNKNOWN"

        if hasattr(param.type, "arguments") and param.type.arguments is not None:
            resolved_type += "<" + ", ".join(
                [SourceMethodParam.resolve_param_type(x) for x in param.type.arguments]) + ">"

        return resolved_type
