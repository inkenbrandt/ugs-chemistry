(function () {
    // the baseUrl is relavant in source version and while running unit tests.
    // the`typeof` is for when this file is passed as a require argument to the build system
    // since it runs on node, it doesn't have a window object. The basePath for the build system
    // is defined in build.profile.js
    var config = {
        baseUrl: (
            typeof window !== 'undefined' &&
            window.dojoConfig &&
            window.dojoConfig.isJasmineTestRunner
            ) ? '/src': './',
        packages: [
            'agrc',
            'app',
            'dgrid',
            'dijit',
            'dojo',
            'dojo-bootstrap',
            'dojox',
            'esri',
            'ijit',
            'put-selector',
            'xstyle',
            {
                name: 'ladda',
                location: './ladda-bootstrap',
                main: 'dist/ladda'
            },{
                name: 'mustache',
                location: './mustache',
                main: 'mustache'
            },{
                name: 'spin',
                location: './spinjs',
                main: 'spin'
            },{
                name: 'stubmodule',
                location: './stubmodule',
                main: 'src/stub-module'
            }
        ],
        map: {
            ijit: {
                jquery: 'dojo/query',
                bootstrap: 'app/dojo-bootstrap-plugins'
            },
            ladda: {
                spin: 'ladda/dist/spin'
            }
        }
    };
    require(config, ['dojo/parser', 'dojo/domReady!'], function (parser) {
        parser.parse();
    });
})();