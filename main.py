from fastapi import FastAPI
import geopandas as gpd

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{layer}/area/{feature}")
def get_features_area(layer, feature):
        gdf = gpd.read_file("/tmp/classes_de_solos.json")
        feature_area = gdf.groupby(feature).area.sum()
        print(feature_area)
        feature_list = [{'feature_class': i.lower(), 'total_area': j} for i,j in feature_area.items()]
        print(feature_list)
        return {
            'layer': layer,
            'feature': feature,
            'total_area': feature_list
        }

@app.get("/{layer}/area/{feature}/{feature_class}")
def get_feature_area(layer, feature, feature_class):
        gdf = gpd.read_file("/tmp/classes_de_solos.json")
        feature_data = gdf[gdf[feature] == feature_class]

        feature_area = feature_data.area.sum()
        print(feature_data)
        return {
            'layer': layer,
            'feature': feature,
            'feature_class': feature,
            'total_area': feature_area
        }
