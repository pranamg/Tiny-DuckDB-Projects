# Chapter 14: Treasure Hunt

Find treasure locations using DuckDB's spatial extension.

## Learning Goals

- Install and use DuckDB extensions
- Work with spatial/geometry data
- Calculate distances between points
- Find locations within a radius

## The Challenge

Build a treasure hunt helper that:
1. Stores treasure locations as spatial points
2. Finds treasures within a given radius of the player
3. Calculates the distance to each treasure
4. Orders treasures by proximity

## Concepts Introduced

- `INSTALL spatial; LOAD spatial;`
- `ST_Point()` to create points
- `ST_Distance()` for distance calculation
- `ST_DWithin()` for radius queries
- `ST_AsText()` and `ST_GeomFromText()`
- Spatial indexing concepts
