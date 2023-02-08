from typing import Callable, Mapping
from marshmallow import Schema, fields, pre_load, post_load, post_dump


class DefaultSchema(Schema):
    __default_field__: str

    @pre_load
    def _convert_default(self, value, **_):
        if isinstance(value, Mapping):
            return value
        return {self.__default_field__: value}


class ThresholdSegmentation(DefaultSchema):
    __default_field__ = "threshold"
    threshold = fields.Number()


class StoredSegmentation(DefaultSchema):
    __default_field__ = "pickle_fn"
    pickle_fn = fields.Str()
    full_frame_archive_fn = fields.Str(load_default=None)
    skip_single = fields.Bool(load_default=False)


class PytorchSegmentation(DefaultSchema):
    __default_field__ = "model_fn"
    model_fn = fields.Str(required=False)
    jit_model_fn = fields.Str(required=False)
    full_frame_archive_fn = fields.Str(load_default=None)
    skip_single = fields.Bool(load_default=False)
    device = fields.Str(load_default="cpu")
    closing_radius = fields.Int(load_default=0)


class SegmentationSchema(Schema):
    threshold = fields.Nested(ThresholdSegmentation, required=False)
    stored = fields.Nested(StoredSegmentation, required=False)
    pytorch = fields.Nested(PytorchSegmentation, required=False)


class LokiInputSchema(Schema):
    path = fields.Str()
    segmentation = fields.Nested(SegmentationSchema)
    slice = fields.Int(required=False)
    meta = fields.Dict(required=False)


class InputSchema(Schema):
    loki = fields.Nested(LokiInputSchema)


class EcoTaxaOutputSchema(Schema):
    path = fields.Str()
    image_fn = fields.Str(required=False)


class OutputSchema(Schema):
    ecotaxa = fields.Nested(EcoTaxaOutputSchema)


class PipelineSchema(Schema):
    input = fields.Nested(LokiInputSchema, required=True)
    output = fields.Nested(EcoTaxaOutputSchema, required=True)


if __name__ == "__main__":
    import sys
    import yaml

    with open(sys.argv[1]) as f:
        config = PipelineConfig()
        x = config.load(yaml.safe_load(f))

        print(x)
