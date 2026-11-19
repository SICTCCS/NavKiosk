# Interactive Map Tutorial

This guide explains how to create an interactive map using **OpenStreetMap**, **Leaflet.js**, HTML, CSS, and JavaScript. It walks through setting up the map, drawing polygon-based areas (such as classrooms), displaying the user's current location, and styling the map.

The examples are intended as a starting point. Replace placeholder coordinates, image paths, and colors with values from your own project.

## Table of Contents

- [Technologies and terminology](#technologies-and-terminology)
- [1. Find the map coordinates](#1-find-the-map-coordinates)
- [2. Create the project files](#2-create-the-project-files)
- [3. Load Leaflet](#3-load-leaflet)
- [4. Add the map container](#4-add-the-map-container)
- [5. Initialize the map and tile layer](#5-initialize-the-map-and-tile-layer)
- [6. Draw areas with polygons](#6-draw-areas-with-polygons)
- [7. Display the user's location](#7-display-the-users-location)
- [8. Style the map with CSS](#8-style-the-map-with-css)
- [Troubleshooting and implementation notes](#troubleshooting-and-implementation-notes)
- [Helpful resources](#helpful-resources)

## Technologies and terminology

A few of the terms used throughout this tutorial are worth understanding before starting:

| Term | Meaning |
|---|---|
| **OpenStreetMap (OSM)** | A collaborative, open map-data project. Its geographic data is used by many mapping applications. In this tutorial, an OSM-based map is used to help identify locations and provide the map tiles displayed by Leaflet. |
| **uMap** | A website built around OpenStreetMap that lets you view and create maps. Here, it is useful for finding latitude and longitude values by clicking locations on the map. |
| **Leaflet.js** | A JavaScript library for building interactive, mobile-friendly maps. It provides functions for displaying map tiles, adding markers, drawing shapes, and responding to map events. |
| **HTML** | The markup that defines the page's structure, including the element where the map will appear. |
| **CSS** | The stylesheet that controls the map's size, position, borders, and other visual properties. |
| **JavaScript** | The code that creates the Leaflet map and adds interactive features such as polygons and geolocation. |
| **Latitude and longitude** | Coordinates that describe a geographic position. Latitude measures north–south position; longitude measures east–west position. Leaflet expects them in the order `[latitude, longitude]`. |
| **Tile layer** | A collection of small map images, called tiles, that fit together to form the visible map. Leaflet requests the appropriate tiles as the user pans and zooms. |
| **Marker** | A point displayed on the map, often used to identify a particular location. |
| **Polygon** | A closed shape made from a sequence of geographic coordinates. It can represent an area such as a room, building section, or campus zone. |
| **Geolocation** | A browser feature that can estimate the device's current position. It generally requires the user's permission and a secure context such as HTTPS or localhost. |
| **Attribution** | A credit that identifies the source of map data or imagery. Map providers may require attribution to remain visible. |
| **DOM element** | An HTML element on the page. Leaflet needs a container element in which to render the map. |

## 1. Find the map coordinates

1. Open [uMap](https://umap.openstreetmap.fr/).
2. Zoom in until you can see the site or area you want your map to display.
3. Right-click the point you want to use as the map's starting center.
4. Copy the displayed coordinate pair.

Coordinates are commonly written as two decimal numbers: latitude first, longitude second. For example, a coordinate pair might look like `[37.0000, -87.0000]`. Use the actual coordinates for your location rather than this example.

The map's starting center determines which part of the world appears when the page first loads. Choosing a useful center prevents the map from opening at a zoomed-out view of the entire world.

## 2. Create the project files

Create an `index.html` file and a `style.css` file. These names are suggestions; if you choose different names, make sure the HTML links to the correct stylesheet.

A simple project structure could look like this:

```text
project-folder/
├── index.html
├── style.css
└── drawMaps/
    └── UserIcon.png
```

The `index.html` file contains the page structure and map JavaScript. The `style.css` file controls the map's appearance. The `drawMaps` folder contains the custom image used for the user's location marker.

Start `index.html` with standard HTML boilerplate. The stylesheet link belongs inside the `<head>` element:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Map</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- The map container will go here. -->
</body>
</html>
```

The viewport meta tag helps the page size itself correctly on phones and other small screens. The stylesheet link tells the browser to load the CSS rules from `style.css`.

## 3. Load Leaflet

Leaflet needs its CSS and JavaScript files before the map can be created. Add the following inside the `<head>` element of `index.html`:

```html
<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""
>

<script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
></script>
```

The **Leaflet CSS file** supplies the styles Leaflet needs for map controls, markers, and other built-in elements. The **Leaflet JavaScript file** defines the `L` object and the methods used in the examples, such as `L.map()`, `L.tileLayer()`, `L.marker()`, and `L.polygon()`.

The `integrity` attribute lets the browser check that the downloaded file matches the expected content. The `crossorigin` attribute supports the cross-origin request used to load the library from the CDN.

Keep the Leaflet CSS and JavaScript versions compatible. If you change the version number, use the matching CDN URLs and integrity values from the Leaflet documentation.

## 4. Add the map container

Inside the `<body>` element, add a `div` with the ID `map`:

```html
<div id="map"></div>
```

This `div` is the **container** (or mounting element) where Leaflet draws the map. The ID is important because the JavaScript uses `L.map('map')` to find it.

The container must have a defined height in CSS. If it has no height, the map may technically be created but remain invisible because the browser gives it no space to display in.

## 5. Initialize the map and tile layer

Add a script after the map container, near the end of the `<body>`. This ensures the browser has created the `map` element before the JavaScript tries to use it.

```html
<script>
    // Create the Leaflet map inside the element whose ID is "map".
    const map = L.map('map', {
        zoomControl: false,
        attributionControl: true
    }).setView([LATITUDE, LONGITUDE], 18);

    // Add the OpenStreetMap tile images to the map.
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        minZoom: 15,
        maxZoom: 22,
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | SICTC CS Class'
    }).addTo(map);

    // Restrict panning to a padded area around the map's initial bounds.
    map.setMaxBounds(map.getBounds().pad(0.15));
</script>
```

Replace `LATITUDE` and `LONGITUDE` with your starting coordinates. They must be numeric values, not words or quoted strings.

### What the map options mean

- `L.map('map', ...)` creates the Leaflet map and connects it to the HTML element with the ID `map`.
- `zoomControl: false` hides Leaflet's default zoom buttons. Users may still be able to zoom with a mouse wheel or touch gestures, depending on the device and map settings.
- `attributionControl: true` keeps the attribution display enabled so map-data credits can be shown.
- `.setView([latitude, longitude], 18)` sets the initial center and zoom level. A larger zoom number shows a closer view; a smaller number shows a wider area.
- `L.tileLayer(...)` defines where Leaflet gets the map's tile images. The `{z}`, `{x}`, and `{y}` parts of the URL are placeholders Leaflet replaces with the zoom level and tile coordinates it needs.
- `minZoom` and `maxZoom` set the zoom range allowed by this tile layer. The values should be chosen to suit the map provider and the area being mapped.
- `attribution` displays credit for the map data. Keep required provider credits visible and follow the provider's usage terms.
- `.addTo(map)` adds the tile layer to the map.
- `map.getBounds()` gets the geographic bounds currently visible in the map. `.pad(0.15)` expands those bounds slightly, and `setMaxBounds()` limits how far the user can pan outside that area.

**Zoom setting note:** The starting zoom in `setView()` should fall between the configured minimum and maximum zoom levels. For example, a starting zoom of `18` will not work as intended if `minZoom` is set to `19`. Adjust these values to match your site.

## 6. Draw areas with polygons

In this project, polygons are used to represent areas such as classrooms. The original implementation defines the coordinates directly in JavaScript, which is called **hard-coding**. Hard-coding is straightforward for a small, fixed map, but it can become difficult to maintain when many shapes need to be added or changed.

Add the polygon code inside the same script as the map initialization, after `map` has been created:

```javascript
// Each pair is [latitude, longitude].
// Add points in order around the outline of the area.
const classroomCoords = [
    [TOP_LEFT_LAT, TOP_LEFT_LNG],
    [TOP_RIGHT_LAT, TOP_RIGHT_LNG],
    [BOTTOM_RIGHT_LAT, BOTTOM_RIGHT_LNG],
    [BOTTOM_LEFT_LAT, BOTTOM_LEFT_LNG]
];

// Create the polygon and add it to the map.
const classroom = L.polygon(classroomCoords, {
    color: '#243D57',       // Outline color
    fillColor: '#243D57',   // Interior color
    fillOpacity: 0.5        // Transparency from 0 (clear) to 1 (opaque)
}).addTo(map);
```

Replace the placeholder coordinate names with real numeric latitude and longitude values. Collect the points in order around the perimeter of the area. Add more points if the outline has more than four corners. Leaflet closes the polygon between the final point and the first point.

### Polygon styling options

- `color` sets the outline (border) color.
- `fillColor` sets the color inside the polygon.
- `fillOpacity` controls how transparent the fill is. A value of `0` makes the fill fully transparent; `1` makes it fully opaque.

You can create multiple polygons by defining a different coordinate array and polygon variable for each area. Give each variable a descriptive name, such as `classroom101Coords` or `libraryPolygon`, so the code is easier to understand.

## 7. Display the user's location

Leaflet can request the device's location through the browser's geolocation feature. The browser normally asks the user for permission before sharing this information. Geolocation generally requires the page to be served over HTTPS, or to be running on `localhost` during development.

### 7.1 Create a custom user icon

The icon image should be stored in your project and referenced with a path that is correct relative to the HTML file:

```javascript
const userIcon = L.icon({
    iconUrl: 'drawMaps/UserIcon.png',
    iconSize: [38, 38]
});
```

`L.icon()` creates a custom marker icon. The `iconUrl` property points to the image file, and `iconSize` sets its displayed width and height in pixels. If the image does not appear, check the spelling, capitalization, and relative file path.

### 7.2 Create the marker and accuracy circle

The location marker shows the reported position. The circle gives a visual indication of the location estimate's accuracy.

```javascript
let locationMarker = null;
let locationCircle = null;

function onLocationFound(e) {
    // The browser reports an estimated accuracy in meters.
    const radius = e.accuracy / 2;

    if (locationMarker === null) {
        // Create the marker and circle the first time a location is received.
        locationMarker = L.marker(e.latlng, {
            icon: userIcon
        }).addTo(map);

        locationCircle = L.circle(e.latlng, {
            radius: radius
        }).addTo(map);
    } else {
        // Move the existing marker and update the circle on later updates.
        locationMarker.setLatLng(e.latlng);
        locationCircle.setLatLng(e.latlng);
        locationCircle.setRadius(radius);
    }
}

function onLocationError(e) {
    alert(e.message);
}

// Ask the browser to locate the device.
map.locate({
    setView: true,
    maxZoom: 18,
    enableHighAccuracy: true,
    watch: true
});

// Listen for successful location updates and errors.
map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);
```

### How the geolocation code works

- `locationMarker` and `locationCircle` begin as `null`, meaning that no marker or circle has been created yet.
- `map.locate()` asks the browser to determine the device's position.
- `enableHighAccuracy: true` asks the device for a more accurate position when possible. It does not guarantee a particular accuracy level.
- `setView: true` asks Leaflet to move the map to the reported location.
- `maxZoom` sets the maximum zoom Leaflet should use when centering on the location.
- `watch: true` tells Leaflet to continue listening for position changes rather than requesting only one position.
- When Leaflet receives a position, it fires the `locationfound` event. The `onLocationFound` function receives the event object as `e`.
- `e.latlng` contains the reported latitude and longitude. `e.accuracy` contains the reported accuracy radius in meters.
- The first location update creates the marker and circle. Later updates move the existing objects instead of adding duplicates.
- `locationCircle.setRadius(radius)` updates the circle's size when the reported accuracy changes.
- If the browser cannot retrieve the location, Leaflet fires `locationerror`, and the `onLocationError` function displays the error message.

The example uses `e.accuracy / 2` to make the displayed circle smaller than the full reported accuracy radius. If you want the circle to represent the browser's full reported accuracy radius, use `e.accuracy` instead.

## 8. Style the map with CSS

Add the following rules to `style.css`:

```css
#map {
    position: fixed;
    top: 10%;
    left: 1%;
    width: 98%;
    height: 60%;
    margin-top: 10px;

    border: 5px solid #707F43;
    background-color: #fff;
}
```

The `#map` selector targets the element whose ID is `map`.

- `position: fixed` positions the map relative to the browser window, so it stays in the same place while the page scrolls.
- `top` and `left` set the map's distance from the top and left edges of the viewport.
- `width` and `height` determine how much screen space the map occupies. Percentage values adjust with the viewport size.
- `margin-top` adds space above the element, although it may be unnecessary when using fixed positioning and a `top` value.
- `border` adds an outline around the map.
- `background-color` sets the background visible behind the map tiles.

Leaflet also provides a class for the small attribution text in the map corner. You can adjust its font size:

```css
.leaflet-control-attribution {
    font-size: 15px;
}
```

The `.leaflet-control-attribution` selector targets Leaflet's attribution control. Avoid hiding or obscuring this control because it contains required map-data credits.

### Responsive sizing

Fixed pixel dimensions can be difficult to use on phones and tablets. Percentage dimensions, viewport units, and media queries can help the map fit different screen sizes. For example:

```css
#map {
    width: 98%;
    height: 60vh;
}

@media (max-width: 600px) {
    #map {
        top: 8%;
        height: 70vh;
    }
}
```

`vh` means **viewport height**. A height of `60vh` uses 60% of the browser window's height. The media query applies different styling when the viewport is 600 pixels wide or narrower.

If your project already has navigation or mobile-specific styles, make sure those rules do not conflict with the map's position and dimensions. In particular, review selectors such as `#map.nav-active` in `mobile.css` if that file is part of your project.

## Troubleshooting and implementation notes

| Problem | What to check |
|---|---|
| The map is blank or invisible | Make sure the `#map` element exists, has a non-zero CSS height, and appears before the map initialization script runs. |
| `L is not defined` appears in the console | Check that the Leaflet JavaScript file loaded successfully and is included before your map code. |
| The map opens in the wrong location | Check the latitude/longitude order and the coordinates passed to `setView()`. Leaflet uses `[latitude, longitude]`. |
| The zoom level does not behave as expected | Make sure the initial zoom is between `minZoom` and `maxZoom`. Also check the limits supported by the tile provider. |
| A polygon appears in the wrong place or has an odd shape | Check every coordinate pair, confirm the order is `[latitude, longitude]`, and list the points in perimeter order. |
| The custom user icon is missing | Confirm the image exists and that `iconUrl` points to the correct relative path. Check capitalization too. |
| Geolocation does not work | Check browser permission settings and use HTTPS or localhost. Also check whether the device has location services enabled. |
| The map attribution is missing or covered | Keep Leaflet's attribution control enabled and make sure custom CSS does not hide it. |

### Ideas for future improvements

The original approach creates each polygon by writing its coordinates directly into the JavaScript. For a map with many rooms, consider storing room names, coordinates, and display styles in a structured array or a separate JSON file, then looping through that data to create the polygons. This reduces repeated code and makes it easier to update the map.

You could also attach a popup to each polygon so users can select a room and see its name or other information. Leaflet supports this with methods such as `bindPopup()`.

## Helpful resources

- [OpenStreetMap](https://www.openstreetmap.org/) — Open geographic data and map information.
- [uMap](https://umap.openstreetmap.fr/) — Create and explore maps using OpenStreetMap data.
- [Leaflet documentation](https://leafletjs.com/reference.html) — Official reference for Leaflet classes, methods, and options.
- [Leaflet quick start guide](https://leafletjs.com/examples/quick-start/) — A beginner-friendly walkthrough of creating a Leaflet map.
- [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/) — Important guidance about using the standard OpenStreetMap tile service.

---

**You have now created the foundation of an interactive map.** To understand how the map fits into the larger project, review the related `mobile.html` and `mobile.css` files, especially any rules that change the map's layout when navigation is active.
