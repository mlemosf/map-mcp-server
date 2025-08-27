from fastapi import FastAPI
import geopandas as gpd

DEFAULT_EPSG=31983 # SIRGAS 2000
JSON_PATH = "~/Downloads/upt.json"
#JSON_PATH = "~/Downloads/classes_de_solos.json"

app = FastAPI()

@app.get("/{layer}/features")
def get_layer_features(layer: str):
    """
    Retrieve feature list for a specific layer.

    Args:
        layer (str): Name of the layer to retrieve features for.

    Returns:
        dict: A dictionary containing the layer name and list of features.
    """
    gdf = gpd.read_file(JSON_PATH)
    features = list(gdf.columns)
    return {
        'layer': layer,
        'feature_list': features
    }
    

@app.get("/{layer}/area/{feature}")
def get_features_area(layer: str, feature: str):
    """
    Calculate total area by feature class for a specific layer.

    Args:
        layer (str): Name of the layer.
        feature (str): Name of the feature to calculate area for.

    Returns:
        dict: A dictionary containing layer info, feature, and total area by class.
    """
    gdf = gpd.read_file(JSON_PATH)
    gdf = gdf.to_crs(epsg=DEFAULT_EPSG)

    try:
        feature_area = gdf.groupby(feature).area.sum()
        feature_list = [{'feature_class': i, 'total_area': j} for i,j in feature_area.items()]
    except Exception:
        new_gdf = gpd.GeoDataFrame(gdf[[feature, 'geometry']])
        new_gdf['area'] = gdf.geometry.area
        feature_list = [{'feature_class': row[feature], 'total_area': row['area']} for idx, row in new_gdf.iterrows()]
    
    return {
        'layer': layer,
        'feature': feature,
        'total_area': feature_list
    }

@app.get("/{layer}/perimeter/{feature}")
def get_feature_perimeter(layer: str, feature: str):
    """
    Calculate total perimeter by feature class for a specific layer.

    Args:
        layer (str): Name of the layer.
        feature (str): Name of the feature to calculate perimeter for.

    Returns:
        dict: A dictionary containing layer info, feature, and total perimeter by class.
    """
    gdf = gpd.read_file(JSON_PATH)
    gdf = gdf.to_crs(epsg=DEFAULT_EPSG)

    try:
        feature_perimeter = gdf.groupby(feature).length.sum()
        feature_list = [{'feature_class': i, 'total_area': j} for i,j in feature_perimeter.items()]
    except Exception:
        new_gdf = gpd.GeoDataFrame(gdf[[feature, 'geometry']])
        new_gdf['perimeter'] = gdf.geometry.length
        feature_list = [{'feature_class': row[feature], 'total_area': row['perimeter']} for idx, row in new_gdf.iterrows()]
    
    return {
        'layer': layer,
        'feature': feature,
        'total_perimeter': feature_list
    }

@app.get("/{layer}/centroid/{feature}")
def get_feature_centroid(layer: str, feature: str):
    """
    Calculate centroids for features in a specific layer.

    Args:
        layer (str): Name of the layer.
        feature (str): Name of the feature to calculate centroids for.

    Returns:
        dict: A dictionary containing layer info, feature, and centroids for each class.
    """
    gdf = gpd.read_file(JSON_PATH)
    gdf = gdf.to_crs(epsg=DEFAULT_EPSG)

    try:
        feature_perimeter = gdf.groupby(feature).centroid.to_crs(epsg=4326)
        feature_list = [{'feature_class': i, 'total_area': j} for i,j in feature_perimeter.items()]
    except Exception:
        new_gdf = gpd.GeoDataFrame(gdf[[feature, 'geometry']])
        new_gdf['centroid'] = gdf.geometry.centroid.to_crs(epsg=4326)
        feature_list = [{
            'feature_class': row[feature],
            'centroid':{
                'x': row['centroid'].x,
                'y': row['centroid'].y,
            }
        } for idx, row in new_gdf.iterrows()]
    
    return {
        'layer': layer,
        'feature': feature,
        'centroids': feature_list
    }



@app.get("/{layer}/area/{feature}/{feature_class}")
def get_feature_area(layer, feature, feature_class):
    """
    Calculate total area for a specific feature class in a layer.

    Parameters:
    layer (str): Name of the layer.
    feature (str): Name of the feature.
    feature_class (str): Class of the feature.

    Returns:
    dict: A dictionary containing layer info, feature, feature class, and total area.
    """
    gdf = gpd.read_file(JSON_PATH)
    feature_data = gdf[gdf[feature] == feature_class]

    feature_area = feature_data.area.sum()
    print(feature_data)
    return {
        'layer': layer,
        'feature': feature,
        'feature_class': feature,
        'total_area': feature_area
    }
