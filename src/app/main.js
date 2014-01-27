define([
    'dojo/parser', 

    'app/App'
], 

function (
    parser
    ) {
    window.AGRC = {
        // errorLogger: ijit.modules.ErrorLogger
        errorLogger: null,

        // app: app.App
        //      global reference to App
        app: null,

        // version: String
        //      The version number.
        version: '0.1.0',

        // apiKey: String
        //      The api key used for services on api.mapserv.utah.gov
        // apiKey: 'AGRC-63E1FF17767822', // localhost
        apiKey: 'AGRC-A94B063C533889', // key for atlas.utah.gov

        urls: {
            mapService: '/arcgis/rest/services/UGSChemistry/MapServer'
        },

        fields: {
            MonitoringLocationIdentifier: 'MonitoringLocationIdentifier'
        }
    };

    // lights...camera...action!
    parser.parse();
});