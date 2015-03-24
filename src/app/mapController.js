define([
    'agrc/widgets/map/BaseMap',
    'agrc/widgets/map/BaseMapSelector',

    'app/config',

    'esri/layers/ArcGISDynamicMapServiceLayer'
], function (
    BaseMap,
    BaseMapSelector,

    config,

    ArcGISDynamicMapServiceLayer
) {
    return {
        // map: BaseMap
        map: null,

        initMap: function (mapDiv) {
            // summary:
            //      Sets up the map
            console.info('app.App::initMap', arguments);

            this.map = new BaseMap(mapDiv, {
                useDefaultBaseMap: false
            });

            var selector;
            selector = new BaseMapSelector({
                map: this.map,
                id: 'tundra',
                position: 'TR'
            });

            var lyr = new ArcGISDynamicMapServiceLayer(config.urls.mapService);

            this.map.addLayer(lyr);
            this.map.addLoaderToLayer(lyr);
        }
    };
});