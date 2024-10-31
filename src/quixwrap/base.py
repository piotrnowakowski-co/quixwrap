import os


class Secret(str):
    def __new__(cls, val):
        obj = super().__new__(cls, val)
        return obj

    def __str__(self):
        return "*****"

    def __repr__(self):
        return "Secret: *****"

    # Descriptor protocol support for managed access to the value
    def __get__(self, obj, objtype=None):
        return self


typemap = {"FreeText": str, "InputTopic": str, "OutputTopic": str, "Secret": Secret}


def as_bool(val: str):
    try:
        if val.casefold() in ["true", "1", "yes", "y"]:
            return True
        if val.casefold() in ["false", "0", "no", "n"]:
            return False
    except AttributeError:
        pass
    if val in [True, False]:
        return val
    raise ValueError(f"Unable to cast {val} as boolean.")


class Variable:
    """Descriptor for accessing quix env vars."""

    def __init__(self, name, default=None, required=False, qtype="FreeText"):
        self.name = name
        self.default = default
        self.required = required
        self._qtype = qtype
        self.type = typemap.get(qtype)

    def __get__(self, obj, objtype=None):
        val = os.getenv(self.name, self.default)
        if not val and self.required:
            raise LookupError(f"Variable {self.name} is not set.")

        try:
            return as_bool(val)
        except ValueError:
            pass

        try:
            if val.casefold() in ["none", "null"]:
                return
        except AttributeError:
            if val is None:
                return
        return self.type(val)


class EnvMixin:

    @classmethod
    def _is(cls, env: str):
        if isinstance(cls.env, str):
            return env.casefold() in cls.env.casefold()
        return False

    @classmethod
    def is_test(cls):
        return cls._is("test")

    @classmethod
    def is_local(cls):
        # testing env is considered local
        return cls._is("local") or cls.is_test()


class Config(EnvMixin):
    broker_address = Variable("BROKER_ADDRESS")
    quix__sdk__token = Variable("Quix__Sdk__Token", qtype="Secret")

    env = Variable("ENV")


class DeploymentWrapper:
    config: Config

    @classmethod
    def app_config(
        cls, auto_create_topics=True, auto_offset_reset="earliest", **opts
    ) -> dict:
        """Returns a configuration mapping suitable for `quixstreams.Application` object.

        Depending on the ENV variable, the returned mapping will contain either the `quix_sdk_token` (in the
        case of non local deployments), or a `broker_address` otherwise.

        """
        conf = {
            "auto_create_topics": auto_create_topics,
            "auto_offset_reset": auto_offset_reset,
        }
        if cls.config.is_local():
            conf.update({"broker_address": cls.config.broker_address})
        else:
            conf.update({"quix_sdk_token": cls.config.quix__sdk__token})
        conf.update(**opts)
        return conf
