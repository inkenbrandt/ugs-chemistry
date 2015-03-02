define([
    'agrc/widgets/locate/MagicZoom',
    'agrc/widgets/map/BaseMap',
    'agrc/widgets/map/BaseMapSelector',

    'app/config',

    'dgrid/OnDemandGrid',

    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',
    'dijit/registry',

    'dojo/_base/array',
    'dojo/_base/declare',
    'dojo/aspect',
    'dojo/dom',
    'dojo/dom-style',
    'dojo/store/Memory',
    'dojo/text!app/templates/App.html',

    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane'
], function(
    MagicZoom,
    BaseMap,
    BaseMapSelector,

    config,

    Grid,

    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTemplateMixin,
    registry,

    array,
    declare,
    aspect,
    dom,
    domStyle,
    Memory,
    template
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
        },
        startup: function() {
            // summary:
            //      Fires after postCreate when all of the child widgets are finished laying out.
            console.log('app.App::startup', arguments);

            // call this before creating the map to make sure that the map container is
            // the correct size
            this.inherited(arguments);

            this.initMap();
        },
        initMap: function() {
            // summary:
            //      Sets up the map
            console.info('app.App::initMap', arguments);

            this.map = new BaseMap(this.mapDiv, {
                useDefaultBaseMap: false
            });

            var selector;

            selector = new BaseMapSelector({
                map: this.map,
                id: 'claro',
                position: 'TR'
            });
        }
    });
});
