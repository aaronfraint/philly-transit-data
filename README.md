# philly-transit-data
Download GIS data published by SEPTA &amp; NJ Transit

## Installation

This package depends upon `geopandas` and `pandas`. After installing these two libraries
you can install this module using the following command:

```bash
pip install git+https://github.com/aaronfraint/philly-transit-data.git
```

## Usage

### Import the module and instantiate the `TransitData` object:

```bash
>>> from philly_transit_data import TransitData
>>> data = TransitData()
```

### Download a single transit mode:
```bash
>>> stops, lines = data.get_data_from_portal(mode="SEPTA bus")
```

### Or, download all transit modes at once:
```bash
>>> stops, lines = data.all_spatial_data()
```

### You can now use `stops` and `lines` like any `GeoDataFrame`
For example, save to shapefile with `.to_file()`

```bash
>>> print(type(stops))
<class 'geopandas.geodataframe.GeoDataFrame'>

>>> stops.to_file("philly_transit_stops.shp")
```

### See a list of all available modes

```bash
>>> data.options()
['SEPTA regional rail', 'SEPTA trolley', 'SEPTA bus', 'SEPTA subway - broad', 'SEPTA subway - market', 'SEPTA norristown high speed line', 'NJT bus', 'NJT rail']
```

### Add a data source

For example, add AMTRAK's national stop and route datasets
```bash
>>> new_mode = "AMTRAK national network"
>>> data.add_data_source(new_mode, "stops", "https://opendata.arcgis.com/datasets/628537f4cf774cde8aa9721212226390_0.geojson")
>>> data.add_data_source(new_mode, "lines", "https://opendata.arcgis.com/datasets/d04fab6590c04feaa5f3955ef5abe929_0.geojson")
```
