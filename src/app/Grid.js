define([
    'app/config',

    'dgrid/extensions/ColumnResizer',
    'dgrid/OnDemandGrid',

    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/declare',
    'dojo/_base/lang',
    'dojo/store/Memory',
    'dojo/text!app/templates/Grid.html',
    'dojo/topic',

    'esri/tasks/query',
    'esri/tasks/QueryTask',

    'ijit/modules/_ErrorMessageMixin',

    'dojo-bootstrap/Tab',
    'xstyle/css!app/resources/Grid.css'
], function (
    config,

    ColumnResizer,
    Grid,

    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTemplateMixin,

    declare,
    lang,
    Memory,
    template,
    topic,

    Query,
    QueryTask,

    _ErrorMessageMixin
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, _ErrorMessageMixin], {
        // description:
        //      A container to hold result grids and download link.

        templateString: template,
        baseClass: 'grid',
        widgetsInTemplate: true,

        // Properties to be sent into constructor

        postCreate: function () {
            // summary:
            //      Overrides method of same name in dijit._Widget.
            // tags:
            //      private
            console.log('app.Grid::postCreate', arguments);

            this.initGrids();

            this.own(topic.subscribe(config.topics.queryIdsComplete,
                lang.hitch(this, 'populateStationsGrid')));

            this.q = new Query();
            this.q.returnGeometry = false;
            this.q.outFields = [
                'OBJECTID',
                config.fieldNames.DataSource,
                config.fieldNames.StationId,
                config.fieldNames.StationName,
                config.fieldNames.StationType
            ];
            this.queryTask = new QueryTask(config.urls.mapService + '/' + config.layerIndices.main);
            this.own(
                this.queryTask.on('complete', lang.hitch(this, 'onQueryTaskComplete')),
                this.queryTask.on('error', lang.hitch(this, 'onQueryTaskError'))
            );

            this.inherited(arguments);
        },
        onQueryTaskComplete: function (response) {
            // summary:
            //      description
            // response: Object
            console.log('app/Grid:onQueryTaskComplete', arguments);

            var showGrid;

            this.hideErrMsg();

            if (response.featureSet.features.length) {
                showGrid = true;
                var data = response.featureSet.features.map(function (g) {
                    return g.attributes;
                });
                this.stationGrid.store.setData(data);
                this.stationGrid.refresh();
            } else {
                showGrid = false;
            }

            topic.publish(config.topics.toggleGrid, showGrid);
        },
        onQueryTaskError: function () {
            // summary:
            //      description
            console.log('app/Grid:onQueryTaskError', arguments);

            this.showErrMsg('There was an error populating the grid!');
        },
        populateStationsGrid: function (defQuery) {
            // summary:
            //      description
            // param: type or return: type
            console.log('app/Grid:populateStationsGrid', arguments);

            if (defQuery === '1 = 2') {
                topic.publish(config.topics.toggleGrid, false);
            } else {
                this.q.where = defQuery;
                this.queryTask.execute(this.q);
            }
        },
        initGrids: function () {
            // summary:
            //      builds the grids
            console.log('app/Grid:initGrids', arguments);

            var fn = config.fieldNames;

            // stations
            var columns = [
                {
                    field: 'OBJECTID'
                }, {
                    field: fn.DataSource,
                    label: 'Database Source'
                }, {
                    field: fn.StationId,
                    label: 'ID'
                }, {
                    field: fn.StationName,
                    label: 'Name'
                }, {
                    field: fn.StationType,
                    label: 'Type'
                }
            ];

            this.stationGrid = new (declare([Grid, ColumnResizer]))({
                columns: columns,
                store: new Memory({idProperty: 'OBJECTID'})
            }, this.stationGridDiv);
            this.stationGrid.startup();
        }
    });
});
