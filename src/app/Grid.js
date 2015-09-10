define([
    'app/config',

    'dgrid/extensions/ColumnResizer',
    'dgrid/OnDemandGrid',

    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/declare',
    'dojo/_base/lang',
    'dojo/_base/query',
    'dojo/dom-class',
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
    query,
    domClass,
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

        // stationGrid: Grid
        stationGrid: null,

        // resultGrid: Grid
        resultGrid: null,

        // stationQuery: Query
        stationQuery: null,

        // stationQueryTask: QueryTask
        stationQueryTask: null,

        // resultQuery: Query
        resultQuery: null,

        // resultQueryTask: QueryTask
        resultQueryTask: null,

        // Properties to be sent into constructor

        postCreate: function () {
            // summary:
            //      Overrides method of same name in dijit._Widget.
            // tags:
            //      private
            console.log('app.Grid::postCreate', arguments);

            this.own(
                topic.subscribe(config.topics.queryIdsComplete, lang.hitch(this, 'populateGrid')),
                query('a[data-toggle="tab"]').on('shown.bs.tab', lang.hitch(this, 'onTabSwitched'))
            );

            this.inherited(arguments);
        },
        onQueryTaskComplete: function (grid, response) {
            // summary:
            //      description
            // grid: Grid
            // response: Object
            console.log('app/Grid:onQueryTaskComplete', arguments);

            var showGrid;

            this.hideErrMsg();

            if (response.featureSet.features.length) {
                showGrid = true;
                var data = response.featureSet.features.map(function (g) {
                    return g.attributes;
                });
                grid.store.setData(data);
                grid.refresh();
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
        populateGrid: function (defQuery, preservePreviousData) {
            // summary:
            //      description
            // param: type or return: type
            // preservePreviousData: Boolean
            console.log('app/Grid:populateGrid', arguments);

            if (defQuery === '1 = 2') {
                topic.publish(config.topics.toggleGrid, false);
                this.lastDefQuery = '1 = 2';
            } else {
                if (domClass.contains(this.stationsTab, 'active')) {
                    if (!this.stationGrid) {
                        this.initStationGrid();
                    }
                    this.stationQuery.where = defQuery;
                    this.stationQueryTask.execute(this.stationQuery);
                } else {
                    if (!this.resultGrid) {
                        this.initResultGrid();
                    }
                    this.resultQuery.where = 'StationId IN (SELECT StationId FROM Stations WHERE ' + defQuery + ')';
                    this.resultQueryTask.execute(this.resultQuery);
                }
                this.lastDefQuery = defQuery;
            }

            if (!preservePreviousData) {
                if (this.stationGrid) {
                    this.stationGrid.store.setData([]);
                    this.stationGrid.refresh();
                }
                if (this.resultGrid) {
                    this.resultGrid.store.setData([]);
                    this.resultGrid.refresh();
                }
            }
        },
        initResultGrid: function () {
            // summary:
            //
            console.log('app/Grid:initResultGrid', arguments);

            var fn = config.fieldNames;
            var resultColumns = [
                {
                    field: fn.Id
                }, {
                    field: fn.Param,
                    label: 'Parameter'
                }, {
                    field: fn.ResultValue,
                    label: 'Measure Value'
                }, {
                    field: fn.Unit,
                    label: 'Meaure Unit'
                }, {
                    field: fn.SampleDate,
                    label: 'Sample Date'
                }, {
                    field: fn.StationId,
                    label: 'Station Id'
                }, {
                    field: fn.DetectCond,
                    label: 'Detection Condition'
                }
            ];

            this.resultGrid = this.buildGrid(this.resultGridDiv, resultColumns);

            this.resultQuery = new Query();
            this.resultQuery.returnGeometry = false;
            this.resultQuery.outFields = [
                fn.Id,
                fn.Param,
                fn.ResultValue,
                fn.Unit,
                fn.SampleDate,
                fn.StationId,
                fn.DetectCond
            ];
            this.resultQueryTask = new QueryTask(config.urls.mapService + '/' + config.layerIndices.results);
            this.own(
                this.resultQueryTask.on('complete',
                    lang.hitch(this, lang.partial(this.onQueryTaskComplete, this.resultGrid))),
                this.resultQueryTask.on('error', lang.hitch(this, 'onQueryTaskError'))
            );
        },
        initStationGrid: function () {
            // summary:
            //      description
            console.log('app/Grid:initStationGrid', arguments);

            var fn = config.fieldNames;
            var stationColumns = [
                {
                    field: fn.Id
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
                }, {
                    field: fn.Depth,
                    label: 'Well Depth'
                }, {
                    field: fn.WIN,
                    label: 'WR Well Id'
                }
            ];

            this.stationGrid = this.buildGrid(this.stationGridDiv, stationColumns);

            this.stationQuery = new Query();
            this.stationQuery.returnGeometry = false;
            this.stationQuery.outFields = [
                fn.Id,
                fn.DataSource,
                fn.StationId,
                fn.StationName,
                fn.StationType,
                fn.Depth,
                fn.WIN
            ];
            this.stationQueryTask = new QueryTask(config.urls.mapService + '/' + config.layerIndices.main);
            this.own(
                this.stationQueryTask.on('complete',
                    lang.hitch(this, lang.partial(this.onQueryTaskComplete, this.stationGrid))),
                this.stationQueryTask.on('error', lang.hitch(this, 'onQueryTaskError'))
            );
        },
        buildGrid: function (div, columns) {
            // summary:
            //      description
            // div: Dom Node
            // columns: Object[]
            console.log('app/Grid:buildGrid', arguments);

            var grid = new (declare([Grid, ColumnResizer]))({
                columns: columns,
                store: new Memory({idProperty: config.fieldNames.Id})
            }, div);
            grid.startup();
            return grid;
        },
        onTabSwitched: function () {
            // summary:
            //      description
            console.log('app/Grid:onTabSwitched', arguments);

            if (!this.stationGrid || !this.resultGrid ||
                this.stationGrid.store.data.length === 0 || this.resultGrid.store.data.length === 0) {
                this.populateGrid(this.lastDefQuery, true);
            }
        }
    });
});
