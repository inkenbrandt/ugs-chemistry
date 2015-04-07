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
        version: '0.2.0',

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
            StationType: 'StationType',
            HUC8: 'HUC8',
            OrgId: 'OrgId',

            // Results
            StationId: StationId, // also used in Stations
            ParamGroup: 'ParamGroup',
            DataSource: 'DataSource',
            Param: 'Param'
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
            ['Box Elder', 3],
            ['Cache', 5],
            ['Carbon', 7],
            ['Daggett', 9],
            ['Davis', 11],
            ['Duchesne', 13],
            ['Emery', 15],
            ['Garfield', 17],
            ['Grand', 19],
            ['Iron', 21],
            ['Juab', 23],
            ['Kane', 25],
            ['Millard', 27],
            ['Morgan', 29],
            ['Piute', 31],
            ['Rich', 33],
            ['Salt Lake', 35],
            ['San Juan', 37],
            ['Sanpete', 39],
            ['Sevier', 41],
            ['Summit', 43],
            ['Tooele', 45],
            ['Uintah', 47],
            ['Utah', 49],
            ['Wasatch', 51],
            ['Washington', 53],
            ['Wayne', 55],
            ['Weber', 57]
        ],
        states: [
            ['Utah', 49],
            ['Idaho', 16],
            ['Wyoming', 56],
            ['Colorado', 8],
            ['New Mexico', 35],
            ['Arizona', 4],
            ['Nevada', 32]
        ],
        siteTypes: [
            ['Atmosphere', 'Atmosphere'],
            ['Facility', 'Facility'],
            ['Lake, Reservoir,  Impoundment', 'Lake, Reservoir,  Impoundment'],
            ['Land', 'Land'],
            ['Other Groundwater', 'Other Groundwater'],
            ['Other', 'Other'],
            ['Spring', 'Spring'],
            ['Stream', 'Stream'],
            ['Surface Water', 'Surface Water'],
            ['Well', 'Well'],
            ['Wetland', 'Wetland']
        ],
        parameterGroups: [
            ['Information', 'Information'],
            ['Inorganics, Minor, Metals', 'Inorganics, Minor, Metals'],
            ['Inorganics, Major, Metals', 'Inorganics, Major, Metals'],
            ['Stable Isotopes', 'Stable Isotopes'],
            ['Inorganics, Minor, Non-metals', 'Inorganics, Minor, Non-metals'],
            ['Organics, other', 'Organics, other'],
            ['Microbiological', 'Microbiological'],
            ['Biological', 'Biological'],
            ['Nutrient', 'Nutrient'],
            ['Inorganics, Major, Non-metals', 'Inorganics, Major, Non-metals'],
            ['Radiochemical', 'Radiochemical'],
            ['Organics, pesticide', 'Organics, pesticide'],
            ['Organics, PCBs', 'Organics, PCBs'],
            ['Toxicity', 'Toxicity'],
            ['Sediment', 'Sediment'],
            ['Physical', 'Physical']
        ],
        dataSources: [
            ['DOGM', 'DOGM'],
            ['DWR', 'DWR'],
            ['SDWIS', 'SDWIS'],
            ['UGS', 'UGS'],
            ['WQP', 'WQP']
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
