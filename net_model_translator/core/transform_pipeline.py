class TransformationPipeline:
    def __init__(self, *transforms):
        self.transforms = transforms

    def apply(self, value):
        for transform in self.transforms:
            value = transform(value)
        return value
