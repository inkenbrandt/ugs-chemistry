define([
    'dojo/text!app/templates/App.html',

    'dojo/_base/declare',
    'dojo/_base/array',

    'dojo/dom',
    'dojo/dom-style',
    'dojo/aspect',
    'dojo/store/Memory',

    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dijit/registry',

    'dgrid/OnDemandGrid',

    'agrc/widgets/map/BaseMap',
    'agrc/widgets/map/BaseMapSelector',
    'agrc/widgets/locate/MagicZoom',

    'esri/layers/FeatureLayer',
    'esri/InfoTemplate',
    'esri/tasks/query',
    'esri/tasks/RelationshipQuery',

    'dojo/text!app/templates/Popup.html',

    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane'
], function(
    template,

    declare,
    array,

    dom,
    domStyle,
    aspect,
    Memory,

    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    registry,

    Grid,

    BaseMap,
    BaseMapSelector,
    MagicZoom,

    FeatureLayer,
    InfoTemplate,
    Query,
    RelationshipQuery,

    popupTemplate
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        // summary:
        //      The main widget for the app

        widgetsInTemplate: true,
        templateString: template,
        baseClass: 'app',

        // map: agrc.widgets.map.Basemap
        map: null,

        constructor: function() {
            // summary:
            //      first function to fire after page loads
            console.info('app.App::constructor', arguments);

            AGRC.app = this;

            this.inherited(arguments);
        },
        postCreate: function() {
            // summary:
            //      Fires when
            console.log('app.App::postCreate', arguments);

            // set version number
            this.version.innerHTML = AGRC.version;

            this.inherited(arguments);

            var lyr = new FeatureLayer(AGRC.urls.mapService + '/1', {outFields: '*'});

            var that = this;
            lyr.on('load', function() {
                var columns = array.map(lyr.fields, function (f) {
                    return {
                        label: f.alias,
                        field: f.name
                    };
                });
                that.grid = new (declare([Grid]))({
                    bufferRows: Infinity,
                    columns: columns,
                    sort: [{attribute: 'ActivityStartDate', descending: true}]
                }, that.gridDiv);
            });
        },
        startup: function() {
            // summary:
            //      Fires after postCreate when all of the child widgets are finished laying out.
            console.log('app.App::startup', arguments);

            // call this before creating the map to make sure that the map container is
            // the correct size
            this.inherited(arguments);

            var stationId;

            this.initMap();

            stationId = new MagicZoom({
                map: this.map,
                mapServiceURL: AGRC.urls.mapService,
                searchLayerIndex: 0,
                searchField: AGRC.fields.MonitoringLocationIdentifier,
                placeHolder: 'search by id...',
                maxResultsToDisplay: 10
            }, this.stationNameDiv);

            var that = this;
            this.own(aspect.after(stationId, 'onZoomed', function (graphic) {
                var q = new Query();
                q.where = AGRC.fields.MonitoringLocationIdentifier + " = '" + graphic.attributes[AGRC.fields.MonitoringLocationIdentifier] + "'";
                that.lyr.queryFeatures(q, function (fSet) {
                    var g = fSet.features[0];
                    that.map.infoWindow.setFeatures([g]);
                    that.map.infoWindow.show(g.geometry);
                    that.showRelatedRows(g.attributes['OBJECTID']);
                }, function (err) {
                    console.log(err);
                });
            }, true));

            this.rQuery = new RelationshipQuery();
            this.rQuery.outFields = ['*'];
            this.rQuery.relationshipId = 0;

            this.lyr.on('click', function (g) {
                that.showRelatedRows(g.graphic.attributes['OBJECTID']);
            });

            this.inherited(arguments);
        },
        showRelatedRows: function (oid) {
            // summary:
            //      populates the dgrid with results related to the station 
            //  
            // oid: String
            //      Objectid of the related station
            console.log('app/App:showRelatedRows', arguments);

            var that = this;
        
            this.rQuery.objectIds = [oid];
            this.lyr.queryRelatedFeatures(this.rQuery, function (rFeatures) {
                var data = array.map(rFeatures[oid].features, function (r) {
                    return r.attributes;
                });
                var store = new Memory({data: data});
                that.grid.set('store', store);
            });
        },
        initMap: function() {
            // summary:
            //      Sets up the map
            console.info('app.App::initMap', arguments);

            this.map = new BaseMap(this.mapDiv, {
                useDefaultBaseMap: false
            });


            this.map.infoWindow.resize(450, 300);

            var selector;

            selector = new BaseMapSelector({
                map: this.map,
                id: 'claro',
                position: 'TR'
            });

            var template = new InfoTemplate('${MonitoringLocationIdentifier}', popupTemplate);
            this.lyr = new FeatureLayer(AGRC.urls.mapService + '/0', {
                opacity: 0.7,
                infoTemplate: template,
                outFields: '*'
            });
            this.map.addLayer(this.lyr);
            this.map.addLoaderToLayer(this.lyr);
        }
    });
});
