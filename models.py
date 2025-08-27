from pydantic import BaseModel

# Features
class Features(BaseModel):
    layer: str
    feature_list: list[str]

class FeatureAreaItem(BaseModel):
    feature_class : str
    total_area : float

class FeatureArea(BaseModel):
    layer : str
    feature : str
    feature_list: list[FeatureAreaItem]

class FeaturePerimeterItem(BaseModel):
    feature_class : str
    perimeter : float

class FeaturePerimeter(BaseModel):
    layer : str
    feature : str
    total_perimeter :  list[FeaturePerimeterItem]


class Centroid(BaseModel):
    x: float
    y : float
class FeatureCentroidItem(BaseModel):
    feature_class : str
    centroid: Centroid

class FeatureCentroids(BaseModel):
    layer : str
    feature: str
    centroids: list[FeatureCentroidItem]

class FeatureAreaShort(BaseModel):
    layer : str
    feature : str
    feature_class : str
    total_area : float

