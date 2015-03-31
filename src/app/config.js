/* jshint maxlen:false */
define([
    'dojo/has',

    'esri/Color',
    'esri/config',
    'esri/symbols/SimpleFillSymbol',
    'esri/symbols/SimpleLineSymbol',

    'dojo/domReady!'
], function (
    has,

    Color,
    esriConfig,
    SimpleFillSymbol,
    SimpleLineSymbol
) {
    // force api to use CORS on mapserv thus removing the test request on app load
    // e.g. http://mapserv.utah.gov/ArcGIS/rest/info?f=json
    esriConfig.defaults.io.corsEnabledServers.push('mapserv.utah.gov');

    var agsDomain;
    if (has('agrc-build') === 'prod') {
        // mapserv.utah.gov
        // apiKey = 'AGRC-1B07B497348512';
        agsDomain = 'mapserv.utah.gov';
    } else if (has('agrc-build') === 'stage') {
        // test.mapserv.utah.gov
        // apiKey = 'AGRC-AC122FA9671436';
        agsDomain = 'test.mapserv.utah.gov';
    } else {
        // localhost
        // apiKey = 'AGRC-E5B94F99865799';
        agsDomain = window.location.host;
    }

    var baseUrl = window.location.protocol + '//' + agsDomain + '/arcgis/rest/services';
    var drawingColor = [51, 160, 44];
    var StationId = 'StationId';
    window.AGRC = {
        // errorLogger: ijit.modules.ErrorLogger
        errorLogger: null,

        // app: app.App
        //      global reference to App
        app: null,

        // appName: String
        //      for permissions proxy
        appName: 'ugs-chemistry',

        // version.: String
        //      The version number.
        version: '0.1.0',

        // apiKey: String
        //      The api key used for services on api.mapserv.utah.gov
        apiKey: '', // acquire at developer.mapserv.utah.gov

        urls: {
            mapService: baseUrl + '/UGSChemistry/MapServer',
            geometry: baseUrl + '/Geometry/GeometryServer'
        },

        minFeatureLayerScale: 500000,
        stationSymbolSize: 9,
        drawingSymbol: new SimpleFillSymbol(
            SimpleFillSymbol.STYLE_SOLID,
            new SimpleLineSymbol()
                .setColor(new Color(drawingColor)),
            new Color(drawingColor.concat([0.25]))
        ),

        fieldNames: {
            // Stations
            StateCode: 'StateCode',
            CountyCode: 'CountyCode',
            SampleDate: 'SampleDate',

            // Results
            StationId: StationId
        },

        queryByResults: StationId + " IN (SELECT " + StationId + " FROM Results WHERE ",

        layerIndices: {
            selection: 0,
            main: 1
        },

        topics: {
            selectFeatures: 'ugs-select-features',
            addGraphic: 'ugs-add-graphic',
            removeGraphic: 'ugs-remove-graphic'
        },

        counties: [
            ['Beaver', 1],
            ['Box Elder', 2],
            ['Cache', 3],
            ['Carbon', 4],
            ['Daggett', 5],
            ['Davis', 6],
            ['Duchesne', 7],
            ['Emery', 8],
            ['Garfield', 9],
            ['Grand', 10],
            ['Iron', 11],
            ['Juab', 12],
            ['Kane', 13],
            ['Millard', 14],
            ['Morgan', 15],
            ['Piute', 16],
            ['Rich', 17],
            ['Salt Lake', 18],
            ['San Juan', 19],
            ['Sanpete', 20],
            ['Sevier', 21],
            ['Summit', 22],
            ['Tooele', 23],
            ['Uintah', 24],
            ['Utah', 25],
            ['Wasatch', 26],
            ['Washington', 27],
            ['Wayne', 28],
            ['Weber', 29],
        ],
        states: [
            ['Utah', 49],
            ['Idaho', 16],
            ['Wyoming', 56],
            ['Colorado', 8],
            ['New Mexico', 35],
            ['Arizona', 4],
            ['Nevada', 32]
        ]
    };

    if (has('agrc-build') === 'prod') {
        // mapserv.utah.gov
        window.AGRC.apiKey = 'AGRC-A94B063C533889';
    } else if (has('agrc-build') === 'stage') {
        // test.mapserv.utah.gov
        window.AGRC.apiKey = 'AGRC-AC122FA9671436';
    } else {
        // localhost
        window.AGRC.apiKey = 'AGRC-E5B94F99865799';
    }

    return window.AGRC;
});
