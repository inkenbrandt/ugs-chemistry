define([
    'agrc/widgets/map/BaseMap',
    'agrc/widgets/map/BaseMapSelector',

    'app/config',

    'dojo/_base/lang',
    'dojo/Deferred',
    'dojo/on',
    'dojo/topic',

    'esri/Color',
    'esri/graphic',
    'esri/layers/ArcGISDynamicMapServiceLayer',
    'esri/layers/FeatureLayer',
    'esri/tasks/query',
    'esri/tasks/QueryTask'
], function (
    BaseMap,
    BaseMapSelector,

    config,

    lang,
    Deferred,
    on,
    topic,

    Color,
    Graphic,
    ArcGISDynamicMapServiceLayer,
    FeatureLayer,
    Query,
    QueryTask
) {
    return {
        // map: BaseMap
        map: null,

        // dLayer: ArcGISDynamicMapServiceLayer
        //      layer that is displayed at smaller scales
        dLayer: null,

        // fLayer: FeatureLayer
        //      layer that is displayed at larger scales
        fLayer: null,

        // fLayerSelection: FeatureLayer
        //      layer that displays the selected stations at larger scales
        fLayerSelection: null,

        initMap: function (mapDiv) {
            // summary:
            //      Sets up the map
            console.info('app/mapController:initMap', arguments);

            var that = this;

            this.map = new BaseMap(mapDiv, {
                useDefaultBaseMap: false
            });

            var selector;
            selector = new BaseMapSelector({
                map: this.map,
                id: 'tundra',
                position: 'TR'
            });

            this.dLayer = new ArcGISDynamicMapServiceLayer(config.urls.mapService, {
                maxScale: config.minFeatureLayerScale
            });
            this.dLayer.setLayerDefinitions(['1 = 2', '1 = 1']);
            this.map.addLayer(this.dLayer);
            this.map.addLoaderToLayer(this.dLayer);

            var addFeatureLayer = function (index, visible) {
                var fLayer = new FeatureLayer(config.urls.mapService + '/' + index, {
                    minScale: config.minFeatureLayerScale,
                    visible: visible
                });
                fLayer.on('load', function () {
                    fLayer.renderer.symbol.setSize(config.stationSymbolSize);
                });
                that.map.addLayer(fLayer);
                that.map.addLoaderToLayer(fLayer);
                return fLayer;
            };
            this.fLayer = addFeatureLayer(config.layerIndices.main, true);
            this.fLayerSelection = addFeatureLayer(config.layerIndices.selection, false);

            this.queryFLayer = new FeatureLayer(config.urls.mapService + '/' + config.layerIndices.main);
            this.queryFLayer.on('query-ids-complete', lang.hitch(this, 'queryIdsComplete'));

            topic.subscribe(config.topics.selectFeatures, lang.hitch(this, 'selectFeatures'));
            topic.subscribe(config.topics.addGraphic, function (geo) {
                that.map.graphics.clear();
                that.map.graphics.add(new Graphic(geo, config.drawingSymbol));
            });
            topic.subscribe(config.topics.removeGraphic, function () {
                that.map.graphics.clear();
            });
        },
        selectFeatures: function (defQuery, geometry) {
            // summary:
            //      selects stations on the map
            //      applies selection to dLayer & fLayer
            // defQuery[optional]: String
            //      select by definition query
            // geometry[optional]: Polygon
            //      select by geometry
            console.log('app/mapController:selectFeatures', arguments);

            var query = new Query();
            if (defQuery) {
                query.where = defQuery;
            }
            if (geometry) {
                query.geometry = geometry;
            }
            if (defQuery || geometry) {
                this.map.showLoader();
                this.queryFLayer.queryIds(query);
            } else {
                this.queryIdsComplete({});
            }
        },
        queryIdsComplete: function (response) {
            // summary:
            //      callback for fLayer.queryIds
            // response: {objectIds: Number[]}
            console.log('app/mapController:queryIdsComplete', arguments);

            this.map.hideLoader();
            var selectDef;
            var mainDef;
            if (response.objectIds) {
                selectDef = config.fieldNames.Id + ' IN (' + response.objectIds.join(', ') + ')';
                mainDef = selectDef.replace('IN', 'NOT IN');
            } else {
                selectDef = '1 = 2';
                mainDef = '1 = 1';
            }
            // if I use selectFeatures then it doesn't make requests by grid and it
            // hits the 1000 feature return limit much sooner
            this.fLayerSelection.setDefinitionExpression(selectDef);
            this.fLayerSelection.show();
            this.fLayer.setDefinitionExpression(mainDef);

            var defs = [];
            defs[config.layerIndices.selection] = selectDef;
            defs[config.layerIndices.main] = mainDef;
            this.dLayer.setLayerDefinitions(defs);

            topic.publish(config.topics.queryIdsComplete, selectDef);
        },
        getParameters: function () {
            // summary:
            //      query tasks for the parameter values
            console.log('app/mapController:getParameters', arguments);

            var def = new Deferred();
            var q = new Query();
            q.returnGeometry = false;
            q.outFields = [config.fieldNames.Param];
            q.where = '1 = 1';

            var qt = new QueryTask(config.urls.mapService + '/' + config.layerIndices.parameters);

            qt.execute(q).then(function (fSet) {
                var params = fSet.features.map(function (f) {
                    return f.attributes[config.fieldNames.Param];
                });
                def.resolve(params);
            }, function () {
                def.reject();
            });

            return def;
        }
    };
});
